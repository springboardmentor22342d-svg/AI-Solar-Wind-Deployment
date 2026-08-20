/**
 * Sidebar.jsx — Dashboard navigation sidebar
 */
import { NavLink, useNavigate } from 'react-router-dom';

const NAV_ITEMS = [
  {
    section: 'Overview',
    items: [
      { to: '/dashboard', label: 'Dashboard' },
      { to: '/projects', label: 'My Projects' },
    ],
  },
  {
    section: 'Analysis',
    items: [
      { to: '/site-analysis', label: 'Site Analysis' },
    ],
  },
  {
    section: 'Reports',
    items: [
      { to: '/reports', label: 'Reports' },
    ],
  },
];

export default function Sidebar() {
  const navigate = useNavigate();

  const user = (() => {
    try {
      return JSON.parse(localStorage.getItem('user') || '{}');
    } catch {
      return {};
    }
  })();

  function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  }

  const initials = user.full_name
    ? user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
    : (user.email?.[0] || 'U').toUpperCase();

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div>
            <div className="logo-text">Solar & Wind</div>
            <div className="logo-sub">Intelligence Platform</div>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="sidebar-nav">
        {NAV_ITEMS.map((group) => (
          <div key={group.section}>
            <div className="sidebar-section-label">{group.section}</div>
            {group.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
              >
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="user-avatar">{initials}</div>
          <div className="user-info">
            <div className="user-name">{user.full_name || user.email || 'User'}</div>
            <div className="user-role">{user.role || 'user'}</div>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="btn btn-ghost btn-sm w-full"
          style={{ marginTop: '0.5rem', justifyContent: 'flex-start', gap: '0.5rem' }}
        >
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
