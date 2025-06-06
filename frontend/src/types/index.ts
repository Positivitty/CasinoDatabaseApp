export enum MachineStatus {
  DOWN = "down",
  FIXED = "fixed",
  IN_PROGRESS = "in_progress"
}

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  is_admin: boolean;
}

export interface Machine {
  id: number;
  machine_number: string;
  serial_number: string;
  vendor: string;
  date_down: string;
  vendor_contacted: boolean;
  technician_id: number;
  status: MachineStatus;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface MachineFormData {
  machine_number: string;
  serial_number: string;
  vendor: string;
  vendor_contacted: boolean;
  notes?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
} 