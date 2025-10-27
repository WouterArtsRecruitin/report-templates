import React from 'react';

export function ReportPreviewB() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="text-center p-12">
        <h2 className="text-3xl font-bold text-slate-800 mb-4">Versie B - Interactive Dashboard</h2>
        <p className="text-slate-600 mb-8">Deze versie is in ontwikkeling.</p>
        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
          <span className="text-2xl">📊</span>
        </div>
      </div>
    </div>
  );
}