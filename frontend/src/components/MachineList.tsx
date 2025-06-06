import React from 'react';
import { Machine, MachineStatus } from '../types';

interface MachineListProps {
  machines: Machine[];
  onUpdateStatus: (machineNumber: string, status: MachineStatus) => void;
}

export const MachineList: React.FC<MachineListProps> = ({ machines, onUpdateStatus }) => {
  const getStatusColor = (status: MachineStatus) => {
    switch (status) {
      case MachineStatus.DOWN:
        return 'bg-red-100 text-red-800';
      case MachineStatus.IN_PROGRESS:
        return 'bg-yellow-100 text-yellow-800';
      case MachineStatus.FIXED:
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {machines.map((machine) => (
        <div
          key={machine.id}
          className={`card ${
            machine.status === MachineStatus.FIXED ? 'border-green-500' : 'border-red-500'
          } border-2`}
        >
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-medium">Machine #{machine.machine_number}</h3>
              <p className="text-sm text-gray-500">Serial: {machine.serial_number}</p>
            </div>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                machine.status
              )}`}
            >
              {machine.status}
            </span>
          </div>
          
          <div className="mt-4">
            <p className="text-sm text-gray-600">Vendor: {machine.vendor}</p>
            <p className="text-sm text-gray-600">
              Down since: {new Date(machine.date_down).toLocaleDateString()}
            </p>
            {machine.notes && (
              <p className="mt-2 text-sm text-gray-600">Notes: {machine.notes}</p>
            )}
          </div>

          <div className="mt-4 flex justify-end space-x-2">
            {machine.status !== MachineStatus.FIXED && (
              <>
                {machine.status === MachineStatus.DOWN && (
                  <button
                    onClick={() => onUpdateStatus(machine.machine_number, MachineStatus.IN_PROGRESS)}
                    className="btn-secondary text-sm"
                  >
                    Mark In Progress
                  </button>
                )}
                <button
                  onClick={() => onUpdateStatus(machine.machine_number, MachineStatus.FIXED)}
                  className="btn-primary text-sm"
                >
                  Mark Fixed
                </button>
              </>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}; 