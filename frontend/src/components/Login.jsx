// src/components/Login.js
import React from "react";
import { Form, Input, Button, Card } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import axios from "axios";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

// Создаем экземпляр для логина тоже с withCredentials
const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  withCredentials: true,
});

export default function LoginForm() {
  const [loading, setLoading] = React.useState(false);
  const { login, user } = useAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const response = await api.post("/users/sign-in/", values);
      login(response.data);

    } catch (error) {
      console.error("Login error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card title="Вход" style={{ width: 400 }}>
        <Form onFinish={onFinish} layout="vertical">
          <Form.Item
            name="email"
            rules={[
              { required: true, message: "Введите email" },
              { type: "email", message: "Неверный формат email" },
            ]}
          >
            <Input prefix={<UserOutlined />} placeholder="Email" size="large" />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: "Введите пароль" }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Пароль"
              size="large"
            />
          </Form.Item>

          <Button
            type="primary"
            htmlType="submit"
            loading={loading}
            className="w-full"
            size="large"
          >
            Войти
          </Button>
        </Form>
      </Card>
    </div>
  );
}
