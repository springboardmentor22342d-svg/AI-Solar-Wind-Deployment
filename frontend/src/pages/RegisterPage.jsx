/**
 * RegisterPage.jsx — User registration page
 * POST /api/v1/auth/register → redirects to /login
 */
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    full_name: '',
    email: '',
    password: '',
    confirm_password: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');

    if (form.password !== form.confirm_password) {
      setError('Passwords do not match.');
      return;
    }
    if (form.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setLoading(true);
    try {
      await api.post('/auth/register', {
        full_name: form.full_name,
        email: form.email,
        password: form.password,
      });

      setSuccess('Account created! Redirecting to login…');
      setTimeout(() => navigate('/login'), 1800);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card" style={{ maxWidth: 480 }}>
        {/* Logo */}
        <div className="auth-logo">
          <div className="logo-title">Solar & Wind Platform</div>
          <div className="logo-sub">Create your account</div>
        </div>

        {error && (
          <div className="alert alert-error" style={{ marginBottom: '1rem' }}>
            {error}
          </div>
        )}
        {success && (
          <div className="alert alert-success" style={{ marginBottom: '1rem' }}>
            {success}
          </div>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="reg-name">Full Name</label>
            <input
              id="reg-name"
              className="form-input"
              type="text"
              name="full_name"
              placeholder="Jane Smith"
              value={form.full_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="reg-email">Email Address</label>
            <input
              id="reg-email"
              className="form-input"
              type="email"
              name="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="reg-password">Password</label>
            <input
              id="reg-password"
              className="form-input"
              type="password"
              name="password"
              placeholder="Min. 6 characters"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="reg-confirm">Confirm Password</label>
            <input
              id="reg-confirm"
              className={`form-input${form.confirm_password && form.password !== form.confirm_password ? ' error' : ''}`}
              type="password"
              name="confirm_password"
              placeholder="Repeat password"
              value={form.confirm_password}
              onChange={handleChange}
              required
            />
            {form.confirm_password && form.password !== form.confirm_password && (
              <span className="form-error">Passwords do not match</span>
            )}
          </div>

          <button
            id="register-submit"
            type="submit"
            className="btn btn-primary btn-lg w-full"
            disabled={loading}
            style={{ marginTop: '0.25rem' }}
          >
            {loading ? (
              <><span className="spinner" /> Creating account…</>
            ) : (
              'Create Account'
            )}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account?{' '}
          <Link to="/login">Sign in</Link>
        </div>
      </div>
    </div>
  );
}
