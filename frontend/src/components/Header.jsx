// src/components/Header.js
import React from 'react';
import { Button, Space } from 'antd';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Мое SPA</h1>
        <Space>
          {user ? (
            <>
              <span>Привет, {user.full_name}</span>
              <Button type="default" onClick={handleLogout}>
                Выйти
              </Button>
            </>
          ) : (
            <Button type="default" onClick={handleLoginClick}>
              Вход
            </Button>
          )}
        </Space>
      </div>
    </header>
  );
}