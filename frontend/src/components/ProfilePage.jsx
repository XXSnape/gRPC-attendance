// src/components/ProfilePage.jsx
import React from 'react';
import { Card, Button, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [loading, setLoading] = React.useState(false);
  const [messageApi, contextHolder] = message.useMessage();

  const handleLogout = async () => {
    setLoading(true);
    try {
      await logout(); // Просто вызываем logout из контекста
      messageApi.success('Вы успешно вышли из аккаунта');
      navigate('/login');
    } catch (error) {
      console.error('Logout error:', error);
      messageApi.error('Ошибка при выходе из аккаунта');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {contextHolder}
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-md mx-auto">
          <Card title="Профиль" className="shadow-sm">
            <div className="text-center">
              <Button
                type="primary"
                danger
                size="large"
                loading={loading}
                onClick={handleLogout}
              >
                Выйти из аккаунта
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </>
  );
}