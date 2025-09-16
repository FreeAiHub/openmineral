import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      }
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use((config) => {
      const token = this.getAuthToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          this.removeAuthToken();
          window.location.reload();
        }
        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token) {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  getAuthToken() {
    return localStorage.getItem('token');
  }

  removeAuthToken() {
    localStorage.removeItem('token');
  }

  // Health check
  async healthCheck() {
    const response = await this.client.get('/api/health');
    return response.data;
  }

  // Authentication
  async login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await this.client.post('/api/auth/token', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/api/auth/me');
    return response.data;
  }

  // Deals
  async getDeals() {
    const response = await this.client.get('/api/deals');
    return response.data;
  }

  async getDeal(dealId) {
    const response = await this.client.get(`/api/deals/${dealId}`);
    return response.data;
  }

  async createDeal(dealData) {
    const response = await this.client.post('/api/deals', dealData);
    return response.data;
  }

  async updateDeal(dealId, dealData) {
    const response = await this.client.put(`/api/deals/${dealId}`, dealData);
    return response.data;
  }

  async deleteDeal(dealId) {
    const response = await this.client.delete(`/api/deals/${dealId}`);
    return response.data;
  }

  // Market data
  async getMarketPrices() {
    const response = await this.client.get('/api/market/prices');
    return response.data;
  }

  async getCommodityAnalysis(commodity) {
    const response = await this.client.get(`/api/market/analysis/${commodity}`);
    return response.data;
  }

  // Dashboard
  async getDashboardStats() {
    const response = await this.client.get('/api/dashboard/stats');
    return response.data;
  }
}

export default new ApiService();