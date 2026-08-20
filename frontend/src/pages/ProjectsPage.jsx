/**
 * ProjectsPage.jsx — Full project management (list, create, edit, delete)
 */
import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

const INITIAL_FORM = {
  project_name: '',
  description: '',
  state: '',
  latitude: '',
  longitude: '',
};

const INDIA_STATES = [
  'Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh',
  'Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka',
  'Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
  'Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
  'Tripura','Uttar Pradesh','Uttarakhand','West Bengal',
  'Andaman & Nicobar Islands','Chandigarh','Dadra & Nagar Haveli','Daman & Diu',
  'Delhi','Jammu & Kashmir','Ladakh','Lakshadweep','Puducherry',
];

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editProject, setEditProject] = useState(null); // null = create, obj = edit
  const [form, setForm] = useState(INITIAL_FORM);
  const [formError, setFormError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  const fetchProjects = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get('/projects');
      setProjects(data);
    } catch {
      setProjects([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchProjects(); }, [fetchProjects]);

  function openCreate() {
    setEditProject(null);
    setForm(INITIAL_FORM);
    setFormError('');
    setShowModal(true);
  }

  function openEdit(project) {
    setEditProject(project);
    setForm({
      project_name: project.project_name,
      description: project.description || '',
      state: project.state,
      latitude: String(project.latitude),
      longitude: String(project.longitude),
    });
    setFormError('');
    setShowModal(true);
  }

  function closeModal() {
    setShowModal(false);
    setEditProject(null);
    setForm(INITIAL_FORM);
    setFormError('');
  }

  function handleFormChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
    setFormError('');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setFormError('');

    const lat = parseFloat(form.latitude);
    const lon = parseFloat(form.longitude);
    if (isNaN(lat) || lat < -90 || lat > 90) { setFormError('Latitude must be between -90 and 90.'); return; }
    if (isNaN(lon) || lon < -180 || lon > 180) { setFormError('Longitude must be between -180 and 180.'); return; }

    const payload = { ...form, latitude: lat, longitude: lon };
    setSubmitting(true);
    try {
      if (editProject) {
        await api.put(`/projects/${editProject.id}`, payload);
      } else {
        await api.post('/projects', payload);
      }
      closeModal();
      fetchProjects();
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save project.');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete(id) {
    try {
      await api.delete(`/projects/${id}`);
      setDeleteConfirm(null);
      fetchProjects();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete project.');
    }
  }

  return (
    <div className="page-content">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">My Projects</h1>
          <p className="page-subtitle">Manage your solar & wind deployment projects</p>
        </div>
        <button id="create-project-btn" className="btn btn-primary" onClick={openCreate}>
          + New Project
        </button>
      </div>

      {/* Content */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-muted)' }}>
          <span className="spinner" style={{ width: 32, height: 32, borderWidth: 3 }} />
          <p style={{ marginTop: '1rem' }}>Loading projects…</p>
        </div>
      ) : projects.length === 0 ? (
        <div className="card">
          <div className="empty-state">
            <h3>No projects yet</h3>
            <p>Create your first deployment project to get started with site analysis</p>
            <button className="btn btn-primary" onClick={openCreate}>+ Create First Project</button>
          </div>
        </div>
      ) : (
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Project Name</th>
                <th>State / Region</th>
                <th>Coordinates</th>
                <th>Description</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((p, idx) => (
                <tr key={p.id}>
                  <td style={{ color: 'var(--text-muted)' }}>{idx + 1}</td>
                  <td>
                    <div style={{ fontWeight: 600 }}>{p.project_name}</div>
                  </td>
                  <td>{p.state}</td>
                  <td style={{ fontFamily: 'monospace', fontSize: 'var(--font-size-xs)', color: 'var(--text-secondary)' }}>
                    {p.latitude.toFixed(4)}°, {p.longitude.toFixed(4)}°
                  </td>
                  <td style={{ color: 'var(--text-secondary)', maxWidth: 200 }}>
                    {p.description || <span style={{ color: 'var(--text-muted)' }}>—</span>}
                  </td>
                  <td style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-xs)' }}>
                    {new Date(p.created_at).toLocaleDateString()}
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => openEdit(p)}
                        title="Edit project"
                      >
                        Edit
                      </button>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => setDeleteConfirm(p)}
                        title="Delete project"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Create / Edit Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && closeModal()}>
          <div className="modal">
            <div className="modal-header">
              <h2 className="modal-title">
                {editProject ? 'Edit Project' : 'New Project'}
              </h2>
              <button className="btn btn-ghost btn-sm" onClick={closeModal}>✕</button>
            </div>

            {formError && (
              <div className="alert alert-error" style={{ marginBottom: '1rem' }}>{formError}</div>
            )}

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label" htmlFor="proj-name">Project Name *</label>
                <input
                  id="proj-name"
                  className="form-input"
                  name="project_name"
                  placeholder="e.g. Rajasthan Solar Farm"
                  value={form.project_name}
                  onChange={handleFormChange}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="proj-state">State / Region *</label>
                <select
                  id="proj-state"
                  className="form-input"
                  name="state"
                  value={form.state}
                  onChange={handleFormChange}
                  required
                  style={{ cursor: 'pointer' }}
                >
                  <option value="">— Select state —</option>
                  {INDIA_STATES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                <div className="form-group">
                  <label className="form-label" htmlFor="proj-lat">Latitude *</label>
                  <input
                    id="proj-lat"
                    className="form-input"
                    name="latitude"
                    type="number"
                    step="0.0001"
                    min="-90"
                    max="90"
                    placeholder="e.g. 26.9124"
                    value={form.latitude}
                    onChange={handleFormChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label" htmlFor="proj-lon">Longitude *</label>
                  <input
                    id="proj-lon"
                    className="form-input"
                    name="longitude"
                    type="number"
                    step="0.0001"
                    min="-180"
                    max="180"
                    placeholder="e.g. 75.7873"
                    value={form.longitude}
                    onChange={handleFormChange}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="proj-desc">Description (optional)</label>
                <textarea
                  id="proj-desc"
                  className="form-input"
                  name="description"
                  rows={3}
                  placeholder="Brief description of the project…"
                  value={form.description}
                  onChange={handleFormChange}
                  style={{ resize: 'vertical' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
                <button type="button" className="btn btn-ghost" onClick={closeModal}>Cancel</button>
                <button
                  id="project-save-btn"
                  type="submit"
                  className="btn btn-primary"
                  disabled={submitting}
                >
                  {submitting ? <><span className="spinner" /> Saving…</> : (editProject ? 'Save Changes' : 'Create Project')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirm Modal */}
      {deleteConfirm && (
        <div className="modal-overlay">
          <div className="modal" style={{ maxWidth: 400 }}>
            <h2 className="modal-title" style={{ marginBottom: '1rem' }}>Delete Project</h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: 'var(--font-size-sm)' }}>
              Are you sure you want to delete <strong style={{ color: 'var(--text-primary)' }}>"{deleteConfirm.project_name}"</strong>?
              This action cannot be undone.
            </p>
            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
              <button className="btn btn-ghost" onClick={() => setDeleteConfirm(null)}>Cancel</button>
              <button
                id="confirm-delete-btn"
                className="btn btn-danger"
                onClick={() => handleDelete(deleteConfirm.id)}
              >
                Delete Project
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
