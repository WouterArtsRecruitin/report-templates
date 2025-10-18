import React from 'react';
import { ReportTemplate } from './ReportTemplate';
import { ReportData } from '../types/report';

interface ProfessionalReportProps {
  data: ReportData;
  showPrintControls?: boolean;
  onDownloadClick?: () => void;
}

export function ProfessionalReport({ 
  data, 
  showPrintControls = false,
  onDownloadClick 
}: ProfessionalReportProps) {
  return (
    <ReportTemplate 
      data={data}
      variant="professional"
      onOrderClick={onDownloadClick}
      showPrintControls={showPrintControls}
    />
  );
}

// Helper function to create professional report data
export function createProfessionalReportData(overrides: Partial<ReportData> = {}): ReportData {
  const baseData: ReportData = {
    config: {
      title: "Professional Position Analysis",
      subtitle: "Market Intelligence Report",
      sector: "Technology",
      region: "Nederland",
      reportId: "PRO-2025-001",
      date: new Date().toLocaleDateString('nl-NL', { 
        year: 'numeric', 
        month: 'long' 
      }),
      companyName: "Professional Intelligence",
      division: "Market Research",
      totalPages: 45,
      previewPages: 45, // Full access
      reliabilityScore: 97.5,
      price: 0, // Professional version might be internal
      currency: "€"
    },
    metrics: {
      activeOpenings: 0,
      openingsGrowth: "+0% YoY",
      avgCandidates: 0,
      candidatesGrowth: "+0% YoY",
      marketSweetSpot: 0,
      salaryRange: {
        min: 0,
        max: 0
      },
      timeToHire: 0,
      timeToHireChange: "+0% vs avg"
    },
    opportunityScore: {
      overall: 50,
      demandLevel: 50,
      talentAvailability: 50,
      salaryCompetitiveness: 50,
      marketTiming: 50
    },
    chartData: {
      demandTrend: [],
      salaryDistribution: [],
      competitors: []
    },
    executiveSummary: {
      paragraphs: [
        "Professional market analysis wordt momenteel samengesteld.",
        "Alle data wordt real-time verzameld van betrouwbare bronnen.",
        "Rapport bevat volledige toegang tot alle analyses en aanbevelingen."
      ]
    }
  };

  // Deep merge function
  function deepMerge<T>(target: T, source: Partial<T>): T {
    const result = { ...target };
    
    for (const key in source) {
      if (source[key] !== undefined) {
        if (typeof source[key] === 'object' && !Array.isArray(source[key]) && source[key] !== null) {
          result[key] = deepMerge(result[key] as any, source[key] as any);
        } else {
          result[key] = source[key] as any;
        }
      }
    }
    
    return result;
  }

  return deepMerge(baseData, overrides);
}