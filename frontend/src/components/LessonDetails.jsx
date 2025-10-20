import React, { useState, useEffect } from 'react';
import { Card, Descriptions, Radio, Tag, Alert, Button, Spin, message, Tooltip } from 'antd';
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
  const [attendances, setAttendances] = useState([]);
  const [originalAttendances, setOriginalAttendances] = useState([]); // Сохраняем исходные данные
  const [saving, setSaving] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();
  const [markedCount, setMarkedCount] = useState(0);

  useEffect(() => {
    fetchLessonData();
  }, [lessonId]);

  const fetchLessonData = async () => {
    try {
      const response = await api.get(`/lessons/${lessonId}`);
      setLessonData(response.data);
      
      // Находим группу, где id совпадает с student_data.group_id и attendances не пустой
      const studentGroupId = response.data.schedule_data.student_data.group_id;
      const targetGroup = response.data.groups.find(group => 
        group.id === studentGroupId && group.attendances && group.attendances.length > 0
      );
      
      const groupAttendances = targetGroup ? targetGroup.attendances : [];
      setAttendances(groupAttendances);
      setOriginalAttendances(JSON.parse(JSON.stringify(groupAttendances))); // Сохраняем копию исходных данных
      setMarkedCount(groupAttendances.filter(a => a.attendance.status === 0).length);
    } catch (error) {
      console.error('Error fetching lesson data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAttendanceChange = (studentIndex, status) => {
    const updatedAttendances = [...attendances];
    updatedAttendances[studentIndex].attendance.status = status;
    setAttendances(updatedAttendances);
  };

  const handleMarkAll = () => {
    const allMarked = attendances.every(student => student.attendance.status === 0);
    const newStatus = allMarked ? 1 : 0; // Если все +, то ставим Н, иначе +
    
    const updatedAttendances = attendances.map(student => ({
      ...student,
      attendance: {
        ...student.attendance,
        status: newStatus
      }
    }));
    
    setAttendances(updatedAttendances);
  };

  const handleCancel = () => {
    // Сбрасываем к исходным данным
    setAttendances(JSON.parse(JSON.stringify(originalAttendances)));
  };

  const handleSaveAttendance = async () => {
    setSaving(true);
    try {
      const attendanceData = attendances.map(student => ({
        student_id: student.student_id,
        attendance: {
          status: student.attendance.status
        }
      }));

      const studentGroupId = lessonData.schedule_data.student_data.group_id;
      const response = await api.put(
        `/lessons/${lessonId}/groups/${studentGroupId}/attendance/`,
        attendanceData
      );

      // Обновляем данные из ответа сервера
      const updatedAttendances = response.data.attendances;
      const studentMap = new Map(updatedAttendances.map(item => [item.student_id, item.attendance]));
      
      const newAttendances = attendances.map(student => ({
        ...student,
        attendance: studentMap.get(student.student_id) || student.attendance
      }));
      
      setAttendances(newAttendances);
      setOriginalAttendances(JSON.parse(JSON.stringify(newAttendances))); // Обновляем исходные данные
      setMarkedCount(newAttendances.filter(a => a.attendance.status === 0).length);
      
      messageApi.success('Посещаемость успешно сохранена');
    } catch (error) {
      console.error('Error saving attendance:', error);
      messageApi.error('Ошибка при сохранении посещаемости');
    } finally {
      setSaving(false);
    }
  };

  // Проверяем является ли пользователь старостой
  const isPerfect = lessonData?.schedule_data?.student_data?.is_prefect || false;
  const canEdit = isPerfect;

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

  const { schedule_data, groups } = lessonData;
  const targetGroup = groups.find(g => g.id === schedule_data.student_data.group_id);

  return (
    <>
      {contextHolder}
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
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
                {schedule_data.time}
              </Descriptions.Item>
              <Descriptions.Item label="Аудитория">
                <Tooltip title={schedule_data.audience.address.name}>
                  <Tag>{schedule_data.audience.name}</Tag>
                </Tooltip>
              </Descriptions.Item>
              <Descriptions.Item label="Преподаватели">
                {schedule_data.teachers.map(teacher => (
                  <Tooltip key={teacher.full_name} title={teacher.decryption_of_full_name}>
                    <Tag className="mb-1">{teacher.full_name}</Tag>
                  </Tooltip>
                ))}
              </Descriptions.Item>
              <Descriptions.Item label="Группы">
                {groups.map(group => (
                  <Tag key={group.id} className="mb-1">
                    {group.complete_name}
                  </Tag>
                ))}
              </Descriptions.Item>
              <Descriptions.Item label="Статус">
                <Tag color={getStatusColor(schedule_data.student_data.attendance.decryption)}>
                  {schedule_data.student_data.attendance.decryption}
                </Tag>
              </Descriptions.Item>
            </Descriptions>
          </Card>

          {/* Посещения */}
          <Card 
            title={`Посещения группы ${targetGroup?.complete_name || 'Не указана'}`}
            className="shadow-sm"
          >
            {/* Статистика и кнопки (только для старосты) */}
            {canEdit && (
              <div className="flex justify-between items-center mb-6">
                <div className="text-lg font-medium">
                  Отмечено {markedCount} из {attendances.length}
                </div>
                <div className="flex gap-2">
                  <Button 
                    size="large"
                    onClick={handleMarkAll}
                  >
                    Отметить всех
                  </Button>
                  <Button size="large">
                    Перейти к статистике журнала
                  </Button>
                </div>
              </div>
            )}

            {/* Предупреждение для не-старосты */}
            {!canEdit && (
              <Alert
                message="Только староста может отмечать студентов"
                type="error"
                className="mb-4 text-center"
              />
            )}

            {/* Список студентов */}
            <div className="space-y-4 mt-4">
              {attendances.map((student, index) => (
                <div
                  key={index}
                  className={`flex items-center justify-between p-4 border rounded-lg transition-all duration-200 hover:shadow-md hover:border-blue-300 ${
                    student.is_prefect ? 'border-blue-300 bg-blue-50' : 'bg-white'
                  }`}
                >
                  <div className="flex items-center flex-1">
                    <UserOutlined className="text-gray-400 mr-3 text-lg" />
                    <Tooltip title={`Персональный номер: ${student.personal_number}`}>
                      <span
                        className={`text-lg ${student.is_prefect ? 'underline font-semibold' : ''}`}
                      >
                        {student.full_name}
                      </span>
                    </Tooltip>
                  </div>
                  
                  <Radio.Group
                    value={student.attendance.status}
                    onChange={(e) => handleAttendanceChange(index, e.target.value)}
                    disabled={!canEdit}
                    size="large"
                  >
                    <Radio.Button value={0} className="px-6 py-2">+</Radio.Button>
                    <Radio.Button value={1} className="px-6 py-2">Н</Radio.Button>
                    <Radio.Button value={2} className="px-6 py-2">У</Radio.Button>
                  </Radio.Group>
                </div>
              ))}
            </div>

            {/* Кнопки сохранения и отмены для старосты */}
            {canEdit && (
              <div className="flex justify-end gap-2 mt-6">
                <Button 
                  size="large"
                  onClick={handleCancel}
                >
                  Отменить
                </Button>
                <Button 
                  type="primary" 
                  size="large" 
                  loading={saving}
                  onClick={handleSaveAttendance}
                >
                  Сохранить
                </Button>
              </div>
            )}
          </Card>
        </div>
      </div>
    </>
  );
}