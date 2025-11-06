import React, { useState, useEffect } from 'react';
import { Card, Descriptions, Radio, Tag, Alert, Button, Spin, message, Tooltip, Collapse, Table } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { getTypeColor, getStatusColor } from '../utils/constants';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
});

export default function LessonDetail() {
  const { lessonId } = useParams();
  const [lessonData, setLessonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();
  const [groupAttendances, setGroupAttendances] = useState({});
  const [originalAttendances, setOriginalAttendances] = useState({});
  const [groupAttendanceStats, setGroupAttendanceStats] = useState({});
  const [totalAttendance, setTotalAttendance] = useState({ totalPresent: 0, totalStudents: 0 });

  useEffect(() => {
    fetchLessonData();
  }, [lessonId]);

  const fetchLessonData = async () => {
    try {
      const response = await api.get(`/lessons/${lessonId}`);
      setLessonData(response.data);
      
      // Инициализируем состояния для каждой группы
      const groupStates = {};
      const originalStates = {};
      const stats = {};
      let totalPresent = 0;
      let totalStudents = 0;
      
      response.data.groups.forEach(group => {
        if (group.attendances && group.attendances.length > 0) {
          groupStates[group.id] = [...group.attendances];
          originalStates[group.id] = JSON.parse(JSON.stringify(group.attendances));
          
          const present = group.attendances.filter(a => a.attendance.status === 0).length;
          stats[group.id] = { present, total: group.attendances.length };
          totalPresent += present;
          totalStudents += group.attendances.length;
        }
      });
      
      setGroupAttendances(groupStates);
      setOriginalAttendances(originalStates);
      setGroupAttendanceStats(stats);
      setTotalAttendance({ totalPresent, totalStudents });
    } catch (error) {
      console.error('Error fetching lesson data:', error);
      handleApiError(error, 'Не удалось загрузить данные урока');
    } finally {
      setLoading(false);
    }
  };

  const handleApiError = (error, defaultMessage) => {
    if (error.response?.data?.detail) {
      messageApi.error(error.response.data.detail);
    } else if (error.response?.status >= 500) {
      messageApi.error('Произошла ошибка, попробуйте позже');
    } else {
      messageApi.error(defaultMessage);
    }
  };

  const handleAttendanceChange = (groupId, studentIndex, status) => {
    const updatedAttendances = { ...groupAttendances };
    updatedAttendances[groupId][studentIndex].attendance.status = status;
    setGroupAttendances(updatedAttendances);
  };

  const handleMarkAll = (groupId) => {
    const groupAttendance = groupAttendances[groupId];
    const allMarked = groupAttendance.every(student => student.attendance.status === 0);
    const newStatus = allMarked ? 1 : 0;
    
    const updatedAttendances = { ...groupAttendances };
    updatedAttendances[groupId] = groupAttendance.map(student => ({
      ...student,
      attendance: {
        ...student.attendance,
        status: newStatus
      }
    }));
    
    setGroupAttendances(updatedAttendances);
  };

  const handleCancel = (groupId) => {
    const updatedAttendances = { ...groupAttendances };
    updatedAttendances[groupId] = JSON.parse(JSON.stringify(originalAttendances[groupId]));
    setGroupAttendances(updatedAttendances);
  };

  const handleSaveAttendance = async (groupId) => {
    setSaving(true);
    try {
      const attendanceData = groupAttendances[groupId].map(student => ({
        student_id: student.student_id,
        attendance: {
          status: student.attendance.status
        }
      }));

      const response = await api.put(
        `/lessons/${lessonId}/groups/${groupId}/attendance/`,
        attendanceData
      );

      // Обновляем данные из ответа сервера
      const updatedAttendances = response.data.attendances;
      const studentMap = new Map(updatedAttendances.map(item => [item.student_id, item.attendance]));
      
      const newAttendances = groupAttendances[groupId].map(student => ({
        ...student,
        attendance: studentMap.get(student.student_id) || student.attendance
      }));
      
      const updatedGroupAttendances = { ...groupAttendances };
      updatedGroupAttendances[groupId] = newAttendances;
      setGroupAttendances(updatedGroupAttendances);
      
      const updatedOriginals = { ...originalAttendances };
      updatedOriginals[groupId] = JSON.parse(JSON.stringify(newAttendances));
      setOriginalAttendances(updatedOriginals);

      // Обновляем статистику посещаемости для этой группы
      const present = newAttendances.filter(a => a.attendance.status === 0).length;
      const updatedStats = { ...groupAttendanceStats };
      updatedStats[groupId] = { present, total: newAttendances.length };
      setGroupAttendanceStats(updatedStats);

      // Пересчитываем общую посещаемость
      let totalPresent = 0;
      let totalStudents = 0;
      Object.values(updatedStats).forEach(stat => {
        totalPresent += stat.present;
        totalStudents += stat.total;
      });
      setTotalAttendance({ totalPresent, totalStudents });

      // Обновляем статус текущего студента если он есть в ответе
      const currentStudent = lessonData?.schedule_data?.student_data;
      if (currentStudent) {
        const updatedStudentAttendance = studentMap.get(currentStudent.student_id);
        if (updatedStudentAttendance) {
          const updatedLessonData = { ...lessonData };
          updatedLessonData.schedule_data.student_data.attendance = updatedStudentAttendance;
          setLessonData(updatedLessonData);
        }
      }
      
      messageApi.success('Посещаемость успешно сохранена');
    } catch (error) {
      console.error('Error saving attendance:', error);
      handleApiError(error, 'Ошибка при сохранении посещаемости');
    } finally {
      setSaving(false);
    }
  };

  const handleGrantAccess = async (minutes = null, groupId = null) => {
    try {
      const url = groupId 
        ? `/lessons/${lessonId}/groups/${groupId}/attendance-permissions`
        : `/lessons/${lessonId}/attendance-permissions`;
      
      const method = groupId ? 'PATCH' : 'PUT';
      
      await api({
        method,
        url,
        data: { number_of_minutes_of_access: minutes }
      });
      
      messageApi.success(minutes === null ? 'Доступ отозван' : `Доступ выдан на ${minutes} минут`);
      fetchLessonData(); // Перезагружаем данные для обновления статусов доступа
    } catch (error) {
      console.error('Error granting access:', error);
      handleApiError(error, 'Ошибка при выдаче доступа');
    }
  };

  const isTeacher = !lessonData?.schedule_data?.student_data;
  const currentStudent = lessonData?.schedule_data?.student_data;
  const isCurrentStudentPrefect = currentStudent?.is_prefect;
  const studentGroupId = currentStudent?.group_id;

  // Для студента показываем только его группу
  const displayGroups = isTeacher 
    ? lessonData?.groups || [] 
    : lessonData?.groups.filter(group => group.id === studentGroupId) || [];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Spin size="large" />
      </div>
    );
  }

  if (!lessonData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card>
          <p>Урок не найден</p>
        </Card>
      </div>
    );
  }

  const { schedule_data } = lessonData;

  // Создаем колонки для таблицы
  const getAttendanceColumns = (groupId) => [
    {
      title: 'Студент',
      dataIndex: 'full_name',
      key: 'full_name',
      align: 'center',
      render: (text, record) => (
        <div className="flex items-center justify-center">
          <UserOutlined className="text-gray-400 mr-2" />
          <Tooltip title={`Персональный номер: ${record.personal_number}`}>
            <span className={record.is_prefect ? 'underline font-semibold' : ''}>
              {text}
            </span>
          </Tooltip>
        </div>
      ),
    },
    {
      title: 'Статус',
      dataIndex: 'attendance',
      key: 'attendance',
      align: 'center',
      render: (attendance, record, index) => {
        const isDisabled = attendance.status === 2;
        const group = displayGroups.find(g => g.id === groupId);
        const canEdit = isTeacher || (group?.can_be_edited_by_prefect && isCurrentStudentPrefect);
        
        return (
          <Radio.Group
            value={attendance.status}
            onChange={(e) => handleAttendanceChange(groupId, index, e.target.value)}
            disabled={!canEdit || isDisabled}
            size="large"
          >
            <Radio.Button value={0}>+</Radio.Button>
            <Radio.Button value={1}>Н</Radio.Button>
            <Tooltip title="Регулируется только учебным отделом">
              <Radio.Button value={2} disabled>У</Radio.Button>
            </Tooltip>
          </Radio.Group>
        );
      },
    },
  ];

  // Создаем items для Collapse (новый API)
  const collapseItems = displayGroups.map(group => {
    const attendance = groupAttendanceStats[group.id] || { present: 0, total: 0 };
    const canEdit = group.can_be_edited_by_prefect;
    const hasAttendances = groupAttendances[group.id]?.length > 0;
    
    return {
      key: group.id,
      label: (
        <div className="flex justify-between items-center">
          <span>{group.complete_name}</span>
          {hasAttendances && (
            <span className="text-gray-600">
              отмечено <span className="text-blue-500 font-medium">{attendance.present}</span> из {attendance.total}
            </span>
          )}
        </div>
      ),
      children: hasAttendances ? (
        <>
          {/* Кнопки управления доступом для преподавателя */}
          {isTeacher && (
            <div className="mb-4">
              <Alert
                message="Управление доступом для старост"
                type="info"
                className="mb-2"
              />
              <div className="mt-1 flex gap-2">
                {canEdit ? (
                  <Button 
                    size="small" 
                    danger 
                    onClick={() => handleGrantAccess(null, group.id)}
                  >
                    Отозвать доступ
                  </Button>
                ) : (
                  <>
                    <Button 
                      size="small" 
                      onClick={() => handleGrantAccess(5, group.id)}
                    >
                      Выдать на 5 минут
                    </Button>
                    <Button 
                      size="small" 
                      onClick={() => handleGrantAccess(10, group.id)}
                    >
                      Выдать на 10 минут
                    </Button>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Сообщение о доступе */}
          {!isTeacher && isCurrentStudentPrefect && !canEdit && (
            <Alert
              message="Для получения доступа к изменению статусов обратитесь к преподавателю"
              type="warning"
              className="mb-4 text-center"
            />
          )}
          {!isTeacher && !isCurrentStudentPrefect && (
            <Alert
              message="Только староста может отмечать студентов"
              type="error"
              className="mb-4 text-center"
            />
          )}

          {/* Кнопки управления для старосты с доступом */}
          {(isTeacher || (isCurrentStudentPrefect && canEdit)) && (
            <div className="flex gap-2 mb-4">
              <Button 
                size="large"
                onClick={() => handleMarkAll(group.id)}
                style={{ flex: 1 }}
              >
                Отметить всех
              </Button>
              <Button 
                size="large"
                style={{ flex: 1 }}
              >
                Перейти к статистике журнала
              </Button>
            </div>
          )}

          {/* Таблица студентов */}
          <Table
            columns={getAttendanceColumns(group.id)}
            dataSource={groupAttendances[group.id]?.map((item, index) => ({
              ...item,
              key: item.student_id || index
            }))}
            pagination={false}
            size="middle"
          />

          {/* Кнопки сохранения для старосты с доступом */}
          {(isTeacher || (isCurrentStudentPrefect && canEdit)) && (
            <div className="flex gap-2 mt-4">
              <Button 
                size="large"
                onClick={() => handleCancel(group.id)}
                style={{ flex: 1 }}
              >
                Отменить
              </Button>
              <Button 
                type="primary" 
                size="large"
                loading={saving}
                onClick={() => handleSaveAttendance(group.id)}
                style={{ flex: 1 }}
              >
                Сохранить
              </Button>
            </div>
          )}
        </>
      ) : (
        !isTeacher && (
          <div className="text-gray-500 text-center py-4">
            Нет данных о посещаемости
          </div>
        )
      )
    };
  });

  return (
    <>
      {contextHolder}
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-6xl mx-auto">
          {/* Заголовок */}
          <Card className="mb-6 shadow-sm">
            <h1 className="text-2xl font-bold text-gray-800">
              {schedule_data.lesson.name}
            </h1>
          </Card>

          {/* Информация о занятии */}
          <Card title="Информация о занятии" className="mb-6 shadow-sm">
            <Descriptions column={2} size="middle">
              <Descriptions.Item label="Тип">
                <Tag color={getTypeColor(schedule_data.type_of_lesson)}>
                  {schedule_data.type_of_lesson}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Дата и время">
                <Tag>{`${schedule_data.date} ${schedule_data.time}`}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Аудитории">
                {schedule_data.audiences.map((audience, index) => (
                  <Tooltip key={index} title={audience.address.name}>
                    <Tag className="mb-1">{audience.name}</Tag>
                  </Tooltip>
                ))}
              </Descriptions.Item>
              <Descriptions.Item label="Преподаватели">
                {schedule_data.teachers.map(teacher => (
                  <Tooltip key={teacher.full_name} title={teacher.decryption_of_full_name}>
                    <Tag className="mb-1">{teacher.full_name}</Tag>
                  </Tooltip>
                ))}
              </Descriptions.Item>
              <Descriptions.Item label="Группы">
                {schedule_data.group_names.map((groupName, index) => (
                  <Tag key={index} className="mb-1">
                    {groupName}
                  </Tag>
                ))}
              </Descriptions.Item>
              {currentStudent && (
                <Descriptions.Item label="Статус">
                  <Tag color={getStatusColor(currentStudent.attendance.decryption)}>
                    {currentStudent.attendance.decryption}
                  </Tag>
                </Descriptions.Item>
              )}
            </Descriptions>
          </Card>

          {/* Общая статистика посещаемости */}
          {totalAttendance.totalStudents > 0 && (
            <Alert
              message={`Общая посещаемость: ${totalAttendance.totalPresent} из ${totalAttendance.totalStudents} (${Math.round((totalAttendance.totalPresent / totalAttendance.totalStudents) * 100)}%)`}
              type="success"
              className="mb-6 text-center min-h-20"
            />
          )}

          {/* Кнопки выдачи доступа для преподавателя */}
          {isTeacher && (
            <div className="mb-6 mt-3">
              <Alert
                message="Управление доступом для старост"
                type="info"
                className="mb-3 mt-2"
              />
              <div className="mt-1 flex gap-2">
                {schedule_data.can_be_edited_by_prefect ? (
                  <>
                    <Button onClick={() => handleGrantAccess(5)}>
                      Выдать доступ всем на 5 минут
                    </Button>
                    <Button onClick={() => handleGrantAccess(10)}>
                      Выдать доступ всем на 10 минут
                    </Button>
                    <Button danger onClick={() => handleGrantAccess(null)}>
                      Отозвать доступ у всех
                    </Button>
                  </>
                ) : (
                  <>
                    <Button onClick={() => handleGrantAccess(5)}>
                      Выдать доступ всем на 5 минут
                    </Button>
                    <Button onClick={() => handleGrantAccess(10)}>
                      Выдать доступ всем на 10 минут
                    </Button>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Посещения по группам */}
          <Card title="Посещения по группам" className="shadow-sm">
            <Collapse items={collapseItems} />
          </Card>
        </div>
      </div>
    </>
  );
}