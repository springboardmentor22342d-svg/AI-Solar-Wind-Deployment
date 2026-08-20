/**
 * LoginPage.jsx — User authentication page
 * POST /api/v1/auth/login → stores JWT → redirects to /dashboard
 */
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // OAuth2 form requires application/x-www-form-urlencoded
      const params = new URLSearchParams();
      params.append('username', form.email);
      params.append('password', form.password);

      const { data } = await api.post('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      // Store token and user info
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify({
        id: data.user_id,
        email: data.email,
        full_name: data.full_name,
        role: data.role,
      }));

      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Check your credentials.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        {/* Logo */}
        <div className="auth-logo">
          <div className="logo-title">Solar & Wind Platform</div>
          <div className="logo-sub">Deployment Intelligence System</div>
        </div>

        <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 700, marginBottom: '1.5rem' }}>
          Sign in to your account
        </h2>

        {error && (
          <div className="alert alert-error" style={{ marginBottom: '1rem' }}>
            {error}
          </div>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="login-email">Email Address</label>
            <input
              id="login-email"
              className="form-input"
              type="email"
              name="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={handleChange}
              required
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="login-password">Password</label>
            <input
              id="login-password"
              className="form-input"
              type="password"
              name="password"
              placeholder="••••••••"
              value={form.password}
              onChange={handleChange}
              required
              autoComplete="current-password"
            />
          </div>

          <button
            id="login-submit"
            type="submit"
            className="btn btn-primary btn-lg w-full"
            disabled={loading}
            style={{ marginTop: '0.5rem' }}
          >
            {loading ? (
              <><span className="spinner" /> Signing in…</>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="auth-footer">
          Don't have an account?{' '}
          <Link to="/register">Create one</Link>
        </div>
      </div>
    </div>
  );
}
