/**
 * App.jsx — Main application with React Router
 *
 * Routes:
 *   /              → redirect to /login
 *   /login         → LoginPage
 *   /register      → RegisterPage
 *   /dashboard     → DashboardPage (protected)
 *   /projects      → ProjectsPage (protected)
 *   /site-analysis → SiteAnalysisPage (protected)
 *   /reports       → ReportsPage (protected)
 */
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import './App.css';

import ProtectedRoute from './components/ProtectedRoute';
import Sidebar from './components/Sidebar';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ProjectsPage from './pages/ProjectsPage';
import SiteAnalysisPage from './pages/SiteAnalysisPage';
import ReportsPage from './pages/ReportsPage';

/** Placeholder for Milestone 2 pages */
function ComingSoonPage({ title, icon }) {
  return (
    <div className="page-content">
      <div className="page-header">
        <div>
          <h1 className="page-title">{title}</h1>
        </div>
      </div>
      <div className="card">
        <div className="empty-state" style={{ padding: '4rem' }}>
          <h3>{title}</h3>
          <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <span className="badge badge-analyst">ML Model Integration</span>
            <span className="badge badge-admin">Dataset Processing</span>
            <span className="badge badge-success">GIS Analysis</span>
          </div>
        </div>
      </div>
    </div>
  );
}

/** Layout wrapper: sidebar + topbar + content */
function DashboardLayout({ children }) {
  const location = useLocation();

  const TITLES = {
    '/dashboard': { label: 'Dashboard' },
    '/projects': { label: 'My Projects' },
    '/site-analysis': { label: 'Site Suitability Analysis' },
    '/reports': { label: 'Reports' },
  };

  const current = TITLES[location.pathname] || { label: 'Platform' };

  const user = (() => {
    try { return JSON.parse(localStorage.getItem('user') || '{}'); }
    catch { return {}; }
  })();

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        {/* Topbar */}
        <header className="topbar">
          <div className="topbar-title">
            {current.label}
          </div>
          <div className="topbar-actions">
            {user.role && (
              <span className={`badge badge-${user.role}`}>{user.role}</span>
            )}
            <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-muted)' }}>
              {user.email}
            </span>
          </div>
        </header>
        {children}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected routes — wrapped in DashboardLayout */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <DashboardPage />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/projects"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <ProjectsPage />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        {/* Unified Analysis */}
        <Route
          path="/site-analysis"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <SiteAnalysisPage />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <ReportsPage />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />

        {/* Default redirect */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
