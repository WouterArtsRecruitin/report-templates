import React from 'react';
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
  PieChart,
  Pie,
  Area,
  AreaChart
} from 'recharts';

interface ChartProps {
  data: any[];
  height?: number;
  className?: string;
}

// Demand Trend Line Chart
export function DemandTrendChart({ data, height = 200, className = "" }: ChartProps) {
  return (
    <div className={`border border-slate-200 p-4 bg-slate-50 print:bg-white ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data}>
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
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#ffffff', 
              border: '1px solid #e5e7eb',
              borderRadius: '4px',
              fontSize: '12px'
            }}
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
  );
}

// Salary Distribution Bar Chart
interface SalaryChartProps extends ChartProps {
  highlightValue?: number;
}

export function SalaryDistributionChart({ data, highlightValue, height = 200, className = "" }: SalaryChartProps) {
  return (
    <div className={`border border-slate-200 p-4 bg-slate-50 print:bg-white ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data}>
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
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#ffffff', 
              border: '1px solid #e5e7eb',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          />
          <Bar dataKey="count" radius={[2, 2, 0, 0]}>
            {data.map((entry, index) => {
              const isHighlight = highlightValue && entry.range.includes(`${highlightValue}`);
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
  );
}

// Area Chart for Growth Trends
export function GrowthTrendChart({ data, height = 200, className = "" }: ChartProps) {
  return (
    <div className={`border border-slate-200 p-4 bg-slate-50 print:bg-white ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <AreaChart data={data}>
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
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#ffffff', 
              border: '1px solid #e5e7eb',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          />
          <Area 
            type="monotone" 
            dataKey="value" 
            stroke="#000000" 
            fill="#f1f5f9"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

// Skills Distribution Pie Chart
export function SkillsDistributionChart({ data, height = 200, className = "" }: ChartProps) {
  const COLORS = ['#000000', '#374151', '#6b7280', '#9ca3af', '#d1d5db'];
  
  return (
    <div className={`border border-slate-200 p-4 bg-slate-50 print:bg-white ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            outerRadius={60}
            fill="#8884d8"
            dataKey="value"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

// Competitor Comparison Chart
export function CompetitorChart({ data, height = 250, className = "" }: ChartProps) {
  return (
    <div className={`border border-slate-200 p-4 bg-slate-50 print:bg-white ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} layout="horizontal">
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            type="number"
            tick={{ fontSize: 11, fill: '#64748b' }} 
            axisLine={{ stroke: '#94a3b8' }}
          />
          <YAxis 
            type="category"
            dataKey="company"
            tick={{ fontSize: 11, fill: '#64748b' }} 
            axisLine={{ stroke: '#94a3b8' }}
            width={100}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#ffffff', 
              border: '1px solid #e5e7eb',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          />
          <Bar 
            dataKey="avgSalary" 
            fill="#cbd5e1" 
            radius={[0, 2, 2, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// Multi-metric Dashboard Chart
interface MultiMetricChartProps {
  data: {
    metrics: Array<{
      name: string;
      current: number;
      previous: number;
      target?: number;
    }>;
  };
  height?: number;
  className?: string;
}

export function MultiMetricChart({ data, height = 300, className = "" }: MultiMetricChartProps) {
  const chartData = data.metrics.map(metric => ({
    name: metric.name,
    current: metric.current,
    previous: metric.previous,
    target: metric.target || metric.current * 1.1
  }));

  return (
    <div className={`border border-slate-200 p-4 bg-slate-50 print:bg-white ${className}`}>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="name" 
            tick={{ fontSize: 10, fill: '#64748b' }} 
            axisLine={{ stroke: '#94a3b8' }}
          />
          <YAxis 
            tick={{ fontSize: 11, fill: '#64748b' }} 
            axisLine={{ stroke: '#94a3b8' }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#ffffff', 
              border: '1px solid #e5e7eb',
              borderRadius: '4px',
              fontSize: '12px'
            }}
          />
          <Bar dataKey="previous" fill="#e5e7eb" name="Vorige periode" />
          <Bar dataKey="current" fill="#000000" name="Huidige periode" />
          <Bar dataKey="target" fill="#94a3af" name="Target" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}