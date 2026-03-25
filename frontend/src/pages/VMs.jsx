import React, { useState, useEffect } from 'react';
import { vmAPI, templateAPI } from '../services/api';
import { Play, StopCircle, RotateCcw, Trash2, Plus, AlertCircle } from 'lucide-react';

export default function VMs() {
  const [vms, setVms] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createFormData, setCreateFormData] = useState({
    name: '',
    cpu_count: 2,
    memory_mb: 2048,
    disk_gb: 50,
    hostname: '',
    template_id: '',
  });

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [vmsRes, templatesRes] = await Promise.all([
        vmAPI.list(),
        templateAPI.list(),
      ]);
      setVms(vmsRes.data);
      setTemplates(templatesRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to load VMs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleVMAction = async (vmName, action) => {
    try {
      let response;
      switch (action) {
        case 'start':
          response = await vmAPI.start(vmName);
          break;
        case 'stop':
          response = await vmAPI.stop(vmName);
          break;
        case 'reboot':
          response = await vmAPI.reboot(vmName);
          break;
        case 'delete':
          if (window.confirm(`Are you sure you want to delete VM '${vmName}'?`)) {
            response = await vmAPI.delete(vmName);
          } else {
            return;
          }
          break;
        default:
          return;
      }
      // Refresh VM list
      await fetchData();
    } catch (err) {
      setError(`Failed to ${action} VM: ${err.message}`);
    }
  };

  const handleCreateVM = async (e) => {
    e.preventDefault();
    try {
      await vmAPI.create(createFormData);
      setShowCreateModal(false);
      setCreateFormData({
        name: '',
        cpu_count: 2,
        memory_mb: 2048,
        disk_gb: 50,
        hostname: '',
        template_id: '',
      });
      await fetchData();
    } catch (err) {
      setError(`Failed to create VM: ${err.message}`);
    }
  };

  const getStateColor = (state) => {
    switch (state) {
      case 'running':
        return 'text-green-600 bg-green-50';
      case 'paused':
        return 'text-yellow-600 bg-yellow-50';
      case 'stopped':
        return 'text-gray-600 bg-gray-50';
      default:
        return 'text-red-600 bg-red-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Virtual Machines</h1>
          <p className="text-gray-600 mt-1">Manage your VM instances</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 flex items-center gap-2"
        >
          <Plus size={20} />
          Create VM
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle size={20} className="text-red-600" />
          <p className="text-red-800">{error}</p>
          <button
            onClick={() => setError(null)}
            className="ml-auto text-red-600 hover:text-red-800"
          >
            ✕
          </button>
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 w-full max-w-md">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New VM</h2>
            <form onSubmit={handleCreateVM} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  VM Name
                </label>
                <input
                  type="text"
                  required
                  value={createFormData.name}
                  onChange={(e) =>
                    setCreateFormData({ ...createFormData, name: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Hostname
                </label>
                <input
                  type="text"
                  required
                  value={createFormData.hostname}
                  onChange={(e) =>
                    setCreateFormData({ ...createFormData, hostname: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Template
                </label>
                <select
                  value={createFormData.template_id}
                  onChange={(e) =>
                    setCreateFormData({ ...createFormData, template_id: e.target.value })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select a template</option>
                  {templates.map((template) => (
                    <option key={template.id} value={template.id}>
                      {template.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    CPU Count
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="128"
                    value={createFormData.cpu_count}
                    onChange={(e) =>
                      setCreateFormData({
                        ...createFormData,
                        cpu_count: parseInt(e.target.value),
                      })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Memory (MB)
                  </label>
                  <input
                    type="number"
                    min="512"
                    value={createFormData.memory_mb}
                    onChange={(e) =>
                      setCreateFormData({
                        ...createFormData,
                        memory_mb: parseInt(e.target.value),
                      })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Disk (GB)
                  </label>
                  <input
                    type="number"
                    min="10"
                    value={createFormData.disk_gb}
                    onChange={(e) =>
                      setCreateFormData({
                        ...createFormData,
                        disk_gb: parseInt(e.target.value),
                      })
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-2 font-medium"
                >
                  Create
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded-lg py-2 font-medium"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* VMs Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {loading && !vms.length ? (
          <div className="p-6 text-center text-gray-500">Loading VMs...</div>
        ) : vms.length === 0 ? (
          <div className="p-6 text-center text-gray-500">No VMs found</div>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  State
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  CPU
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  Memory
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {vms.map((vm) => (
                <tr key={vm.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">
                    {vm.name}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStateColor(vm.state)}`}>
                      {vm.state}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{vm.cpu_count}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {vm.memory_mb} MB
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-2">
                      {vm.state !== 'running' && (
                        <button
                          onClick={() => handleVMAction(vm.name, 'start')}
                          className="p-2 text-green-600 hover:bg-green-50 rounded"
                          title="Start"
                        >
                          <Play size={18} />
                        </button>
                      )}
                      {vm.state === 'running' && (
                        <>
                          <button
                            onClick={() => handleVMAction(vm.name, 'stop')}
                            className="p-2 text-red-600 hover:bg-red-50 rounded"
                            title="Stop"
                          >
                            <StopCircle size={18} />
                          </button>
                          <button
                            onClick={() => handleVMAction(vm.name, 'reboot')}
                            className="p-2 text-blue-600 hover:bg-blue-50 rounded"
                            title="Reboot"
                          >
                            <RotateCcw size={18} />
                          </button>
                        </>
                      )}
                      <button
                        onClick={() => handleVMAction(vm.name, 'delete')}
                        className="p-2 text-orange-600 hover:bg-orange-50 rounded"
                        title="Delete"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
