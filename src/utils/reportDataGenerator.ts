import { ReportData } from '../types/report';

export interface ReportGeneratorConfig {
  position: string;
  sector: string;
  region: string;
  companyName?: string;
  customMetrics?: Partial<ReportData['metrics']>;
}

export function generateReportData({
  position,
  sector,
  region,
  companyName = "Recruitin Intelligence",
  customMetrics = {}
}: ReportGeneratorConfig): ReportData {
  
  // Generate realistic metrics based on position and sector
  const baseMetrics = generateMarketMetrics(position, sector);
  const metrics = { ...baseMetrics, ...customMetrics };
  
  // Generate opportunity scores based on metrics
  const opportunityScore = calculateOpportunityScores(metrics);
  
  // Generate chart data
  const chartData = generateChartData(metrics, position, sector);
  
  // Generate executive summary
  const executiveSummary = generateExecutiveSummary(position, sector, region, metrics);
  
  return {
    config: {
      title: position,
      subtitle: `${sector} • ${region}`,
      sector,
      region,
      reportId: generateReportId(position),
      date: new Date().toLocaleDateString('nl-NL', { 
        year: 'numeric', 
        month: 'long' 
      }),
      companyName,
      division: "Market Research Division",
      totalPages: Math.floor(Math.random() * 15) + 30, // 30-45 pages
      previewPages: 2,
      reliabilityScore: Math.floor(Math.random() * 8) + 92, // 92-99%
      price: calculatePrice(position, sector),
      currency: "€"
    },
    metrics,
    opportunityScore,
    chartData,
    executiveSummary
  };
}

function generateMarketMetrics(position: string, sector: string) {
  // Base metrics vary by seniority and sector
  const seniority = getSeniorityLevel(position);
  const sectorMultiplier = getSectorMultiplier(sector);
  
  const baseOpenings = Math.floor((500 + Math.random() * 2000) * sectorMultiplier);
  const baseGrowth = Math.floor(Math.random() * 40) + 10; // 10-50%
  const baseCandidates = Math.floor(20 + Math.random() * 40 + seniority * 10);
  const candidateGrowthDirection = Math.random() > 0.6 ? 1 : -1;
  const candidateGrowth = Math.floor(Math.random() * 20) + 5;
  
  const baseSalary = calculateBaseSalary(position, sector, seniority);
  const timeToHire = Math.floor(15 + Math.random() * 20 + seniority * 5);
  
  return {
    activeOpenings: baseOpenings,
    openingsGrowth: `+${baseGrowth}% YoY`,
    avgCandidates: baseCandidates,
    candidatesGrowth: `${candidateGrowthDirection > 0 ? '+' : ''}${candidateGrowthDirection * candidateGrowth}% YoY`,
    marketSweetSpot: baseSalary,
    salaryRange: {
      min: Math.floor(baseSalary * 0.85),
      max: Math.floor(baseSalary * 1.15)
    },
    timeToHire,
    timeToHireChange: `-${Math.floor(Math.random() * 30) + 10}% vs avg`
  };
}

function getSeniorityLevel(position: string): number {
  const positionLower = position.toLowerCase();
  if (positionLower.includes('junior') || positionLower.includes('entry')) return 0;
  if (positionLower.includes('senior') || positionLower.includes('lead')) return 2;
  if (positionLower.includes('principal') || positionLower.includes('head')) return 3;
  if (positionLower.includes('director') || positionLower.includes('vp')) return 4;
  return 1; // Mid-level
}

function getSectorMultiplier(sector: string): number {
  const sectorLower = sector.toLowerCase();
  if (sectorLower.includes('tech') || sectorLower.includes('software')) return 1.3;
  if (sectorLower.includes('finance') || sectorLower.includes('fintech')) return 1.1;
  if (sectorLower.includes('healthcare') || sectorLower.includes('pharma')) return 0.9;
  if (sectorLower.includes('education')) return 0.7;
  return 1.0;
}

function calculateBaseSalary(position: string, sector: string, seniority: number): number {
  let baseSalary = 45 + seniority * 15; // Base salary progression
  
  // Sector adjustments
  const sectorMultiplier = getSectorMultiplier(sector);
  baseSalary = Math.floor(baseSalary * sectorMultiplier);
  
  // Role-specific adjustments
  const positionLower = position.toLowerCase();
  if (positionLower.includes('engineer') || positionLower.includes('developer')) {
    baseSalary += 10;
  } else if (positionLower.includes('manager')) {
    baseSalary += 8;
  } else if (positionLower.includes('analyst')) {
    baseSalary += 5;
  } else if (positionLower.includes('designer')) {
    baseSalary += 3;
  }
  
  return Math.floor(baseSalary);
}

function calculateOpportunityScores(metrics: any) {
  const demandLevel = Math.min(100, Math.floor((metrics.activeOpenings / 30) + Math.random() * 20 + 70));
  const talentAvailability = Math.max(20, Math.min(100, 120 - metrics.avgCandidates + Math.random() * 20));
  const salaryCompetitiveness = Math.floor(Math.random() * 20) + 80;
  const marketTiming = Math.floor(Math.random() * 15) + 85;
  const overall = Math.floor((demandLevel + talentAvailability + salaryCompetitiveness + marketTiming) / 4);
  
  return {
    overall,
    demandLevel,
    talentAvailability,
    salaryCompetitiveness,
    marketTiming
  };
}

function generateChartData(metrics: any, position: string, sector: string) {
  // Generate 6 months of demand trend data
  const demandTrend = [];
  const months = ['Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep'];
  let currentOpenings = Math.floor(metrics.activeOpenings * 0.7);
  
  for (const month of months) {
    demandTrend.push({ month, openings: currentOpenings });
    currentOpenings = Math.floor(currentOpenings * (1 + Math.random() * 0.15 + 0.05));
  }
  
  // Generate salary distribution
  const baseSalary = metrics.marketSweetSpot;
  const salaryRanges = [
    `${baseSalary-20}-${baseSalary-15}k`,
    `${baseSalary-15}-${baseSalary-10}k`,
    `${baseSalary-10}-${baseSalary-5}k`,
    `${baseSalary-5}-${baseSalary}k`,
    `${baseSalary}-${baseSalary+5}k`,
    `${baseSalary+5}-${baseSalary+10}k`,
    `${baseSalary+10}-${baseSalary+15}k`,
    `${baseSalary+15}k+`,
  ];
  
  const salaryDistribution = salaryRanges.map((range, index) => {
    // Normal distribution around the middle
    const distance = Math.abs(index - 3.5);
    const count = Math.floor(Math.exp(-distance) * 800 + Math.random() * 200 + 100);
    return { range, count };
  });
  
  // Generate competitors
  const competitors = generateCompetitors(sector, metrics.marketSweetSpot);
  
  return {
    demandTrend,
    salaryDistribution,
    competitors
  };
}

function generateCompetitors(sector: string, avgSalary: number) {
  const techCompanies = ['Booking.com', 'Adyen', 'Coolblue', 'Bol.com', 'ING', 'Philips', 'ASML', 'TomTom'];
  const financeCompanies = ['ING', 'ABN AMRO', 'Rabobank', 'Aegon', 'NN Group', 'Adyen', 'Mollie'];
  const consultingCompanies = ['McKinsey', 'BCG', 'Deloitte', 'PwC', 'KPMG', 'EY', 'Accenture'];
  
  let companyPool = techCompanies;
  if (sector.toLowerCase().includes('finance')) companyPool = financeCompanies;
  if (sector.toLowerCase().includes('consulting')) companyPool = consultingCompanies;
  
  return companyPool.slice(0, 5).map(company => ({
    company,
    openings: Math.floor(Math.random() * 40) + 15,
    avgSalary: Math.floor(avgSalary * (0.9 + Math.random() * 0.2)),
    growth: `+${Math.floor(Math.random() * 15) + 3}%`
  }));
}

function generateExecutiveSummary(position: string, sector: string, region: string, metrics: any) {
  const paragraphs = [
    `De arbeidsmarkt voor <strong>${position}</strong> in de ${sector} vertoont een 
    ${metrics.openingsGrowth.includes('+') ? 'sterke stijgende' : 'stabiele'} trend met 
    <strong>${metrics.activeOpenings.toLocaleString()} actieve vacatures</strong>. 
    Dit wijst op een ${metrics.activeOpenings > 2000 ? 'significante' : 'gezonde'} vraag naar 
    talent in de ${region}.`,
    
    `De <strong>gemiddelde kandidatenpool van ${metrics.avgCandidates} sollicitanten</strong> per vacature 
    ${metrics.candidatesGrowth.includes('-') ? 'is gedaald' : 'is gestegen'}, wat duidt op een 
    ${metrics.avgCandidates < 30 ? 'krappe' : 'competitieve'} arbeidsmarkt. Dit creëert 
    ${metrics.avgCandidates < 30 ? 'gunstige condities voor professionals' : 'meer competitie tussen kandidaten'}.`,
    
    `Het <strong>market sweet spot salaris van €${metrics.marketSweetSpot.toLocaleString()}</strong> ligt binnen een 
    competitieve range van €${metrics.salaryRange.min}k-€${metrics.salaryRange.max}k. 
    Werkgevers die binnen de optimale range bieden, zien gemiddeld meer gekwalificeerde sollicitaties.`
  ];
  
  return { paragraphs };
}

function generateReportId(position: string): string {
  const prefix = position.substring(0, 3).toUpperCase();
  const year = new Date().getFullYear();
  const month = String(new Date().getMonth() + 1).padStart(2, '0');
  const random = Math.floor(Math.random() * 100);
  return `${prefix}-${year}-${month}-${random}`;
}

function calculatePrice(position: string, sector: string): number {
  const basePrices = [49, 59, 69, 79, 89, 99];
  const seniority = getSeniorityLevel(position);
  const sectorMultiplier = getSectorMultiplier(sector);
  
  const basePrice = basePrices[Math.min(seniority + 1, basePrices.length - 1)];
  return Math.floor(basePrice * sectorMultiplier);
}