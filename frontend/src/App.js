import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import BookDetail from './pages/BookDetail';
import QAPage from './pages/QAPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-blue-600 text-white p-4">
          <h1 className="text-2xl font-bold">AI-Powered Book Insight Platform</h1>
        </header>
        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/book/:id" element={<BookDetail />} />
            <Route path="/qa" element={<QAPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;