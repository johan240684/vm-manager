import React from 'react';

const colorClasses = {
  blue: 'bg-blue-50 text-blue-700 border-blue-200',
  green: 'bg-green-50 text-green-700 border-green-200',
  red: 'bg-red-50 text-red-700 border-red-200',
  purple: 'bg-purple-50 text-purple-700 border-purple-200',
  gray: 'bg-gray-50 text-gray-700 border-gray-200',
};

const iconColorClasses = {
  blue: 'text-blue-600',
  green: 'text-green-600',
  red: 'text-red-600',
  purple: 'text-purple-600',
  gray: 'text-gray-600',
};

export default function StatCard({ title, value, icon: Icon, color = 'blue' }) {
  return (
    <div className={`rounded-lg border p-6 ${colorClasses[color]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium opacity-70">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <Icon size={32} className={`opacity-50 ${iconColorClasses[color]}`} />
      </div>
    </div>
  );
}
