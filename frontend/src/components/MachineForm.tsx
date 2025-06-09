import React, { FormEvent, ChangeEvent } from 'react';
import { MachineFormData } from '../types';

interface MachineFormProps {
    onSubmit: (data: MachineFormData) => void;
    isLoading: boolean;
}

export const MachineForm: React.FC<MachineFormProps> = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = React.useState<MachineFormData>({
        machine_number: '',
        serial_number: '',
        vendor: '',
        notes: ''
    });

    const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        onSubmit(formData);
    };

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData((prev: MachineFormData) => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label htmlFor="machine_number" className="block text-sm font-medium text-gray-700">
                    Machine Number
                </label>
                <input
                    type="text"
                    name="machine_number"
                    id="machine_number"
                    required
                    value={formData.machine_number}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
            </div>

            <div>
                <label htmlFor="serial_number" className="block text-sm font-medium text-gray-700">
                    Serial Number
                </label>
                <input
                    type="text"
                    name="serial_number"
                    id="serial_number"
                    required
                    value={formData.serial_number}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
            </div>

            <div>
                <label htmlFor="vendor" className="block text-sm font-medium text-gray-700">
                    Vendor
                </label>
                <input
                    type="text"
                    name="vendor"
                    id="vendor"
                    required
                    value={formData.vendor}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
            </div>

            <div>
                <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
                    Notes
                </label>
                <textarea
                    name="notes"
                    id="notes"
                    value={formData.notes}
                    onChange={handleChange}
                    rows={3}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
            </div>

            <div className="flex justify-end">
                <button
                    type="submit"
                    disabled={isLoading}
                    className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
                >
                    {isLoading ? 'Adding...' : 'Add Machine'}
                </button>
            </div>
        </form>
    );
}; 