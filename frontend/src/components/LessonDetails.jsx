import React, { useState, useEffect } from 'react';
import { Card, Descriptions, Radio, Tag, Alert, Button, Spin, message } from 'antd';
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
  const [saving, setSaving] = useState(false);
  const [isPerfect, setIsPerfect] = useState(false);

  useEffect(() => {
    fetchLessonData();
  }, [lessonId]);

  const fetchLessonData = async () => {
    try {
      const response = await api.get(`/lessons/${lessonId}`);
      setLessonData(response.data);
      setAttendances(response.data.attendances);
      setIsPerfect(response.data.is_prefect);
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

  const handleSaveAttendance = async () => {
    setSaving(true);
    try {
      const attendanceData = attendances.map(student => ({
        student_id: student.student_id,
        attendance: {
          status: student.attendance.status
        }
      }));

      await api.post(`/lessons/${lessonId}/mark-attendance/`, attendanceData);
      message.success('Посещаемость успешно сохранена');
    } catch (error) {
      console.error('Error saving attendance:', error);
      message.error('Ошибка при сохранении посещаемости');
    } finally {
      setSaving(false);
    }
  };

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

  const { schedule_data, group } = lessonData;

  return (
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
            <Descriptions.Item label="Дата">
              {schedule_data.time}
            </Descriptions.Item>
            <Descriptions.Item label="Аудитория">
              {schedule_data.audience.name}
            </Descriptions.Item>
            <Descriptions.Item label="Преподаватель">
              {schedule_data.teachers.map(t => t.full_name).join(', ')}
            </Descriptions.Item>
            <Descriptions.Item label="Статус">
              <Tag color={getStatusColor(schedule_data.my_attendance.decryption)}>
                {schedule_data.my_attendance.decryption}
              </Tag>
            </Descriptions.Item>
          </Descriptions>
        </Card>

        {/* Посещения */}
        <Card 
          title={`Посещения группы ${group.complete_name}`}
          className="shadow-sm"
        >
          {/* Статистика и кнопки */}
          <div className="flex justify-between items-center mb-6">
            <div className="text-lg font-medium">
              Отмечено {attendances.filter(a => a.attendance.status === 0).length} из {attendances.length}
            </div>
            <div className="flex gap-2">
              <Button disabled={!canEdit} size="large">
                Отметить всех
              </Button>
              <Button size="large">
                Перейти к статистике журнала
              </Button>
            </div>
          </div>

          {/* Предупреждение */}
          {!canEdit && (
            <Alert
              message="Только староста может отмечать студентов"
              type="warning"
              className="mb-6 text-center"
            />
          )}

          {/* Список студентов */}
          <div className="space-y-4">
            {attendances.map((student, index) => (
              <div
                key={index}
                className={`flex items-center justify-between p-4 border rounded-lg transition-all duration-200 hover:shadow-md hover:border-blue-300 ${
                  student.is_prefect ? 'border-blue-300 bg-blue-50' : 'bg-white'
                }`}
              >
                <div className="flex items-center flex-1">
                  <UserOutlined className="text-gray-400 mr-3 text-lg" />
                  <span
                    className={`text-lg ${student.is_prefect ? 'underline font-semibold' : ''}`}
                  >
                    {student.full_name}
                  </span>
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

          {/* Кнопка сохранения для старосты */}
          {canEdit && (
            <div className="flex justify-end mt-6">
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
  );
}