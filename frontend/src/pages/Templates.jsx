import React, { useState, useEffect } from 'react';
import { templateAPI } from '../services/api';
import { Package, AlertCircle } from 'lucide-react';

export default function Templates() {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const response = await templateAPI.list();
      setTemplates(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load templates');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">VM Templates</h1>
        <p className="text-gray-600 mt-1">Pre-configured templates for quick VM deployment</p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3">
          <AlertCircle size={20} className="text-red-600" />
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Templates Grid */}
      <div>
        {loading ? (
          <div className="text-center text-gray-500 py-12">Loading templates...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {templates.map((template) => (
              <div key={template.id} className="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden">
                {/* Template Header */}
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-6 text-white text-center">
                  <Package size={32} className="mx-auto mb-2 opacity-80" />
                  <h3 className="text-lg font-bold">{template.name}</h3>
                  <p className="text-sm opacity-90">v{template.os_version}</p>
                </div>

                {/* Template Details */}
                <div className="p-6 space-y-4">
                  <p className="text-sm text-gray-600">{template.description}</p>

                  {/* Default Specs */}
                  <div className="border-t border-gray-200 pt-4">
                    <h4 className="font-semibold text-gray-900 mb-3">Default Specs</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">CPU Cores</span>
                        <span className="font-medium">{template.default_cpu}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Memory</span>
                        <span className="font-medium">{template.default_memory_mb} MB</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Disk Size</span>
                        <span className="font-medium">{template.default_disk_gb} GB</span>
                      </div>
                    </div>
                  </div>

                  {/* OS Info */}
                  <div className="border-t border-gray-200 pt-4">
                    <div className="text-xs text-gray-500">
                      <p><strong>OS Type:</strong> {template.os_type}</p>
                      <p><strong>Template ID:</strong> {template.id}</p>
                    </div>
                  </div>

                  {/* Action Button */}
                  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-2 font-medium transition">
                    Use Template
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">About Templates</h3>
        <p className="text-blue-800 text-sm">
          Templates are pre-configured VM images that can be used to quickly deploy new VMs with a single click.
          Use the "Use Template" button to deploy a VM based on any template.
        </p>
      </div>
    </div>
  );
}
