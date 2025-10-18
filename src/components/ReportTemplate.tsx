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
  Lock
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
  Line
} from 'recharts';
import { ReportProps } from '../types/report';

export function ReportTemplate({ data, variant, onOrderClick, showPrintControls = true }: ReportProps) {
  const scrollToOrder = () => {
    if (onOrderClick) {
      onOrderClick();
    } else {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const isDemoMode = variant === 'demo';

  return (
    <div className="w-full bg-white">
      {/* Print Actions Bar */}
      {showPrintControls && (
        <div className="print:hidden sticky top-16 z-40 bg-slate-100 border-b border-slate-200 py-3">
          <div className="max-w-4xl mx-auto px-6 flex items-center justify-between">
            <div className="text-sm text-slate-600">Print-geoptimaliseerde versie • A4 formaat</div>
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
                className="gap-2 bg-slate-900 hover:bg-slate-800"
              >
                <Download className="w-4 h-4" />
                {isDemoMode ? 'Download Volledig Rapport' : 'Download Rapport'}
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content - Optimized for A4 Print */}
      <div className="max-w-4xl mx-auto bg-white print:max-w-none">
        {/* Page 1 */}
        <div className="p-12 print:p-8 min-h-screen print:min-h-0 print:page-break-after-always">
          {/* Header */}
          <div className="border-b-2 border-slate-900 pb-6 mb-8">
            <div className="flex items-start justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-slate-900 rounded flex items-center justify-center print:bg-black">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
                <div>
                  <div className="text-xl">{data.config.companyName}</div>
                  {data.config.division && (
                    <div className="text-xs text-slate-600">{data.config.division}</div>
                  )}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-slate-500 mb-1">Report ID</div>
                <div className="text-sm font-mono">{data.config.reportId}</div>
              </div>
            </div>

            <div className="mb-4">
              <div className="text-xs text-slate-500 uppercase tracking-wider mb-2">Market Intelligence Report</div>
              <h1 className="text-4xl mb-3 leading-tight print:text-3xl">
                {data.config.title}
              </h1>
              <h2 className="text-xl text-slate-600 print:text-lg">
                {data.config.subtitle}
              </h2>
            </div>

            <div className="flex gap-8 text-sm text-slate-600">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                {data.config.date}
              </div>
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4" />
                {data.config.region}
              </div>
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                {data.config.reliabilityScore}% Betrouwbaarheid
              </div>
            </div>
          </div>

          {/* Executive Summary */}
          <div className="mb-10">
            <h3 className="text-lg mb-4 pb-2 border-b border-slate-200">Executive Summary</h3>
            <div className="space-y-3 text-sm leading-relaxed text-slate-700">
              {data.executiveSummary.paragraphs.map((paragraph, index) => (
                <p key={index} dangerouslySetInnerHTML={{ __html: paragraph }} />
              ))}
            </div>
          </div>

          {/* Key Metrics Grid */}
          <div className="mb-10">
            <h3 className="text-lg mb-4 pb-2 border-b border-slate-200">Key Market Indicators</h3>
            <div className="grid grid-cols-4 gap-4 print:gap-3">
              <div className="border border-slate-200 p-4 print:p-3">
                <div className="text-xs text-slate-500 mb-2">Active Openings</div>
                <div className="text-3xl mb-1 print:text-2xl">{data.metrics.activeOpenings.toLocaleString()}</div>
                <div className="flex items-center gap-1 text-xs text-green-700">
                  <TrendingUp className="w-3 h-3" />
                  {data.metrics.openingsGrowth}
                </div>
              </div>
              <div className="border border-slate-200 p-4 print:p-3">
                <div className="text-xs text-slate-500 mb-2">Avg Candidates</div>
                <div className="text-3xl mb-1 print:text-2xl">{data.metrics.avgCandidates}</div>
                <div className="flex items-center gap-1 text-xs text-green-700">
                  <TrendingDown className="w-3 h-3" />
                  {data.metrics.candidatesGrowth}
                </div>
              </div>
              <div className="border border-slate-200 p-4 print:p-3">
                <div className="text-xs text-slate-500 mb-2">Market Sweet Spot</div>
                <div className="text-3xl mb-1 print:text-2xl">€{data.metrics.marketSweetSpot}k</div>
                <div className="flex items-center gap-1 text-xs text-slate-700">
                  <Minus className="w-3 h-3" />
                  €{data.metrics.salaryRange.min}-{data.metrics.salaryRange.max}k
                </div>
              </div>
              <div className="border border-slate-200 p-4 print:p-3">
                <div className="text-xs text-slate-500 mb-2">Time to Hire</div>
                <div className="text-3xl mb-1 print:text-2xl">{data.metrics.timeToHire}d</div>
                <div className="flex items-center gap-1 text-xs text-green-700">
                  <TrendingDown className="w-3 h-3" />
                  {data.metrics.timeToHireChange}
                </div>
              </div>
            </div>
          </div>

          {/* Market Opportunity Score */}
          <div className="mb-10">
            <h3 className="text-lg mb-4 pb-2 border-b border-slate-200">Market Opportunity Analysis</h3>
            <div className="grid grid-cols-2 gap-6">
              <div className="flex items-center justify-center">
                <div className="text-center">
                  <div className="w-32 h-32 rounded-full border-8 border-slate-900 flex items-center justify-center mb-3 print:border-4">
                    <div>
                      <div className="text-4xl print:text-3xl">{data.opportunityScore.overall}</div>
                      <div className="text-xs text-slate-500">/100</div>
                    </div>
                  </div>
                  <div className="text-sm text-slate-700">Overall Opportunity Score</div>
                  <div className="text-xs text-slate-500 mt-1">
                    {data.opportunityScore.overall >= 80 ? 'Zeer gunstig momentum' : 
                     data.opportunityScore.overall >= 60 ? 'Gunstig momentum' : 
                     'Neutraal momentum'}
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <ScoreItem 
                  label="Demand Level" 
                  score={data.opportunityScore.demandLevel} 
                  description={data.opportunityScore.demandLevel >= 90 ? 'Extreem hoge vraag' : 'Hoge vraag'} 
                />
                <ScoreItem 
                  label="Talent Availability" 
                  score={data.opportunityScore.talentAvailability} 
                  description={data.opportunityScore.talentAvailability >= 80 ? 'Goede beschikbaarheid' : 'Beperkte beschikbaarheid'} 
                />
                <ScoreItem 
                  label="Salary Competitiveness" 
                  score={data.opportunityScore.salaryCompetitiveness} 
                  description={data.opportunityScore.salaryCompetitiveness >= 90 ? 'Zeer competitief' : 'Competitief'} 
                />
                <ScoreItem 
                  label="Market Timing" 
                  score={data.opportunityScore.marketTiming} 
                  description={data.opportunityScore.marketTiming >= 90 ? 'Optimaal momentum' : 'Goed momentum'} 
                />
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="absolute bottom-8 left-12 right-12 flex justify-between text-xs text-slate-500 print:static print:mt-8 print:pt-4 print:border-t border-slate-200">
            <div>{data.config.companyName} © 2025</div>
            <div>
              Pagina 1 van {data.config.totalPages}
              {isDemoMode && ' • Demo Preview'}
            </div>
          </div>
        </div>

        {/* Page 2 */}
        <div className="p-12 print:p-8 min-h-screen print:min-h-0 print:page-break-after-always">
          {/* Page Header */}
          <div className="flex justify-between items-center mb-8 pb-3 border-b border-slate-200">
            <div className="text-sm text-slate-600">{data.config.title} • Market Intelligence</div>
            <div className="text-xs text-slate-500">Pagina 2 van {data.config.totalPages}</div>
          </div>

          {/* Demand Trend Analysis */}
          <div className="mb-10">
            <h3 className="text-lg mb-4 pb-2 border-b border-slate-200">Vraag Ontwikkeling (6 maanden)</h3>
            <div className="border border-slate-200 p-4 bg-slate-50 print:bg-white">
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={data.chartData.demandTrend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    dataKey="month" 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <YAxis 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="openings" 
                    stroke="#000000" 
                    strokeWidth={2}
                    dot={{ fill: '#000000', r: 3 }}
                  />
                </LineChart>
              </ResponsiveContainer>
              <div className="mt-3 text-xs text-slate-500">
                Bronnen: LinkedIn Jobs API, Indeed Market Intelligence
              </div>
            </div>
          </div>

          {/* Salary Distribution */}
          <div className="mb-10">
            <h3 className="text-lg mb-4 pb-2 border-b border-slate-200">
              Salaris Distributie (n={data.chartData.salaryDistribution.reduce((sum, item) => sum + item.count, 0).toLocaleString()})
            </h3>
            <div className="border border-slate-200 p-4 bg-slate-50 print:bg-white">
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={data.chartData.salaryDistribution}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    dataKey="range" 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <YAxis 
                    tick={{ fontSize: 11, fill: '#64748b' }} 
                    axisLine={{ stroke: '#94a3b8' }}
                  />
                  <Bar dataKey="count" radius={[2, 2, 0, 0]}>
                    {data.chartData.salaryDistribution.map((entry, index) => {
                      const isHighlight = entry.range.includes(`${data.metrics.marketSweetSpot}`);
                      return (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={isHighlight ? '#000000' : '#cbd5e1'} 
                        />
                      );
                    })}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-3 text-xs text-slate-500">
                Bronnen: Glassdoor Salary Data, PayScale Nederland
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="border border-slate-200 p-3 text-center">
                <div className="text-xs text-slate-500 mb-1">P25 (Entry-Mid)</div>
                <div className="text-xl">€{data.metrics.salaryRange.min}k</div>
              </div>
              <div className="border border-slate-900 p-3 text-center bg-slate-50 print:bg-gray-100">
                <div className="text-xs text-slate-700 mb-1">P50 (Median)</div>
                <div className="text-xl">€{data.metrics.marketSweetSpot}k</div>
              </div>
              <div className="border border-slate-200 p-3 text-center">
                <div className="text-xs text-slate-500 mb-1">P75 (Senior)</div>
                <div className="text-xl">€{data.metrics.salaryRange.max}k</div>
              </div>
            </div>
          </div>

          {/* Competitor Table */}
          <div className="mb-10">
            <h3 className="text-lg mb-4 pb-2 border-b border-slate-200">
              Top {data.chartData.competitors.length} Concurrenten {isDemoMode && '(Preview)'}
            </h3>
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="border-b-2 border-slate-900">
                  <th className="text-left py-2 px-3 text-slate-700">Bedrijf</th>
                  <th className="text-right py-2 px-3 text-slate-700">Openings</th>
                  <th className="text-right py-2 px-3 text-slate-700">Avg Salaris</th>
                  <th className="text-right py-2 px-3 text-slate-700">Groei YoY</th>
                </tr>
              </thead>
              <tbody>
                {data.chartData.competitors.map((company, idx) => (
                  <tr key={idx} className="border-b border-slate-200">
                    <td className="py-2 px-3">{company.company}</td>
                    <td className="py-2 px-3 text-right">{company.openings}</td>
                    <td className="py-2 px-3 text-right">€{company.avgSalary}k</td>
                    <td className="py-2 px-3 text-right text-green-700">{company.growth}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {isDemoMode && (
              <div className="mt-3 text-xs text-slate-500 italic">
                Volledig rapport bevat 200+ bedrijven met gedetailleerde analyses
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="absolute bottom-8 left-12 right-12 flex justify-between text-xs text-slate-500 print:static print:mt-8 print:pt-4 print:border-t border-slate-200">
            <div>{data.config.companyName} © 2025</div>
            <div>
              Pagina 2 van {data.config.totalPages}
              {isDemoMode && ' • Demo Preview'}
            </div>
          </div>
        </div>

        {/* Demo Mode: Locked Content Preview */}
        {isDemoMode && (
          <div className="p-12 print:p-8 min-h-screen print:hidden">
            <div className="flex justify-between items-center mb-8 pb-3 border-b border-slate-200">
              <div className="text-sm text-slate-600">{data.config.title} • Market Intelligence</div>
              <div className="text-xs text-slate-500">Pagina 3 van {data.config.totalPages}</div>
            </div>

            <div className="border-2 border-slate-300 rounded p-12 text-center bg-slate-50 min-h-[600px] flex items-center justify-center">
              <div>
                <div className="w-20 h-20 bg-slate-200 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Lock className="w-10 h-10 text-slate-500" />
                </div>
                <h3 className="text-2xl mb-4">Nog {data.config.totalPages - data.config.previewPages} pagina's vergrendeld</h3>
                <p className="text-slate-600 mb-8 max-w-xl mx-auto">
                  Het volledige rapport bevat diepgaande analyses, strategische aanbevelingen, 
                  geografische heatmaps, skills matrices en 12-maanden forecasts.
                </p>

                <div className="grid grid-cols-2 gap-4 max-w-2xl mx-auto mb-8 text-left text-sm">
                  <div className="border border-slate-200 bg-white p-4">
                    <div className="mb-1">✓ Complete salary benchmarks (P10-P90)</div>
                  </div>
                  <div className="border border-slate-200 bg-white p-4">
                    <div className="mb-1">✓ 200+ concurrent analyses</div>
                  </div>
                  <div className="border border-slate-200 bg-white p-4">
                    <div className="mb-1">✓ Skills gap analyse (50+ competenties)</div>
                  </div>
                  <div className="border border-slate-200 bg-white p-4">
                    <div className="mb-1">✓ 12-maanden market forecast</div>
                  </div>
                  <div className="border border-slate-200 bg-white p-4">
                    <div className="mb-1">✓ Geografische heatmaps</div>
                  </div>
                  <div className="border border-slate-200 bg-white p-4">
                    <div className="mb-1">✓ Interview frameworks & templates</div>
                  </div>
                </div>

                <div className="mb-6">
                  <div className="text-4xl mb-2">{data.config.currency}{data.config.price}</div>
                  <div className="text-sm text-slate-600">Eenmalige investering • Print + Digital formaat</div>
                </div>

                <Button 
                  onClick={scrollToOrder}
                  size="lg"
                  className="bg-slate-900 hover:bg-slate-800 px-8 h-12"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Download Volledig Rapport (PDF + Printable)
                </Button>

                <div className="mt-6 text-xs text-slate-500">
                  <div className="mb-2">✓ Instant download • ✓ PDF + Editable formaat • ✓ 30 dagen updates</div>
                  <div>Real-time data van: LinkedIn API • Glassdoor • Indeed • CBS • UWV • PayScale</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function ScoreItem({ label, score, description }: { label: string; score: number; description: string }) {
  return (
    <div>
      <div className="flex justify-between items-center text-xs mb-1">
        <span className="text-slate-600">{label}</span>
        <span className="text-slate-900">{score}/100</span>
      </div>
      <div className="h-2 bg-slate-200 rounded-full overflow-hidden print:h-1.5">
        <div 
          className="h-full bg-slate-900 rounded-full print:bg-black"
          style={{ width: `${score}%` }}
        />
      </div>
      <div className="text-xs text-slate-500 mt-1">{description}</div>
    </div>
  );
}