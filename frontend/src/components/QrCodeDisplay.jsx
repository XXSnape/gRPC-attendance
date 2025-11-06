// src/components/QrCodeDisplay.jsx
import React, { useState, useEffect } from 'react';
import { Modal, Alert, Spin, Button, QRCode, Tag } from 'antd';
import { QrcodeOutlined, ReloadOutlined, UserOutlined } from '@ant-design/icons';
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

  const fetchQrData = async () => {
    setLoading(true);
    try {
      // Временная заглушка
      const qrUrl = `${window.location.origin}/self-approve/${lessonId}`;
      setQrData({ qr_url: qrUrl });
      
      // Получаем статистику посещаемости
      const statsResponse = await api.get(`/lessons/${lessonId}`);
      const groups = statsResponse.data.groups || [];
      let totalPresent = 0;
      let totalStudents = 0;
      
      groups.forEach(group => {
        if (group.attendances && group.attendances.length > 0) {
          totalPresent += group.attendances.filter(a => a.attendance.status === 0).length;
          totalStudents += group.attendances.length;
        }
      });
      
      setAttendanceStats({ present: totalPresent, total: totalStudents });
      setTimeLeft(5);
    } catch (error) {
      console.error('Error fetching QR data:', error);
    } finally {
      setLoading(false);
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

  const handleManualRefresh = () => {
    fetchQrData();
  };

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
      width={500}
      footer={[
        <Button key="refresh" icon={<ReloadOutlined />} onClick={handleManualRefresh}>
          Обновить ({timeLeft}с)
        </Button>,
        <Button key="close" onClick={onClose}>
          Закрыть
        </Button>
      ]}
    >
      <div className="text-center">
        <div className="mb-6">
          <Tag icon={<UserOutlined />} color="blue" style={{ fontSize: '16px', padding: '8px 16px' }}>
            Отмечено: <strong>{attendanceStats.present}</strong> / {attendanceStats.total}
          </Tag>
        </div>

        {loading ? (
          <div className="py-12">
            <Spin size="large" />
            <div className="mt-4 text-gray-500">Загрузка QR кода...</div>
          </div>
        ) : qrData ? (
          <div className="space-y-4">
            <div className="flex justify-center">
              <QRCode 
                value={qrData.qr_url} 
                size={280}
                errorLevel="M"
                status={loading ? "loading" : "active"}
              />
            </div>
            
            <Alert 
              message="Сканируйте QR код для отметки посещаемости" 
              type="info" 
              showIcon 
            />
            
            <div className="text-sm text-gray-500">
              QR код обновится автоматически через: <strong>{timeLeft} секунд</strong>
            </div>
          </div>
        ) : (
          <Alert 
            message="Не удалось загрузить QR код" 
            description="Попробуйте обновить страницу" 
            type="error" 
            showIcon 
          />
        )}
      </div>
    </Modal>
  );
}