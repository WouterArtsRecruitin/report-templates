import React from 'react';
import { ReportTemplate } from './ReportTemplate';
import { ReportData } from '../types/report';

interface DemoReportProps {
  position?: string;
  sector?: string;
  region?: string;
  onOrderClick?: () => void;
  customData?: Partial<ReportData>;
}

export function DemoReport({ 
  position = "Senior Marketing Manager",
  sector = "Tech & Digital Sector",
  region = "Nederland & DACH Region",
  onOrderClick,
  customData 
}: DemoReportProps) {
  const defaultData: ReportData = {
    config: {
      title: position,
      subtitle: `${sector} • ${region}`,
      sector,
      region,
      reportId: "MKT-2025-10-NL",
      date: "Oktober 2025",
      companyName: "Recruitin Intelligence",
      division: "Market Research Division",
      totalPages: 32,
      previewPages: 2,
      reliabilityScore: 96.2,
      price: 59,
      currency: "€"
    },
    metrics: {
      activeOpenings: 2847,
      openingsGrowth: "+34% YoY",
      avgCandidates: 38,
      candidatesGrowth: "-12% YoY",
      marketSweetSpot: 67,
      salaryRange: {
        min: 58,
        max: 76
      },
      timeToHire: 22,
      timeToHireChange: "-29% vs avg"
    },
    opportunityScore: {
      overall: 89,
      demandLevel: 94,
      talentAvailability: 78,
      salaryCompetitiveness: 92,
      marketTiming: 96
    },
    chartData: {
      demandTrend: [
        { month: 'Apr', openings: 1820 },
        { month: 'Mei', openings: 2150 },
        { month: 'Jun', openings: 2380 },
        { month: 'Jul', openings: 2590 },
        { month: 'Aug', openings: 2680 },
        { month: 'Sep', openings: 2847 },
      ],
      salaryDistribution: [
        { range: '45-50k', count: 180 },
        { range: '50-55k', count: 420 },
        { range: '55-60k', count: 680 },
        { range: '60-65k', count: 890 },
        { range: '65-70k', count: 950 },
        { range: '70-75k', count: 720 },
        { range: '75-80k', count: 450 },
        { range: '80k+', count: 280 },
      ],
      competitors: [
        { company: 'Booking.com', openings: 47, avgSalary: 72, growth: '+12%' },
        { company: 'Adyen', openings: 34, avgSalary: 76, growth: '+8%' },
        { company: 'Coolblue', openings: 28, avgSalary: 65, growth: '+15%' },
        { company: 'Bol.com', openings: 31, avgSalary: 68, growth: '+6%' },
        { company: 'ING', openings: 25, avgSalary: 71, growth: '+4%' },
      ]
    },
    executiveSummary: {
      paragraphs: [
        `De arbeidsmarkt voor <strong>${position}</strong> in de ${sector} vertoont een 
        sterke stijgende trend met <strong>${2847} actieve vacatures</strong> per September 2025, een 
        toename van <strong>34% jaar-op-jaar</strong>. Dit wijst op een significante vraag naar 
        marketing talent in de Nederlandse en DACH regio.`,
        `De <strong>gemiddelde kandidatenpool van 38 sollicitanten</strong> per vacature is met 12% 
        gedaald, wat duidt op een krappe arbeidsmarkt. Dit creëert gunstige condities voor 
        getalenteerde professionals, maar verhoogt de competitie tussen werkgevers.`,
        `Het <strong>market sweet spot salaris van €67,000</strong> ligt binnen een competitieve 
        range van €58k-€76k. Werkgevers die binnen de €64k-€68k range bieden, zien gemiddeld 
        23% meer gekwalificeerde sollicitaties.`
      ]
    }
  };

  // Merge custom data with defaults
  const reportData = customData ? {
    ...defaultData,
    ...customData,
    config: { ...defaultData.config, ...customData.config },
    metrics: { ...defaultData.metrics, ...customData.metrics },
    opportunityScore: { ...defaultData.opportunityScore, ...customData.opportunityScore },
    chartData: { ...defaultData.chartData, ...customData.chartData },
    executiveSummary: { ...defaultData.executiveSummary, ...customData.executiveSummary }
  } : defaultData;

  return (
    <ReportTemplate 
      data={reportData}
      variant="demo"
      onOrderClick={onOrderClick}
      showPrintControls={true}
    />
  );
}