import React, { useState, useEffect } from "react";
import { Calendar, Card, Tag, List, ConfigProvider, Spin, Tooltip } from "antd";
import { useNavigate, useLocation } from "react-router-dom";
import dayjs from "dayjs";
import "dayjs/locale/ru";
import ru_RU from "antd/locale/ru_RU";
import axios from "axios";

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

  const handleLessonClick = (lessonId) => {
    navigate(`/lessons/${lessonId}`);
  };

  const getTypeColor = (type) => {
    switch (type) {
      case "ЛK":
        return "geekblue";
      case "ПР":
        return "cyan";
      case "ЛАБ":
        return "magenta";
      default:
        return "gray";
    }
  };

  const getTypeText = (type) => {
    switch (type) {
      case "ЛK":
        return "Лекция";
      case "ПР":
        return "Практика";
      case "ЛАБ":
        return "Лабораторная";
      default:
        return type;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "Н":
        return "red";
      case "+":
        return "green";
      case "У":
        return "gray";
      default:
        return "red";
    }
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
                          className="w-full cursor-pointer hover:shadow-md transition-shadow"
                          onClick={() => handleLessonClick(lesson.lesson.id)}
                        >
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center gap-2">
                              <Tag color={getTypeColor(lesson.type_of_lesson)}>
                                {getTypeText(lesson.type_of_lesson)}
                              </Tag>
                              <Tag
                                color={getStatusColor(
                                  lesson.attendance.decryption
                                )}
                              >
                                {lesson.attendance.decryption}
                              </Tag>
                            </div>
                            <span className="text-gray-600 font-medium">
                              {lesson.time}
                            </span>
                          </div>

                          <h4 className="font-semibold text-lg mb-2">
                            {lesson.lesson.name}
                          </h4>

                          <div className="flex justify-between text-gray-600">
                            <div>
                              <Tooltip
                                placement="top"
                                title={lesson.audience.address.name}
                              >
                                <span className="font-medium">Аудитория: </span>
                                {lesson.audience.name}
                              </Tooltip>
                            </div>
                            <div>
                              <span className="font-medium">
                                Преподаватели:{" "}
                              </span>
                              {lesson.teachers
                                .map((t) => t.full_name)
                                .join(", ")}
                            </div>
                          </div>
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
