import React from 'react';
import { 
  Calendar,
  Globe,
  BarChart3,
  TrendingUp,
  TrendingDown,
  Clock,
  Printer,
  Download
} from 'lucide-react';
import { Button } from './ui/button';

export function ReportPreviewA() {
  const handlePrint = () => {
    window.print();
  };

  const scrollToOrder = () => {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  };

  return (
    <div className="w-full bg-gray-50 min-h-screen">
      {/* Print Actions Bar */}
      <div className="print:hidden sticky top-0 z-40 bg-white border-b border-gray-200 py-4">
        <div className="max-w-6xl mx-auto px-6 flex items-center justify-between">
          <div className="text-sm text-gray-600">Versie A - Classic Report</div>
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={handlePrint}
              className="gap-2"
            >
              <Printer className="w-4 h-4" />
              Print Preview
            </Button>
            <Button 
              size="sm"
              onClick={scrollToOrder}
              className="gap-2 bg-blue-600 hover:bg-blue-700"
            >
              <Download className="w-4 h-4" />
              Download Volledig
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto bg-white print:shadow-none">
        {/* Header Section - Dark Blue like Figma */}
        <div className="bg-slate-800 text-white px-8 py-12">
          <div className="flex items-start justify-between mb-8">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6" />
              </div>
              <div>
                <div className="text-xl mb-1">Recruitin Intelligence</div>
                <div className="text-sm text-slate-300">Powered by 15+ real-time APIs</div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-light mb-1">96.2%</div>
              <div className="text-sm text-slate-300">Data betrouwbaarheid</div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-light mb-1">4,570</div>
              <div className="text-sm text-slate-300">Vacatures geanalyseerd</div>
            </div>
          </div>

          <div className="mb-6">
            <div className="inline-block bg-blue-600 text-white text-sm px-3 py-1 rounded mb-4">
              Market Intelligence Report
            </div>
            <h1 className="text-4xl font-light mb-2 leading-tight">
              Senior Marketing Manager
            </h1>
            <h2 className="text-xl text-slate-300 mb-6">
              Tech & Digital Sector
            </h2>
            <p className="text-slate-300 max-w-2xl">
              Comprehensive hiring intelligence voor de Nederlandse en DACH arbeidsmarkt
            </p>
          </div>
          
          <div className="flex flex-wrap gap-8 text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Gegenereerd: Oktober 2025
            </div>
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4" />
              Regio: Nederland + DACH
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Laatste update: 2 uur geleden
            </div>
          </div>
        </div>

        {/* Markt Overview Section */}
        <div className="p-8">
          <div className="mb-8">
            <h3 className="text-2xl text-slate-800 mb-2">Markt Overview</h3>
            <p className="text-gray-600">Real-time arbeidsmarkt indicatoren (laatste 6 maanden)</p>
          </div>

          {/* Metrics Cards - Clean White Design like Figma */}
          <div className="grid grid-cols-4 gap-6 mb-12">
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm text-gray-600">Active Openings</div>
                <div className="flex items-center text-green-600 text-sm">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  +34%
                </div>
              </div>
              <div className="text-3xl font-light text-slate-800 mb-1">2,847</div>
              <div className="text-sm text-gray-500">vs 2,124 vorig jaar (Q3 2024)</div>
              <div className="mt-3 h-1 bg-gray-200 rounded-full">
                <div className="h-1 bg-green-500 rounded-full" style={{ width: '75%' }}></div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm text-gray-600">Avg Candidates</div>
                <div className="flex items-center text-red-600 text-sm">
                  <TrendingDown className="w-4 h-4 mr-1" />
                  -12%
                </div>
              </div>
              <div className="text-3xl font-light text-slate-800 mb-1">38</div>
              <div className="text-sm text-gray-500">per vacature (gunstige ratio)</div>
              <div className="mt-3 h-1 bg-gray-200 rounded-full">
                <div className="h-1 bg-blue-500 rounded-full" style={{ width: '60%' }}></div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm text-gray-600">Market Sweet Spot</div>
                <div className="flex items-center text-blue-600 text-sm">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  +6%
                </div>
              </div>
              <div className="text-3xl font-light text-slate-800 mb-1">€67K</div>
              <div className="text-sm text-gray-500">Range: €58k - €76k (80th percentile)</div>
              <div className="mt-3 h-1 bg-gray-200 rounded-full">
                <div className="h-1 bg-purple-500 rounded-full" style={{ width: '85%' }}></div>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm text-gray-600">Days to Hire</div>
                <div className="flex items-center text-green-600 text-sm">
                  <TrendingDown className="w-4 h-4 mr-1" />
                  -29%
                </div>
              </div>
              <div className="text-3xl font-light text-slate-800 mb-1">22</div>
              <div className="text-sm text-gray-500">Industry average: 31 dagen</div>
              <div className="mt-3 h-1 bg-gray-200 rounded-full">
                <div className="h-1 bg-green-500 rounded-full" style={{ width: '70%' }}></div>
              </div>
            </div>
          </div>

          {/* Simple Download Section */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-12 text-center">
            <h3 className="text-2xl text-slate-800 mb-4">Download Volledig Rapport</h3>
            <p className="text-gray-600 mb-8">
              32 pagina's met complete analyse, strategische aanbevelingen en markt insights.
            </p>
            
            <div className="bg-white rounded-lg shadow-sm p-8 inline-block mb-8">
              <div className="text-4xl text-slate-800 mb-2">€59</div>
              <div className="text-gray-600 mb-4">Eenmalige investering • Lifetime toegang</div>
            </div>

            <div>
              <Button 
                onClick={scrollToOrder}
                size="lg"
                className="bg-blue-600 hover:bg-blue-700 px-10 py-4 text-lg"
              >
                <Download className="w-5 h-5 mr-2" />
                Download Volledig Rapport
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}