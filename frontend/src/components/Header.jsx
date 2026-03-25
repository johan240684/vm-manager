import React from 'react';
import { Menu, Bell, Settings, LogOut } from 'lucide-react';

export default function Header({ user = {} }) {
  return (
    <header className="bg-white shadow">
      <div className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-gray-900">VM Manager</h1>
        </div>

        <div className="flex items-center gap-4">
          {/* Notifications */}
          <button className="p-2 text-gray-600 hover:text-gray-900">
            <Bell size={20} />
          </button>

          {/* Settings */}
          <button className="p-2 text-gray-600 hover:text-gray-900">
            <Settings size={20} />
          </button>

          {/* User Menu */}
          <div className="flex items-center gap-3 pl-4 border-l border-gray-200">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">
                {user.name || 'Admin'}
              </p>
              <p className="text-xs text-gray-500">Administrator</p>
            </div>
            <button className="p-2 text-gray-600 hover:text-gray-900">
              <LogOut size={20} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
