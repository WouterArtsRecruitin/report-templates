export interface ReportConfig {
  // Basic Info
  title: string;
  subtitle: string;
  sector: string;
  region: string;
  reportId: string;
  date: string;
  
  // Company/Brand Info
  companyName: string;
  companyLogo?: string;
  division?: string;
  
  // Report Metadata
  totalPages: number;
  previewPages: number;
  reliabilityScore: number;
  
  // Pricing
  price: number;
  currency: string;
}

export interface MarketMetrics {
  activeOpenings: number;
  openingsGrowth: string;
  avgCandidates: number;
  candidatesGrowth: string;
  marketSweetSpot: number;
  salaryRange: {
    min: number;
    max: number;
  };
  timeToHire: number;
  timeToHireChange: string;
}

export interface OpportunityScore {
  overall: number;
  demandLevel: number;
  talentAvailability: number;
  salaryCompetitiveness: number;
  marketTiming: number;
}

export interface ChartData {
  demandTrend: Array<{
    month: string;
    openings: number;
  }>;
  salaryDistribution: Array<{
    range: string;
    count: number;
  }>;
  competitors: Array<{
    company: string;
    openings: number;
    avgSalary: number;
    growth: string;
  }>;
}

export interface ExecutiveSummary {
  paragraphs: string[];
}

export interface ReportData {
  config: ReportConfig;
  metrics: MarketMetrics;
  opportunityScore: OpportunityScore;
  chartData: ChartData;
  executiveSummary: ExecutiveSummary;
}

export interface ReportProps {
  data: ReportData;
  variant: 'demo' | 'professional';
  onOrderClick?: () => void;
  showPrintControls?: boolean;
}