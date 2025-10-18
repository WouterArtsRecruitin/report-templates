// Report Components
export { ReportTemplate } from './ReportTemplate';
export { DemoReport } from './DemoReport';
export { ProfessionalReport, createProfessionalReportData } from './ProfessionalReport';

// Chart Components
export { 
  DemandTrendChart,
  SalaryDistributionChart,
  GrowthTrendChart,
  SkillsDistributionChart,
  CompetitorChart,
  MultiMetricChart
} from './charts/ReportCharts';

// Types
export type { ReportData, ReportProps, ReportConfig, MarketMetrics, OpportunityScore, ChartData } from '../types/report';

// Utils
export { generateReportData } from '../utils/reportDataGenerator';
export type { ReportGeneratorConfig } from '../utils/reportDataGenerator';