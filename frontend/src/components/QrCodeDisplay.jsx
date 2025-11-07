// src/components/QrCodeDisplay.jsx
import React, { useState, useEffect, useRef } from 'react';
import { Modal, Alert, Spin, Button, QRCode, Tag } from 'antd';
import { QrcodeOutlined, UserOutlined, CloseOutlined } from '@ant-design/icons';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
});

export default function QrCodeDisplay({ lessonId, isOpen, onClose }) {
  const [qrData, setQrData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [attendanceStats, setAttendanceStats] = useState({ present: 0, total: 0 });
  const [timeLeft, setTimeLeft] = useState(5);
  const [currentQrUrl, setCurrentQrUrl] = useState('');
  const qrCodeRef = useRef(null);

  const fetchQrData = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/lessons/${lessonId}/qr-code/`);
      // Сначала обновляем данные
      setQrData(response.data);
      setCurrentQrUrl(response.data.qr_url);
      setAttendanceStats({
        present: response.data.total_attendance.present_students,
        total: response.data.total_attendance.total_students
      });
      setTimeLeft(5);
    } catch (error) {
      console.error('Error fetching QR data:', error);
    } finally {
      // Задержка для плавности
      setTimeout(() => {
        setLoading(false);
      }, 300);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchQrData();
      
      const countdown = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            fetchQrData();
            return 5;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(countdown);
    }
  }, [isOpen, lessonId]);

  return (
    <Modal
      title={
        <div className="flex items-center gap-2">
          <QrcodeOutlined />
          QR код для отметки посещаемости
        </div>
      }
      open={isOpen}
      onCancel={onClose}
      width={520}
      styles={{
        body: {
          padding: '24px',
          maxHeight: '70vh',
        }
      }}
      style={{
        top: '5vh',
      }}
      footer={[
        <Button 
          key="close" 
          danger 
          icon={<CloseOutlined />}
          onClick={onClose}
          size="large"
        >
          Закрыть
        </Button>
      ]}
      maskClosable={false}
    >
      <div className="text-center">
        {/* Статистика посещаемости */}
        <div className="mb-4">
          <Tag 
            icon={<UserOutlined />} 
            color="blue" 
            style={{ 
              fontSize: '16px', 
              padding: '8px 16px',
            }}
          >
            Отмечено: <strong>{attendanceStats.present}</strong> / {attendanceStats.total}
          </Tag>
        </div>

        {/* Таймер автообновления */}
        <div className="mb-6 text-sm text-gray-500">
          Автообновление через: <strong>{timeLeft} секунд</strong>
        </div>

        {/* Контейнер для QR кода */}
        <div 
          ref={qrCodeRef}
          className="flex justify-center items-center min-h-[260px] mb-4 transition-all duration-300 ease-in-out"
          style={{
            opacity: loading ? 0.6 : 1,
          }}
        >
          {loading ? (
            <div className="flex flex-col items-center">
              <Spin size="large" />
              <div className="mt-4 text-gray-500">Обновление QR кода...</div>
            </div>
          ) : (
            currentQrUrl && (
              <QRCode 
                value={currentQrUrl} 
                size={260}
                errorLevel="M"
                status="active"
              />
            )
          )}
        </div>

        {/* Сообщение */}
        {!loading && (
          <div className="mt-2">
            <Alert 
              message="Сканируйте QR код для отметки посещаемости" 
              type="info" 
              showIcon 
            />
          </div>
        )}
      </div>
    </Modal>
  );
}