import React, { useState, useEffect } from 'react';
import { monitoringAPI } from '../services/api';
import { Activity, AlertCircle } from 'lucide-react';

export default function Monitoring() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMonitoringData();
    const interval = setInterval(fetchMonitoringData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchMonitoringData = async () => {
    try {
      const response = await monitoringAPI.getStats();
      setStats(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load monitoring data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Monitoring</h1>
        <p className="text-gray-600 mt-1">Real-time system monitoring and metrics</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle size={20} className="text-red-600" />
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Metrics Grid */}
      {stats && (
        <>
          {/* VM Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Activity size={20} className="text-blue-600" />
                Virtual Machines
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total VMs</span>
                  <span className="font-semibold">{stats.total_vms}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Running</span>
                  <span className="font-semibold text-green-600">{stats.running_vms}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Stopped</span>
                  <span className="font-semibold text-gray-600">{stats.stopped_vms}</span>
                </div>
              </div>
            </div>

            {/* CPU Metrics */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="font-semibold text-gray-900 mb-4">CPU Resources</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Cores</span>
                  <span className="font-semibold">{stats.total_cpu_cores}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Hypervisors</span>
                  <span className="font-semibold">{stats.hypervisors}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Memory Metrics */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Memory</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600">Usage</span>
                  <span className="font-semibold">
                    {stats.used_memory_gb}/{stats.total_memory_gb} GB
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-blue-600 h-3 rounded-full"
                    style={{
                      width: `${(stats.used_memory_gb / stats.total_memory_gb) * 100}%`,
                    }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Storage Metrics */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Storage</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600">Usage</span>
                  <span className="font-semibold">
                    {stats.used_disk_gb}/{stats.total_disk_gb} GB
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-purple-600 h-3 rounded-full"
                    style={{
                      width: `${(stats.used_disk_gb / stats.total_disk_gb) * 100}%`,
                    }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Loading State */}
      {loading && !stats && (
        <div className="text-center text-gray-500 py-12">Loading monitoring data...</div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">Monitoring</h3>
        <p className="text-blue-800 text-sm">
          This page displays real-time metrics about your VM infrastructure. Metrics are updated every 30 seconds.
          For detailed VM metrics, visit the Virtual Machines page.
        </p>
      </div>
    </div>
  );
}
