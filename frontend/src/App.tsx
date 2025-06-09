import React, { useState } from 'react';
import { QueryClient, QueryClientProvider, useQuery, useMutation } from 'react-query';
import { LoginForm } from './components/LoginForm';
import { CreateAccountForm } from './components/CreateAccountForm';
import { MachineList } from './components/MachineList';
import { MachineForm } from './components/MachineForm';
import { login, getMachines, addMachine, updateMachine, createAccount } from './api/client';
import { LoginCredentials, MachineFormData, MachineStatus, CreateAccountData } from './types';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

function AppContent() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));
  const [showAddForm, setShowAddForm] = useState(false);
  const [showCreateAccount, setShowCreateAccount] = useState(false);

  const { data: machines = [], isLoading: machinesLoading } = useQuery(
    'machines',
    getMachines,
    {
      enabled: isAuthenticated,
    }
  );

  const loginMutation = useMutation(login, {
    onSuccess: (data) => {
      localStorage.setItem('token', data.access_token);
      setIsAuthenticated(true);
    },
  });

  const createAccountMutation = useMutation(createAccount, {
    onSuccess: (data) => {
      localStorage.setItem('token', data.access_token!);
      setIsAuthenticated(true);
      setShowCreateAccount(false);
    },
  });

  const addMachineMutation = useMutation(addMachine, {
    onSuccess: () => {
      queryClient.invalidateQueries('machines');
      setShowAddForm(false);
    },
  });

  const updateMachineMutation = useMutation(
    ({ machineNumber, status }: { machineNumber: string; status: MachineStatus }) =>
      updateMachine(machineNumber, { status }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('machines');
      },
    }
  );

  if (!isAuthenticated) {
    if (showCreateAccount) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full">
            <CreateAccountForm
              onSubmit={(data: CreateAccountData) => createAccountMutation.mutate(data)}
              onCancel={() => setShowCreateAccount(false)}
              isLoading={createAccountMutation.isLoading}
            />
          </div>
        </div>
      );
    }

    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full">
          <LoginForm
            onSubmit={(data: LoginCredentials) => loginMutation.mutate(data)}
            isLoading={loginMutation.isLoading}
          />
          <div className="mt-4 text-center">
            <button
              onClick={() => setShowCreateAccount(true)}
              className="text-indigo-600 hover:text-indigo-500"
            >
              Create a new account
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Casino Machine Tracker</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={() => {
                  localStorage.removeItem('token');
                  setIsAuthenticated(false);
                }}
                className="btn-secondary"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              {showAddForm ? 'Add New Machine' : 'Machine Status'}
            </h2>
            <button
              onClick={() => setShowAddForm(!showAddForm)}
              className="btn-primary"
            >
              {showAddForm ? 'View Machines' : 'Add Machine'}
            </button>
          </div>

          {showAddForm ? (
            <MachineForm
              onSubmit={(data: MachineFormData) => addMachineMutation.mutate(data)}
              isLoading={addMachineMutation.isLoading}
            />
          ) : (
            <>
              {machinesLoading ? (
                <div className="text-center">Loading machines...</div>
              ) : (
                <MachineList
                  machines={machines}
                  onUpdateStatus={(machineNumber, status) =>
                    updateMachineMutation.mutate({ machineNumber, status })
                  }
                />
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
