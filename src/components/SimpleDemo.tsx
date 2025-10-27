import React from 'react';
import { ReportTemplate } from './ReportTemplate';

interface SimpleDemoProps {
  onOrderClick?: () => void;
}

export function SimpleDemo({ onOrderClick }: SimpleDemoProps) {
  return (
    <ReportTemplate 
      data={undefined}
      variant="demo"
      onOrderClick={onOrderClick}
    />
  );
}