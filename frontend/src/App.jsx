// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';
import Header from './components/Header';
import LoginForm from './components/Login';
import SchedulePage from './components/SchedulePage';
import LessonDetails from './components/LessonDetails';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen">
          <Header />
          <Routes>
            <Route path="/" element={<SchedulePage />} />
            <Route path="/login" element={<LoginForm />} />
            <Route path="/lessons/:lessonId" element={<LessonDetails />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;