// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';
import Header from './components/Header';
import LoginForm from './components/Login';
import SchedulePage from './components/SchedulePage';
import LessonDetails from './components/LessonDetails';
import ProfilePage from './components/ProfilePage';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen">
          <Header />
          <Routes>
            <Route path="/login" element={<LoginForm />} />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <SchedulePage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/lessons/:lessonId" 
              element={
                <ProtectedRoute>
                  <LessonDetails />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/me" 
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;