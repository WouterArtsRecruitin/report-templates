import React from 'react';
import { LucideIcon } from 'lucide-react';

interface LockedFeatureProps {
  icon: LucideIcon;
  text: string;
  color?: 'green' | 'blue' | 'purple' | 'amber';
}

export function LockedFeature({ icon: Icon, text, color = 'blue' }: LockedFeatureProps) {
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
    <div className={`bg-gradient-to-br ${colorMap[color]} border rounded-lg p-4 flex items-start gap-3`}>
      <Icon className={`w-5 h-5 ${iconColor[color]} shrink-0 mt-0.5`} />
      <span className="text-sm leading-snug">{text}</span>
    </div>
  );
}