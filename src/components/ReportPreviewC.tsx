import React from 'react';
import { 
  Calendar,
  Globe,
  BarChart3,
  TrendingUp,
  TrendingDown,
  Minus,
  Printer,
  Download,
  Lock,
  CheckCircle2,
  AlertCircle,
  Award,
  Target
} from 'lucide-react';
import { Button } from './ui/button';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell,
  LineChart,
  Line,
  Area,
  AreaChart
} from 'recharts';

const demandTrendData = [
  { month: 'Apr', openings: 1820 },
  { month: 'Mei', openings: 2150 },
  { month: 'Jun', openings: 2380 },
  { month: 'Jul', openings: 2590 },
  { month: 'Aug', openings: 2680 },
  { month: 'Sep', openings: 2847 },
];

const salaryDistributionData = [
  { range: '45-50k', count: 180 },
  { range: '50-55k', count: 420 },
  { range: '55-60k', count: 680 },
  { range: '60-65k', count: 890 },
  { range: '65-70k', count: 950 },
  { range: '70-75k', count: 720 },
  { range: '75-80k', count: 450 },
  { range: '80k+', count: 280 },
];

const competitorData = [
  { company: 'Booking.com', openings: 47, avgSalary: 72, growth: '+12%' },
  { company: 'Adyen', openings: 34, avgSalary: 76, growth: '+8%' },
  { company: 'Coolblue', openings: 28, avgSalary: 65, growth: '+15%' },
  { company: 'Bol.com', openings: 31, avgSalary: 68, growth: '+6%' },
  { company: 'ING', openings: 25, avgSalary: 71, growth: '+4%' },
];

export function ReportPreviewC() {
  const scrollToOrder = () => {
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="w-full bg-slate-50">
      {/* Print Actions Bar */}
      <div className="print:hidden sticky top-16 z-40 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 shadow-lg">
        <div className="max-w-4xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Printer className="w-5 h-5" />
            <div>
              <div className="text-sm">Print-geoptimaliseerde versie</div>
              <div className="text-xs opacity-90">A4 formaat • Professioneel kleurenpalet</div>
            </div>
          </div>
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={handlePrint}
              className="gap-2 bg-white/10 hover:bg-white/20 border-white/20 text-white"
            >
              <Printer className="w-4 h-4" />
              Print Preview
            </Button>
            <Button 
              size="sm"
              onClick={scrollToOrder}
              className="gap-2 bg-white text-blue-700 hover:bg-blue-50"
            >
              <Download className="w-4 h-4" />
              Download Volledig
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content - Optimized for A4 Print */}
      <div className="max-w-4xl mx-auto bg-white shadow-lg print:shadow-none print:max-w-none">
        {/* Page 1 */}
        <div className="p-12 print:p-8 min-h-screen print:min-h-0 print:page-break-after-always bg-white">
          {/* Header with Brand Colors */}
          <div className="bg-gradient-to-r from-blue-700 to-blue-800 text-white p-8 -mx-12 -mt-12 mb-8 print:-mx-8 print:-mt-8 print:bg-blue-700">
            <div className="flex items-start justify-between mb-6">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-white/20 backdrop-blur rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-7 h-7" />
                </div>
                <div>
                  <div className="text-2xl mb-1">Recruitin Intelligence</div>
                  <div className="text-sm text-blue-100">Market Research & Analytics Division</div>
                </div>
              </div>
              <div className="text-right bg-white/10 backdrop-blur rounded-lg px-4 py-3">
                <div className="text-xs text-blue-100 mb-1">Report ID</div>
                <div className="text-sm font-mono">MKT-2025-10-NL</div>
              </div>
            </div>

            <div className="border-t border-white/20 pt-6">
              <div className="text-xs text-blue-200 uppercase tracking-wider mb-3">Market Intelligence Report</div>
              <h1 className="text-4xl mb-3 leading-tight print:text-3xl">
                Senior Marketing Manager
              </h1>
              <h2 className="text-xl text-blue-100 mb-6 print:text-lg">
                Tech & Digital Sector • Nederland & DACH Region
              </h2>
              
              <div className="flex flex-wrap gap-6 text-sm text-blue-100">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  Oktober 2025
                </div>
                <div className="flex items-center gap-2">
                  <Globe className="w-4 h-4" />
                  Nederland + DACH
                </div>
                <div className="flex items-center gap-2">
                  <Award className="w-4 h-4" />
                  96.2% Betrouwbaarheid
                </div>
              </div>
            </div>
          </div>

          {/* Executive Summary with Color */}
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-4 pb-3 border-b-2 border-blue-600">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-blue-700" />
              </div>
              <h3 className="text-xl text-blue-900">Executive Summary</h3>
            </div>
            <div className="bg-blue-50 border-l-4 border-blue-600 p-6 rounded-r-lg mb-6">
              <div className="space-y-4 text-sm leading-relaxed text-slate-700">
                <p>
                  De arbeidsmarkt voor Senior Marketing Managers in de Tech & Digital sector vertoont een 
                  sterke stijgende trend met <strong className="text-blue-900">2,847 actieve vacatures</strong> per September 2025, een 
                  toename van <strong className="text-green-700">34% jaar-op-jaar</strong>. Dit wijst op een significante vraag naar 
                  marketing talent in de Nederlandse en DACH regio.
                </p>
                <p>
                  De <strong className="text-blue-900">gemiddelde kandidatenpool van 38 sollicitanten</strong> per vacature is met 12% 
                  gedaald, wat duidt op een krappe arbeidsmarkt. Dit creëert gunstige condities voor 
                  getalenteerde professionals, maar verhoogt de competitie tussen werkgevers.
                </p>
                <p>
                  Het <strong className="text-blue-900">market sweet spot salaris van €67,000</strong> ligt binnen een competitieve 
                  range van €58k-€76k. Werkgevers die binnen de <strong className="text-green-700">€64k-€68k range</strong> bieden, 
                  zien gemiddeld 23% meer gekwalificeerde sollicitaties.
                </p>
              </div>
            </div>
          </div>

          {/* Key Metrics Grid with Colors */}
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-4 pb-3 border-b-2 border-blue-600">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-blue-700" />
              </div>
              <h3 className="text-xl text-blue-900">Key Market Indicators</h3>
            </div>
            <div className="grid grid-cols-4 gap-4 print:gap-3">
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-l-4 border-green-600 p-5 rounded-r-lg print:p-3">
                <div className="text-xs text-green-700 mb-2 uppercase tracking-wide">Active Openings</div>
                <div className="text-3xl text-green-900 mb-1 print:text-2xl">2,847</div>
                <div className="flex items-center gap-1 text-xs text-green-700">
                  <TrendingUp className="w-3 h-3" />
                  +34% YoY
                </div>
              </div>
              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 border-l-4 border-blue-600 p-5 rounded-r-lg print:p-3">
                <div className="text-xs text-blue-700 mb-2 uppercase tracking-wide">Avg Candidates</div>
                <div className="text-3xl text-blue-900 mb-1 print:text-2xl">38</div>
                <div className="flex items-center gap-1 text-xs text-green-700">
                  <TrendingDown className="w-3 h-3" />
                  -12% YoY
                </div>
              </div>
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 border-l-4 border-purple-600 p-5 rounded-r-lg print:p-3">
                <div className="text-xs text-purple-700 mb-2 uppercase tracking-wide">Market Sweet Spot</div>
                <div className="text-3xl text-purple-900 mb-1 print:text-2xl">€67k</div>
                <div className="flex items-center gap-1 text-xs text-purple-700">
                  <Minus className="w-3 h-3" />
                  €58-76k
                </div>
              </div>
              <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-l-4 border-amber-600 p-5 rounded-r-lg print:p-3">
                <div className="text-xs text-amber-700 mb-2 uppercase tracking-wide">Time to Hire</div>
                <div className="text-3xl text-amber-900 mb-1 print:text-2xl">22d</div>
                <div className="flex items-center gap-1 text-xs text-green-700">
                  <TrendingDown className="w-3 h-3" />
                  -29% vs avg
                </div>
              </div>
            </div>
          </div>

          {/* Market Opportunity Score with Color */}
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-4 pb-3 border-b-2 border-blue-600">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <Award className="w-5 h-5 text-blue-700" />
              </div>
              <h3 className="text-xl text-blue-900">Market Opportunity Analysis</h3>
            </div>
            <div className="bg-gradient-to-br from-slate-50 to-blue-50 border border-blue-200 rounded-lg p-6">
              <div className="grid grid-cols-2 gap-8">
                <div className="flex items-center justify-center">
                  <div className="text-center">
                    <div className="relative w-36 h-36 mb-4">
                      <svg className="transform -rotate-90 w-36 h-36">
                        <circle
                          cx="72"
                          cy="72"
                          r="64"
                          stroke="#e0e7ff"
                          strokeWidth="12"
                          fill="none"
                        />
                        <circle
                          cx="72"
                          cy="72"
                          r="64"
                          stroke="#1e40af"
                          strokeWidth="12"
                          fill="none"
                          strokeDasharray={`${89 * 4.02} 402`}
                          strokeLinecap="round"
                        />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <div className="text-5xl text-blue-900 print:text-4xl">89</div>
                        <div className="text-sm text-blue-600">/100</div>
                      </div>
                    </div>
                    <div className="text-sm text-slate-700 mb-1">Overall Opportunity Score</div>
                    <div className="inline-block bg-green-100 text-green-800 text-xs px-3 py-1 rounded-full">
                      Zeer gunstig momentum
                    </div>
                  </div>
                </div>
                <div className="space-y-5">
                  <ScoreItem label="Demand Level" score={94} description="Extreem hoge vraag" color="green" />
                  <ScoreItem label="Talent Availability" score={78} description="Beperkte beschikbaarheid" color="amber" />
                  <ScoreItem label="Salary Competitiveness" score={92} description="Zeer competitief" color="blue" />
                  <ScoreItem label="Market Timing" score={96} description="Optimaal momentum" color="green" />
                </div>
              </div>
            </div>
          </div>

          {/* Key Insights Box */}
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-600 p-6 rounded-r-lg">
            <div className="flex items-start gap-3 mb-4">
              <CheckCircle2 className="w-6 h-6 text-green-700 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-green-900 mb-2">Belangrijkste Inzichten</h4>
                <ul className="space-y-2 text-sm text-slate-700">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 shrink-0">•</span>
                    <span>Post vacatures <strong>binnen 72 uur</strong> om optimaal momentum te benutten</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 shrink-0">•</span>
                    <span>Target <strong>€64-68k range</strong> voor 23% meer gekwalificeerde responses</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 shrink-0">•</span>
                    <span>Focus op <strong>hybrid werk</strong> (89% candidate preference in sector)</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="absolute bottom-8 left-12 right-12 flex justify-between text-xs text-slate-500 print:static print:mt-12 print:pt-4 print:border-t border-slate-200">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full" />
              Recruitin Intelligence © 2025
            </div>
            <div>Pagina 1 van 32 • Confidential Preview</div>
          </div>
        </div>

        {/* Page 2 */}
        <div className="p-12 print:p-8 min-h-screen print:min-h-0 print:page-break-after-always bg-white">
          {/* Page Header */}
          <div className="bg-blue-700 text-white px-6 py-3 -mx-12 -mt-12 mb-8 print:-mx-8 print:-mt-8 flex justify-between items-center">
            <div className="text-sm">Senior Marketing Manager • Market Intelligence</div>
            <div className="text-xs text-blue-200">Pagina 2 van 32</div>
          </div>

          {/* Demand Trend Analysis */}
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-4 pb-3 border-b-2 border-blue-600">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-blue-700" />
              </div>
              <h3 className="text-xl text-blue-900">Vraag Ontwikkeling (6 maanden)</h3>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-slate-50 border border-blue-200 rounded-lg p-6">
              <ResponsiveContainer width="100%" height={240}>
                <AreaChart data={demandTrendData}>
                  <defs>
                    <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1e40af" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#1e40af" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
                  <XAxis 
                    dataKey="month" 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <YAxis 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '2px solid #1e40af',
                      borderRadius: '8px'
                    }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="openings" 
                    stroke="#1e40af" 
                    strokeWidth={3}
                    fill="url(#colorGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
              <div className="mt-4 flex items-center justify-between text-xs">
                <span className="text-slate-600">Bronnen: LinkedIn Jobs API, Indeed Market Intelligence</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" />
                  Stijgende trend (+34%)
                </span>
              </div>
            </div>
          </div>

          {/* Salary Distribution */}
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-4 pb-3 border-b-2 border-blue-600">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-blue-700" />
              </div>
              <h3 className="text-xl text-blue-900">Salaris Distributie (n=4,570)</h3>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-slate-50 border border-purple-200 rounded-lg p-6">
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={salaryDistributionData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
                  <XAxis 
                    dataKey="range" 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <YAxis 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '2px solid #7c3aed',
                      borderRadius: '8px'
                    }}
                  />
                  <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                    {salaryDistributionData.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={index === 4 ? '#7c3aed' : '#cbd5e1'} 
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 text-xs text-slate-600">
                Bronnen: Glassdoor Salary Data, PayScale Nederland
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mt-6">
              <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded-r-lg text-center">
                <div className="text-xs text-blue-700 mb-2 uppercase tracking-wide">P25 (Entry-Mid)</div>
                <div className="text-2xl text-blue-900">€58k</div>
              </div>
              <div className="bg-purple-50 border-l-4 border-purple-600 p-4 rounded-r-lg text-center">
                <div className="text-xs text-purple-700 mb-2 uppercase tracking-wide">P50 (Median) ★</div>
                <div className="text-2xl text-purple-900">€67k</div>
              </div>
              <div className="bg-green-50 border-l-4 border-green-600 p-4 rounded-r-lg text-center">
                <div className="text-xs text-green-700 mb-2 uppercase tracking-wide">P75 (Senior)</div>
                <div className="text-2xl text-green-900">€76k</div>
              </div>
            </div>
          </div>

          {/* Competitor Table */}
          <div className="mb-10">
            <div className="flex items-center gap-3 mb-4 pb-3 border-b-2 border-blue-600">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <Award className="w-5 h-5 text-blue-700" />
              </div>
              <h3 className="text-xl text-blue-900">Top 5 Concurrenten (Preview)</h3>
            </div>
            <div className="overflow-hidden rounded-lg border-2 border-slate-200">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-blue-700 text-white">
                    <th className="text-left py-3 px-4">Bedrijf</th>
                    <th className="text-right py-3 px-4">Openings</th>
                    <th className="text-right py-3 px-4">Avg Salaris</th>
                    <th className="text-right py-3 px-4">Groei YoY</th>
                  </tr>
                </thead>
                <tbody>
                  {competitorData.map((company, idx) => (
                    <tr key={idx} className={`border-b border-slate-200 ${idx % 2 === 0 ? 'bg-slate-50' : 'bg-white'}`}>
                      <td className="py-3 px-4 text-slate-900">{company.company}</td>
                      <td className="py-3 px-4 text-right text-blue-700">{company.openings}</td>
                      <td className="py-3 px-4 text-right text-purple-700">€{company.avgSalary}k</td>
                      <td className="py-3 px-4 text-right">
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                          {company.growth}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="mt-4 bg-blue-50 border-l-4 border-blue-600 p-4 rounded-r-lg">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-blue-700 shrink-0 mt-0.5" />
                <div className="text-sm text-slate-700">
                  <strong className="text-blue-900">Volledig rapport bevat:</strong> Gedetailleerde analyses van 200+ bedrijven 
                  inclusief hiring velocity, budget allocatie, benefits packages en retention metrics.
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="absolute bottom-8 left-12 right-12 flex justify-between text-xs text-slate-500 print:static print:mt-12 print:pt-4 print:border-t border-slate-200">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-blue-600 rounded-full" />
              Recruitin Intelligence © 2025
            </div>
            <div>Pagina 2 van 32 • Confidential Preview</div>
          </div>
        </div>

        {/* Page 3 - Locked Content Preview */}
        <div className="p-12 print:p-8 min-h-screen print:hidden bg-white">
          <div className="bg-blue-700 text-white px-6 py-3 -mx-12 -mt-12 mb-8 flex justify-between items-center">
            <div className="text-sm">Senior Marketing Manager • Market Intelligence</div>
            <div className="text-xs text-blue-200">Pagina 3 van 32</div>
          </div>

          <div className="border-2 border-blue-200 rounded-lg p-12 bg-gradient-to-br from-blue-50 to-slate-50 min-h-[600px] flex items-center justify-center">
            <div>
              <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Lock className="w-12 h-12 text-blue-700" />
              </div>
              <h3 className="text-3xl text-blue-900 mb-4 text-center">Nog 30 pagina's diepgaande analyse</h3>
              <p className="text-slate-600 mb-10 max-w-2xl mx-auto text-center leading-relaxed">
                Het volledige rapport bevat uitgebreide strategische aanbevelingen, geografische heatmaps, 
                skills matrices, channel ROI analyses en 12-maanden forecasts met scenario planning.
              </p>

              <div className="grid grid-cols-2 gap-4 max-w-3xl mx-auto mb-10">
                <LockedFeature icon={CheckCircle2} text="Complete salary benchmarks (P10-P90)" color="blue" />
                <LockedFeature icon={CheckCircle2} text="200+ concurrent analyses & profiles" color="purple" />
                <LockedFeature icon={CheckCircle2} text="Skills gap analyse (50+ competenties)" color="green" />
                <LockedFeature icon={CheckCircle2} text="12-maanden market forecast & trends" color="amber" />
                <LockedFeature icon={CheckCircle2} text="Geografische heatmaps per regio" color="blue" />
                <LockedFeature icon={CheckCircle2} text="Interview frameworks & templates" color="purple" />
              </div>

              <div className="text-center mb-8">
                <div className="inline-block bg-white rounded-lg shadow-lg p-8">
                  <div className="text-5xl text-blue-900 mb-2">€59</div>
                  <div className="text-sm text-slate-600 mb-4">Eenmalige investering • Lifetime toegang</div>
                  <div className="flex items-center justify-center gap-4 text-xs text-slate-500">
                    <div className="flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-green-600" />
                      PDF + Print formaat
                    </div>
                    <div className="flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-green-600" />
                      30 dagen updates
                    </div>
                  </div>
                </div>
              </div>

              <div className="text-center">
                <Button 
                  onClick={scrollToOrder}
                  size="lg"
                  className="bg-blue-700 hover:bg-blue-800 px-10 h-14 text-lg"
                >
                  <Download className="w-5 h-5 mr-2" />
                  Download Volledig Rapport (32 Pagina's)
                </Button>
              </div>

              <div className="mt-8 text-center text-xs text-slate-500">
                <div className="mb-3">Real-time data integraties:</div>
                <div className="flex flex-wrap justify-center gap-3">
                  <span className="bg-white px-3 py-1 rounded-full">LinkedIn API</span>
                  <span className="bg-white px-3 py-1 rounded-full">Glassdoor</span>
                  <span className="bg-white px-3 py-1 rounded-full">Indeed</span>
                  <span className="bg-white px-3 py-1 rounded-full">CBS</span>
                  <span className="bg-white px-3 py-1 rounded-full">UWV</span>
                  <span className="bg-white px-3 py-1 rounded-full">PayScale</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ScoreItem({ label, score, description, color }: { label: string; score: number; description: string; color: string }) {
  const colorMap = {
    green: { bg: 'bg-green-600', text: 'text-green-700', lightBg: 'bg-green-100' },
    blue: { bg: 'bg-blue-600', text: 'text-blue-700', lightBg: 'bg-blue-100' },
    amber: { bg: 'bg-amber-600', text: 'text-amber-700', lightBg: 'bg-amber-100' },
    purple: { bg: 'bg-purple-600', text: 'text-purple-700', lightBg: 'bg-purple-100' },
  };

  const colors = colorMap[color as keyof typeof colorMap] || colorMap.blue;

  return (
    <div>
      <div className="flex justify-between items-center text-xs mb-2">
        <span className="text-slate-700">{label}</span>
        <span className={`${colors.text} font-semibold`}>{score}/100</span>
      </div>
      <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
        <div 
          className={`h-full ${colors.bg} rounded-full transition-all duration-500`}
          style={{ width: `${score}%` }}
        />
      </div>
      <div className={`text-xs ${colors.text} mt-1.5`}>{description}</div>
    </div>
  );
}

function LockedFeature({ icon: Icon, text, color }: { icon: any; text: string; color: string }) {
  const colorMap = {
    green: 'from-green-50 to-emerald-50 border-green-200 text-green-900',
    blue: 'from-blue-50 to-cyan-50 border-blue-200 text-blue-900',
    purple: 'from-purple-50 to-pink-50 border-purple-200 text-purple-900',
    amber: 'from-amber-50 to-orange-50 border-amber-200 text-amber-900',
  };

  const iconColor = {
    green: 'text-green-600',
    blue: 'text-blue-600',
    purple: 'text-purple-600',
    amber: 'text-amber-600',
  };

  return (
    <div className={`bg-gradient-to-br ${colorMap[color as keyof typeof colorMap]} border rounded-lg p-4 flex items-start gap-3`}>
      <Icon className={`w-5 h-5 ${iconColor[color as keyof typeof iconColor]} shrink-0 mt-0.5`} />
      <span className="text-sm leading-snug">{text}</span>
    </div>
  );
}