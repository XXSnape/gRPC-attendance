# 📚 Электронный журнал (на данный момент на начальной стадии разработки)

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&style=for-the-badge)](https://www.python.org/)
[![UV](https://img.shields.io/badge/uv-0.1%2B-FF6B35?logo=python&style=for-the-badge)](https://github.com/astral-sh/uv)
[![gRPC](https://img.shields.io/badge/gRPC-1.50%2B-4B8BBE?logo=google&style=for-the-badge)](https://grpc.io/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.100%2B-009688?logo=fastapi&style=for-the-badge)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-D71F00?logo=sqlalchemy&style=for-the-badge)](https://www.sqlalchemy.org/)
[![Beanie](https://img.shields.io/badge/beanie-1.20%2B-00AA00?logo=mongodb&style=for-the-badge)](https://beanie-odm.dev/)
[![Argon2](https://img.shields.io/badge/argon2-23.1%2B-8A2BE2?logo=keybase&style=for-the-badge)](https://argon2.online/)
[![SQLAdmin](https://img.shields.io/badge/sqladmin-1.10%2B-FF6B35?logo=sqlalchemy&style=for-the-badge)](https://aminalaee.dev/sqladmin/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&style=for-the-badge)](https://github.com/psf/black)
[![Ant Design](https://img.shields.io/badge/ant--design-5.0%2B-0170FE?logo=antdesign&style=for-the-badge)](https://ant.design/)
[![React](https://img.shields.io/badge/react-18%2B-61DAFB?logo=react&style=for-the-badge)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/tailwind--css-3.3%2B-06B6D4?logo=tailwindcss&style=for-the-badge)](https://tailwindcss.com/)

Красивый и лёгкий в развёртывании сервис для учёта посещаемости пар с gRPC + FastAPI backend и React + Ant Design frontend. 🚀

---

## ✨ Возможности
- Просмотр расписания и пар по датам 📅
- Подробная страница пары со списком студентов и отметками посещаемости ✅❌
- Управление правами старосты (выдача доступа на изменение посещаемости) 🔐
- Генерация QR-кодов для подтверждения посещаемости 📱
- Авторизация через куки (sign-in / sign-out) 🔑

---

## 🧰 Технологии
- Backend: Python, FastAPI, gRPC, protobuf, loguru 🐍
- Frontend: React, Ant Design, Tailwind CSS ⚛️
- Коммуникация: gRPC между сервисами, HTTP API для фронтенда 🌐
- БД/ODM: SQLAlchemy / Beanie 🗄️


---

## 🚀 Быстрый старт

1. Клонировать репозиторий:
```bash
git clone https://github.com/XXSnape/gRPC-attendance.git
```

2. Backend (локально / с Docker) — аккуратный шаг за шагом 🛠️

1) Создать и заполнить .env
- Скопируйте шаблон и отредактируйте значения (Unix):
```bash
cp backend/.env.template backend/.env
nano backend/.env
```
(Windows PowerShell)
```powershell
Copy-Item backend\.env.template backend\.env
notepad backend\.env
```
Убедитесь, что переменные DATABASE / POSTGRES / MONGO заполнены корректно.

2) Запустить зависимости (Postgres / Mongo) через Docker Compose
- Из корня проекта:
```bash
docker compose -f backend/docker-compose.yaml up -d
```
Проверить статус:
```bash
docker compose -f backend/docker-compose.yaml ps
```
Дождитесь статуса healthy для сервисов перед выполнением миграций.

3) Установить зависимости и активировать виртуальное окружение
- Unix:
```bash
python -m venv .venv
source .venv/bin/activate
pip install uv
uv sync
```

- Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install uv
uv sync
```

4) Выполнить миграции Alembic
- Перейдите в каталог backend и примените миграции:
```bash
cd backend
alembic upgrade head
```
(Если alembic настроен иначе — используйте `alembic -c alembic.ini upgrade head`)

5) Скомпилировать protobuf (по умолчанию не нужно)
```bash
cd backend/core/grpc
python -m grpc_tools.protoc --proto_path=protos --python_out=./pb --pyi_out=./pb protos/*
python -m grpc_tools.protoc --proto_path=protos --python_out=./pb --grpc_python_out=./pb --pyi_out=./pb protos/user-service.proto
python -m grpc_tools.protoc --proto_path=protos --python_out=./pb --grpc_python_out=./pb --pyi_out=./pb protos/lesson-service.proto
```

6) Запустить backend сервис(ы) в разных терминалах
- Примеры:
```bash
python backend/server.py
python backend/main.py
```
Примечание: если вы использовали docker compose для БД, убедитесь, что backend читает переменные из backend/.env или из окружения.

3. Frontend:
- Перейти в каталог frontend:
```bash
cd frontend
```
- Установить зависимости:
```bash
npm install
```
- Запустить приложение:
```bash
npm run dev
```
- По умолчанию фронт ожидает API на http://localhost:8000/api/v1

---

---

## 🏗️ Архитектура (кратко)
- gateway / API (FastAPI) — предоставляет REST для фронтенда и проксирует вызовы к gRPC сервисам.
- gRPC сервисы — бизнес-логика, доступ к БД.
- Frontend — SPA на React, использует куки для авторизации и Ant Design для UI.

---
