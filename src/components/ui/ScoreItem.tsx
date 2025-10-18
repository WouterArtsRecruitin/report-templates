import React from 'react';

interface ScoreItemProps {
  label: string;
  score: number;
  description: string;
  color?: 'green' | 'blue' | 'amber' | 'purple';
}

export function ScoreItem({ label, score, description, color = 'blue' }: ScoreItemProps) {
  const colorMap = {
    green: { bg: 'bg-green-600', text: 'text-green-700', lightBg: 'bg-green-100' },
    blue: { bg: 'bg-blue-600', text: 'text-blue-700', lightBg: 'bg-blue-100' },
    amber: { bg: 'bg-amber-600', text: 'text-amber-700', lightBg: 'bg-amber-100' },
    purple: { bg: 'bg-purple-600', text: 'text-purple-700', lightBg: 'bg-purple-100' },
  };

  const colors = colorMap[color];

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