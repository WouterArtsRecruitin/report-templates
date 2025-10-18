import { generateReportData } from '../utils/reportDataGenerator';
import { PDFGenerator } from '../utils/pdfGenerator';

describe('Report Generator', () => {
  test('generates valid report data for Marketing Manager', () => {
    const reportData = generateReportData({
      position: 'Marketing Manager',
      sector: 'Technology',
      region: 'Nederland'
    });

    expect(reportData.config.title).toBe('Marketing Manager');
    expect(reportData.config.sector).toBe('Technology');
    expect(reportData.metrics.activeOpenings).toBeGreaterThan(0);
    expect(reportData.opportunityScore.overall).toBeGreaterThanOrEqual(0);
    expect(reportData.opportunityScore.overall).toBeLessThanOrEqual(100);
    expect(reportData.chartData.demandTrend).toHaveLength(6);
    expect(reportData.chartData.competitors.length).toBeGreaterThan(0);
  });

  test('generates different data for different positions', () => {
    const marketingData = generateReportData({
      position: 'Marketing Manager',
      sector: 'Technology',
      region: 'Nederland'
    });

    const techData = generateReportData({
      position: 'Frontend Developer',
      sector: 'Technology', 
      region: 'Nederland'
    });

    expect(marketingData.config.title).not.toBe(techData.config.title);
    expect(marketingData.config.reportId).not.toBe(techData.config.reportId);
  });

  test('applies sector multipliers correctly', () => {
    const techData = generateReportData({
      position: 'Developer',
      sector: 'Technology',
      region: 'Nederland'
    });

    const educationData = generateReportData({
      position: 'Developer', 
      sector: 'Education',
      region: 'Nederland'
    });

    // Tech should generally have higher salaries than education
    expect(techData.metrics.marketSweetSpot).toBeGreaterThan(educationData.metrics.marketSweetSpot);
  });

  test('generates valid PDF HTML', () => {
    const reportData = generateReportData({
      position: 'Test Manager',
      sector: 'Technology',
      region: 'Nederland'
    });

    const pdfHtml = PDFGenerator.generatePDFHTML(reportData);
    
    expect(pdfHtml).toContain('<!DOCTYPE html>');
    expect(pdfHtml).toContain(reportData.config.title);
    expect(pdfHtml).toContain(reportData.config.companyName);
    expect(pdfHtml).toContain('Market Intelligence Report');
    expect(pdfHtml).toContain('@media print');
  });

  test('generates valid text report', () => {
    const reportData = generateReportData({
      position: 'Test Manager',
      sector: 'FinTech',
      region: 'DACH'
    });

    const textReport = PDFGenerator.generateTextReport(reportData);

    expect(textReport).toContain('MARKET INTELLIGENCE REPORT');
    expect(textReport).toContain(reportData.config.title);
    expect(textReport).toContain('EXECUTIVE SUMMARY');
    expect(textReport).toContain('KEY METRICS');
    expect(textReport).toContain('OPPORTUNITY SCORES');
    expect(textReport).toContain('TOP COMPETITORS');
  });

  test('validates executive summary content', () => {
    const reportData = generateReportData({
      position: 'Senior Developer',
      sector: 'FinTech',
      region: 'Nederland'
    });

    expect(reportData.executiveSummary.paragraphs).toBeInstanceOf(Array);
    expect(reportData.executiveSummary.paragraphs.length).toBeGreaterThan(0);
    
    reportData.executiveSummary.paragraphs.forEach(paragraph => {
      expect(typeof paragraph).toBe('string');
      expect(paragraph.length).toBeGreaterThan(0);
    });
  });

  test('validates opportunity scores are within range', () => {
    const reportData = generateReportData({
      position: 'Product Manager',
      sector: 'Technology',
      region: 'Nederland'
    });

    const { opportunityScore } = reportData;
    
    expect(opportunityScore.overall).toBeGreaterThanOrEqual(0);
    expect(opportunityScore.overall).toBeLessThanOrEqual(100);
    expect(opportunityScore.demandLevel).toBeGreaterThanOrEqual(0);
    expect(opportunityScore.demandLevel).toBeLessThanOrEqual(100);
    expect(opportunityScore.talentAvailability).toBeGreaterThanOrEqual(0);
    expect(opportunityScore.talentAvailability).toBeLessThanOrEqual(100);
    expect(opportunityScore.salaryCompetitiveness).toBeGreaterThanOrEqual(0);
    expect(opportunityScore.salaryCompetitiveness).toBeLessThanOrEqual(100);
    expect(opportunityScore.marketTiming).toBeGreaterThanOrEqual(0);
    expect(opportunityScore.marketTiming).toBeLessThanOrEqual(100);
  });

  test('validates chart data structure', () => {
    const reportData = generateReportData({
      position: 'UX Designer',
      sector: 'Technology',
      region: 'Nederland'
    });

    const { chartData } = reportData;

    // Demand trend validation
    expect(chartData.demandTrend).toHaveLength(6);
    chartData.demandTrend.forEach(item => {
      expect(item).toHaveProperty('month');
      expect(item).toHaveProperty('openings');
      expect(typeof item.month).toBe('string');
      expect(typeof item.openings).toBe('number');
      expect(item.openings).toBeGreaterThan(0);
    });

    // Salary distribution validation
    expect(chartData.salaryDistribution.length).toBeGreaterThan(0);
    chartData.salaryDistribution.forEach(item => {
      expect(item).toHaveProperty('range');
      expect(item).toHaveProperty('count');
      expect(typeof item.range).toBe('string');
      expect(typeof item.count).toBe('number');
      expect(item.count).toBeGreaterThan(0);
    });

    // Competitors validation
    expect(chartData.competitors.length).toBeGreaterThan(0);
    chartData.competitors.forEach(competitor => {
      expect(competitor).toHaveProperty('company');
      expect(competitor).toHaveProperty('openings');
      expect(competitor).toHaveProperty('avgSalary');
      expect(competitor).toHaveProperty('growth');
      expect(typeof competitor.company).toBe('string');
      expect(typeof competitor.openings).toBe('number');
      expect(typeof competitor.avgSalary).toBe('number');
      expect(typeof competitor.growth).toBe('string');
    });
  });
});