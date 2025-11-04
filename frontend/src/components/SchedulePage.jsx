import React, { useState, useEffect } from "react";
import { Calendar, Card, Tag, List, ConfigProvider, Spin, Tooltip, Progress, Button } from "antd";
import { useNavigate, useLocation } from "react-router-dom";
import dayjs from "dayjs";
import "dayjs/locale/ru";
import ru_RU from "antd/locale/ru_RU";
import axios from "axios";
import { getTypeColor, getStatusColor } from '../utils/constants';

dayjs.locale("ru");

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  withCredentials: true,
});

export default function SchedulePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [selectedDate, setSelectedDate] = useState(dayjs());
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [studyDays, setStudyDays] = useState([]);

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const dateParam = searchParams.get("date");

    if (dateParam) {
      setSelectedDate(dayjs(dateParam));
    } else {
      const today = dayjs();
      setSelectedDate(today);
      navigate(`?date=${today.format("YYYY-MM-DD")}`, { replace: true });
    }
  }, [location.search, navigate]);

  useEffect(() => {
    if (selectedDate) {
      fetchLessons(selectedDate);
      fetchStudyDays(selectedDate.year(), selectedDate.month() + 1);
    }
  }, [selectedDate]);

  const fetchStudyDays = async (year, month) => {
    try {
      const response = await api.get(
        `/lessons/study-days/?year=${year}&month=${month}`
      );
      setStudyDays(response.data.dates || []);
    } catch (error) {
      console.error("Error fetching study days:", error);
      setStudyDays([]);
    }
  };

  const fetchLessons = async (date) => {
    setLoading(true);
    try {
      const dateStr = date.format("YYYY-MM-DD");
      const response = await api.get(`/lessons?date=${dateStr}`);
      setLessons(response.data.lessons || []);
    } catch (error) {
      console.error("Error fetching lessons:", error);
      setLessons([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDateSelect = (date) => {
    setSelectedDate(date);
    navigate(`?date=${date.format("YYYY-MM-DD")}`);
  };

  const handlePanelChange = (date) => {
    fetchStudyDays(date.year(), date.month() + 1);
  };

  const handleLessonClick = (lessonId, e) => {
    // Предотвращаем всплытие события если кликнули по кнопке
    if (e && e.target.closest('button')) {
      return;
    }
    navigate(`/lessons/${lessonId}`);
  };

  const renderGroupTags = (groupNames) => {
    if (!groupNames || groupNames.length === 0) return null;
    
    const visibleGroups = groupNames.slice(0, 5);
    const hiddenGroupsCount = groupNames.length - 5;

    return (
      <>
        {visibleGroups.map((groupName, index) => (
          <Tag key={index} className="mb-1">
            {groupName}
          </Tag>
        ))}
        {hiddenGroupsCount > 0 && (
          <Tooltip title={groupNames.slice(5).join(', ')}>
            <Tag className="mb-1">
              +{hiddenGroupsCount}...
            </Tag>
          </Tooltip>
        )}
      </>
    );
  };

  const dateFullCellRender = (date) => {
    const dateStr = date.format("YYYY-MM-DD");
    const hasLessons = studyDays.includes(dateStr);

    return (
      <div className="ant-picker-cell-inner flex flex-col items-center justify-center h-12">
        <div>{date.date()}</div>
        {hasLessons && (
          <div className="w-2 h-2 bg-blue-500 rounded-full mt-1"></div>
        )}
      </div>
    );
  };

  return (
    <ConfigProvider locale={ru_RU}>
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-1">
              <Card title="Календарь" className="shadow-sm">
                <Calendar
                  fullscreen={false}
                  onSelect={handleDateSelect}
                  value={selectedDate}
                  fullCellRender={dateFullCellRender}
                  onPanelChange={handlePanelChange}
                />
              </Card>
            </div>

            <div className="lg:col-span-2">
              <Card
                title={`Пары на ${selectedDate.format("DD.MM.YYYY")}`}
                className="shadow-sm transition-all duration-300 min-h-[200px]"
              >
                <Spin spinning={loading} size="large">
                  <List
                    dataSource={lessons}
                    renderItem={(lesson) => (
                      <List.Item>
                        <Card
                          size="small"
                          className="w-full hover:shadow-md transition-shadow cursor-pointer"
                          onClick={(e) => handleLessonClick(lesson.id, e)}
                        >
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center gap-2">
                              <Tag color={getTypeColor(lesson.type_of_lesson)}>
                                {lesson.type_of_lesson}
                              </Tag>
                              {lesson.student_data && (
                                <Tag
                                  color={getStatusColor(
                                    lesson.student_data.attendance.decryption
                                  )}
                                >
                                  {lesson.student_data.attendance.decryption}
                                </Tag>
                              )}
                              {lesson.can_be_edited_by_prefect && (
                                <Tag color="orange">открыто старосте</Tag>
                              )}
                            </div>
                            <span className="text-gray-600 font-medium">
                              {lesson.time}
                            </span>
                          </div>

                          <h4 className="font-semibold text-lg mb-2">
                            {lesson.lesson.name}
                          </h4>

                          <div className="flex justify-between items-center mb-3">
                            <div className="flex-1">
                              <div className="text-gray-600 mb-1">
                                <span className="font-medium">Аудитории: </span>
                                {lesson.audiences.map((audience, index) => (
                                  <Tooltip
                                    key={index}
                                    placement="top"
                                    title={audience.address.name}
                                  >
                                    <Tag className="mr-1 mb-1">
                                      {audience.name}
                                    </Tag>
                                  </Tooltip>
                                ))}
                              </div>
                              <div className="text-gray-600">
                                <span className="font-medium">Преподаватели: </span>
                                {lesson.teachers.map((teacher, index) => (
                                  <Tooltip
                                    key={index}
                                    title={teacher.decryption_of_full_name}
                                  >
                                    <Tag className="mr-1 mb-1">
                                      {teacher.full_name}
                                    </Tag>
                                  </Tooltip>
                                ))}
                              </div>
                              {lesson.group_names && lesson.group_names.length > 0 && (
                                <div className="text-gray-600 mt-1">
                                  <span className="font-medium">Группы: </span>
                                  {renderGroupTags(lesson.group_names)}
                                </div>
                              )}
                            </div>
                            
                            <Button 
                              type="primary" 
                              size="small"
                              onClick={() => handleLessonClick(lesson.id)}
                            >
                              Подробности
                            </Button>
                          </div>

                          {lesson.total_attendance && (
                            <div className="border-t pt-3">
                              <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-600">
                                  Посещаемость: {lesson.total_attendance.present_students} из {lesson.total_attendance.total_students}
                                </span>
                                <Progress 
                                  percent={Math.round((lesson.total_attendance.present_students / lesson.total_attendance.total_students) * 100)}
                                  size="small" 
                                  style={{ width: 100 }}
                                />
                              </div>
                            </div>
                          )}
                        </Card>
                      </List.Item>
                    )}
                    locale={{ emptyText: "Пар на выбранную дату нет" }}
                  />
                </Spin>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </ConfigProvider>
  );
}