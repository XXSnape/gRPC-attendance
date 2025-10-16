// src/components/Dashboard.js
import React from 'react';
import { Card, Alert, Spin } from 'antd';
import { useAuth } from './AuthContext';
import { Navigate } from 'react-router-dom';

export default function Dashboard() {
  const { user, loading } = useAuth();

  // Показываем спиннер во время загрузки
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <div className="container mx-auto flex justify-center">
          <Spin size="large" />
        </div>
      </div>
    );
  }

  // Если не авторизован, перенаправляем на логин
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="container mx-auto">
        <Card title="Главная страница">
          <Alert
            message={`Добро пожаловать, ${user.full_name}!`}
            description="Вы успешно авторизовались в системе."
            type="success"
            showIcon
          />
        </Card>
      </div>
    </div>
  );
}