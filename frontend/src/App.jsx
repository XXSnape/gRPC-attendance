// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';
import Header from './components/Header';
import LoginForm from './components/Login';
import Dashboard from './components/Lessons';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen">
          <Header />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/login" element={<LoginForm />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;