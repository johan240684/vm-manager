import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Server, Package, Activity, Menu, X } from 'lucide-react';

export default function Sidebar({ isOpen, onToggle }) {
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/vms', label: 'Virtual Machines', icon: Server },
    { path: '/templates', label: 'Templates', icon: Package },
    { path: '/monitoring', label: 'Monitoring', icon: Activity },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <>
      {/* Sidebar */}
      <div
        className={`${
          isOpen ? 'w-64' : 'w-20'
        } bg-gray-900 text-white transition-all duration-300 flex flex-col`}
      >
        {/* Logo */}
        <div className="p-4 flex items-center justify-between">
          {isOpen && <h2 className="text-xl font-bold">VM Manager</h2>}
          <button
            onClick={onToggle}
            className="p-2 hover:bg-gray-800 rounded-lg"
          >
            {isOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Menu */}
        <nav className="flex-1 px-4 py-8">
          <div className="space-y-2">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-4 px-4 py-3 rounded-lg transition-colors ${
                  isActive(item.path)
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
                title={!isOpen ? item.label : ''}
              >
                <item.icon size={20} />
                {isOpen && <span>{item.label}</span>}
              </Link>
            ))}
          </div>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-gray-800">
          <div className="text-xs text-gray-500">
            {isOpen && <p>© 2024 VM Manager</p>}
          </div>
        </div>
      </div>
    </>
  );
}
