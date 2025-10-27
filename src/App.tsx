import React, { useState } from 'react';
import { ReportPreviewA } from './components/ReportPreviewA';
import { ReportPreviewB } from './components/ReportPreviewB';
import { ReportPreviewC } from './components/ReportPreviewC';

export default function App() {
  const [version, setVersion] = useState<'a' | 'b' | 'c'>('a');

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Version Switcher */}
      <div className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm print:hidden">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="text-sm text-slate-600">A/B/C Test Varianten</div>
            <div className="flex gap-2">
              <button
                onClick={() => setVersion('a')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'a'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie A - Classic Report
              </button>
              <button
                onClick={() => setVersion('b')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'b'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie B - Interactive Dashboard
              </button>
              <button
                onClick={() => setVersion('c')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'c'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie C - Printable Report
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      {version === 'a' ? <ReportPreviewA /> : version === 'b' ? <ReportPreviewB /> : <ReportPreviewC />}
    </div>
  );
}