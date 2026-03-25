import React, { useState, useEffect } from 'react';
import { monitoringAPI, hypervisorAPI } from '../services/api';
import StatCard from '../components/StatCard';
import { Server, AlertCircle, Zap } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [hypervisors, setHypervisors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsRes, hvRes] = await Promise.all([
        monitoringAPI.getStats(),
        hypervisorAPI.list(),
      ]);
      setStats(statsRes.data);
      setHypervisors(hvRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !stats) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">System overview and quick stats</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle size={20} className="text-red-600" />
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total VMs"
            value={stats.total_vms}
            icon={Server}
            color="blue"
          />
          <StatCard
            title="Running VMs"
            value={stats.running_vms}
            icon={Zap}
            color="green"
          />
          <StatCard
            title="Stopped VMs"
            value={stats.stopped_vms}
            icon={Server}
            color="gray"
          />
          <StatCard
            title="CPU Cores"
            value={stats.total_cpu_cores}
            icon={Zap}
            color="purple"
          />
        </div>
      )}

      {/* Hypervisor Status */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Hypervisor Status</h2>
        {hypervisors.length === 0 ? (
          <p className="text-gray-500">No hypervisors connected</p>
        ) : (
          <div className="space-y-4">
            {hypervisors.map((hv) => (
              <div key={hv.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-gray-900">{hv.name}</h3>
                    <p className="text-sm text-gray-600">{hv.hostname}</p>
                  </div>
                  <div className="text-right">
                    <p className={`text-sm font-medium ${
                      hv.status === 'connected' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {hv.status}
                    </p>
                    <p className="text-xs text-gray-500">
                      {hv.vms_running}/{hv.vms_total} VMs
                    </p>
                  </div>
                </div>
                <div className="mt-3 grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">CPU Cores</p>
                    <p className="font-semibold">{hv.cpu_cores}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Memory</p>
                    <p className="font-semibold">{hv.memory_gb} GB</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Hypervisor</p>
                    <p className="font-semibold">{hv.hypervisor_type}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="p-4 border border-blue-200 rounded-lg hover:bg-blue-50 transition">
            <p className="text-sm font-medium text-blue-900">Create VM</p>
          </button>
          <button className="p-4 border border-green-200 rounded-lg hover:bg-green-50 transition">
            <p className="text-sm font-medium text-green-900">Start All</p>
          </button>
          <button className="p-4 border border-orange-200 rounded-lg hover:bg-orange-50 transition">
            <p className="text-sm font-medium text-orange-900">Backup</p>
          </button>
          <button className="p-4 border border-purple-200 rounded-lg hover:bg-purple-50 transition">
            <p className="text-sm font-medium text-purple-900">Settings</p>
          </button>
        </div>
      </div>
    </div>
  );
}
