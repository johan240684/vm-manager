import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// VMs API
export const vmAPI = {
  list: () => api.get('/vms'),
  get: (name) => api.get(`/vms/${name}`),
  create: (data) => api.post('/vms', data),
  delete: (name) => api.delete(`/vms/${name}`),
  start: (name) => api.post(`/vms/${name}/start`),
  stop: (name) => api.post(`/vms/${name}/stop`, { force: false }),
  reboot: (name) => api.post(`/vms/${name}/reboot`),
  update: (name, data) => api.put(`/vms/${name}`, data),
};

// Templates API
export const templateAPI = {
  list: () => api.get('/templates'),
  get: (id) => api.get(`/templates/${id}`),
  create: (data) => api.post('/templates', data),
};

// Monitoring API
export const monitoringAPI = {
  getStats: () => api.get('/monitoring/stats'),
  getVMMetrics: (vmName) => api.get(`/monitoring/vms/${vmName}/metrics`),
  getVMHistory: (vmName, hours = 24) => api.get(`/monitoring/vms/history/${vmName}`, { params: { hours } }),
  getAlerts: () => api.get('/monitoring/alerts'),
};

// Hypervisors API
export const hypervisorAPI = {
  list: () => api.get('/hypervisors'),
  get: (id) => api.get(`/hypervisors/${id}`),
  getStatus: (id) => api.get(`/hypervisors/${id}/status`),
};

export default api;
