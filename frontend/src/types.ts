export enum MachineStatus {
    DOWN = "down",
    FIXED = "fixed",
    IN_PROGRESS = "in_progress"
}

export interface Machine {
    id: number;
    machine_number: string;
    serial_number: string;
    vendor: string;
    notes?: string;
    status: MachineStatus;
    date_down: string;
}

export interface MachineFormData {
    machine_number: string;
    serial_number: string;
    vendor: string;
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

export interface CreateAccountData {
    username: string;
    email: string;
    password: string;
}

export interface UserResponse {
    id: number;
    username: string;
    email: string;
    is_active: boolean;
    is_admin: boolean;
    access_token?: string;
    token_type?: string;
} 