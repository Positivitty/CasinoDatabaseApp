import React from 'react';
import { useForm } from 'react-hook-form';
import { MachineFormData } from '../types';

interface MachineFormProps {
  onSubmit: (data: MachineFormData) => void;
  isLoading: boolean;
}

export const MachineForm: React.FC<MachineFormProps> = ({ onSubmit, isLoading }) => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm<MachineFormData>();

  const onSubmitForm = (data: MachineFormData) => {
    onSubmit(data);
    reset();
  };

  return (
    <div className="card max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Add New Machine</h2>
      <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-6">
        <div>
          <label htmlFor="machine_number" className="form-label">
            Machine Number
          </label>
          <input
            type="text"
            id="machine_number"
            {...register('machine_number', { required: 'Machine number is required' })}
            className="form-input"
          />
          {errors.machine_number && (
            <p className="mt-1 text-sm text-red-600">{errors.machine_number.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="serial_number" className="form-label">
            Serial Number
          </label>
          <input
            type="text"
            id="serial_number"
            {...register('serial_number', { required: 'Serial number is required' })}
            className="form-input"
          />
          {errors.serial_number && (
            <p className="mt-1 text-sm text-red-600">{errors.serial_number.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="vendor" className="form-label">
            Vendor
          </label>
          <input
            type="text"
            id="vendor"
            {...register('vendor', { required: 'Vendor is required' })}
            className="form-input"
          />
          {errors.vendor && (
            <p className="mt-1 text-sm text-red-600">{errors.vendor.message}</p>
          )}
        </div>

        <div>
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              {...register('vendor_contacted')}
              className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            />
            <span className="ml-2">Vendor Contacted</span>
          </label>
        </div>

        <div>
          <label htmlFor="notes" className="form-label">
            Notes
          </label>
          <textarea
            id="notes"
            {...register('notes')}
            className="form-input"
            rows={3}
          />
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary"
          >
            {isLoading ? 'Adding...' : 'Add Machine'}
          </button>
        </div>
      </form>
    </div>
  );
}; 