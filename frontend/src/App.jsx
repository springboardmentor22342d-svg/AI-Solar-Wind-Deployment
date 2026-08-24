import React, { useState } from "react";

import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import SolarAnalysis from "./pages/SolarAnalysis";
import WindAnalysis from "./pages/WindAnalysis";
import SiteSuitability from "./pages/SiteSuitability";
import MapExplorer from "./pages/MapExplorer";
import AIRecommendations from "./pages/AIRecommendations";
import Projects from "./pages/Projects";
import Reports from "./pages/Reports";
import DataSources from "./pages/DataSources";
import Alerts from "./pages/Alerts";
import Settings from "./pages/Settings";

function App() {

  const [activePage, setActivePage] =
    useState("Dashboard");

  function renderPage() {

    switch (activePage) {

      case "Solar Analysis":
        return <SolarAnalysis />;

      case "Wind Analysis":
        return <WindAnalysis />;

      case "Site Suitability":
        return <SiteSuitability />;

      case "Map Explorer":
        return <MapExplorer />;

      case "AI Recommendations":
        return <AIRecommendations />;

      case "Projects":
        return <Projects />;

      case "Reports":
        return <Reports />;

      case "Data Sources":
        return <DataSources />;

      case "Alerts":
        return <Alerts />;

      case "Settings":
        return <Settings />;

      default:
        return (
          <Dashboard
            setActivePage={setActivePage}
          />
        );
    }
  }

  return (
    <div className="app">

      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <div className="main">

        <Navbar />

        <div className="page-container">
          {renderPage()}
        </div>

      </div>

    </div>
  );
}

export default App;
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'

import Login      from './pages/Login'
import Register   from './pages/Register'
import Dashboard  from './pages/Dashboard'
import Projects   from './pages/Projects'
import Sites      from './pages/Sites'
import Assessment from './pages/Assessment'
import Features   from './pages/Features'
import Forecast   from './pages/Forecast'
import Profile    from './pages/Profile'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public */}
          <Route path="/login"    element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected — wrapped in Layout (Sidebar + Topbar) */}
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard"  element={<Dashboard />} />
              <Route path="/projects"   element={<Projects />} />
              <Route path="/sites"      element={<Sites />} />
              <Route path="/assessment" element={<Assessment />} />
              <Route path="/features"   element={<Features />} />
              <Route path="/forecast"   element={<Forecast />} />
              <Route path="/profile"    element={<Profile />} />
            </Route>
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
