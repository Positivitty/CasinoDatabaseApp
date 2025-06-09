import axios from 'axios';
import { AuthResponse, LoginCredentials, Machine, MachineFormData, CreateAccountData, UserResponse } from '../types';

const API_URL = 'http://localhost:8001';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  // Create URLSearchParams for proper form data encoding
  const formData = new URLSearchParams();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);
  
  const response = await axios.post<AuthResponse>(`${API_URL}/token`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const getMachines = async (): Promise<Machine[]> => {
  const response = await api.get<Machine[]>('/machines/');
  return response.data;
};

export const addMachine = async (machine: MachineFormData): Promise<Machine> => {
  const response = await api.post<Machine>('/machines/', machine);
  return response.data;
};

export const updateMachine = async (machineNumber: string, updates: Partial<Machine>): Promise<Machine> => {
  const response = await api.patch<Machine>(`/machines/${machineNumber}`, updates);
  return response.data;
};

export const getMachine = async (machineNumber: string): Promise<Machine> => {
  const response = await api.get<Machine>(`/machines/${machineNumber}`);
  return response.data;
};

export const createAccount = async (data: CreateAccountData): Promise<UserResponse> => {
  const response = await api.post<UserResponse>('/users/', data);
  return response.data;
}; 