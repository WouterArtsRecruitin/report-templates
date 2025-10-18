import { ReportData } from '../types/report';

// PDF Generation utility using browser's print functionality
// For production, you might want to use libraries like jsPDF or html2pdf
export class PDFGenerator {
  static async generateReport(reportData: ReportData): Promise<void> {
    try {
      // Create a new window with the report content
      const printWindow = window.open('', '_blank');
      if (!printWindow) {
        throw new Error('Pop-up blocker is enabled. Please allow pop-ups for this site.');
      }

      // Generate the HTML content for PDF
      const htmlContent = this.generatePDFHTML(reportData);
      
      printWindow.document.write(htmlContent);
      printWindow.document.close();
      
      // Trigger print dialog after a short delay to ensure content loads
      setTimeout(() => {
        printWindow.focus();
        printWindow.print();
        
        // Close the window after printing (user dependent)
        printWindow.addEventListener('afterprint', () => {
          printWindow.close();
        });
      }, 1000);
      
    } catch (error) {
      console.error('PDF generation failed:', error);
      
      // Fallback: open print dialog for current page
      this.fallbackPrint();
    }
  }

  static generatePDFHTML(reportData: ReportData): string {
    return `
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${reportData.config.title} - Market Intelligence Report</title>
    <style>
        /* Print-optimized styles */
        @media print {
            @page {
                size: A4;
                margin: 2cm 1.5cm;
            }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                line-height: 1.4;
                color: #1e293b;
                background: white;
            }
            .page-break { page-break-before: always; }
            .no-print { display: none; }
            .print-only { display: block; }
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }
        
        .header {
            background: linear-gradient(to right, #1e40af, #1e3a8a);
            color: white;
            padding: 30px;
            margin: -20px -20px 40px -20px;
            border-radius: 0;
        }
        
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo {
            width: 50px;
            height: 50px;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .company-info h1 {
            font-size: 24px;
            margin: 0;
            font-weight: 600;
        }
        
        .company-info .division {
            font-size: 14px;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        .report-id {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: right;
        }
        
        .report-id .label {
            font-size: 12px;
            opacity: 0.8;
        }
        
        .report-id .id {
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin-top: 5px;
        }
        
        .header-content {
            border-top: 1px solid rgba(255,255,255,0.2);
            padding-top: 20px;
        }
        
        .report-type {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
            margin-bottom: 15px;
        }
        
        .main-title {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 10px;
            line-height: 1.2;
        }
        
        .subtitle {
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 25px;
        }
        
        .meta-info {
            display: flex;
            gap: 30px;
            font-size: 14px;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section-title {
            font-size: 20px;
            color: #1e40af;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #1e40af;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            border-left: 4px solid #1e40af;
            padding: 20px;
            background: #f8fafc;
            border-radius: 0 8px 8px 0;
        }
        
        .metric-card.green { border-left-color: #059669; background: #f0fdf4; }
        .metric-card.blue { border-left-color: #2563eb; background: #eff6ff; }
        .metric-card.purple { border-left-color: #7c3aed; background: #faf5ff; }
        .metric-card.amber { border-left-color: #d97706; background: #fffbeb; }
        
        .metric-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        }
        
        .metric-change {
            font-size: 11px;
            color: #059669;
        }
        
        .summary-box {
            background: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 25px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 30px;
        }
        
        .summary-content p {
            margin-bottom: 15px;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .insights-box {
            background: #f0fdf4;
            border-left: 4px solid #059669;
            padding: 25px;
            border-radius: 0 8px 8px 0;
        }
        
        .insights-title {
            color: #065f46;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .insights-list {
            list-style: none;
            padding: 0;
        }
        
        .insights-list li {
            margin-bottom: 10px;
            padding-left: 20px;
            position: relative;
            font-size: 14px;
        }
        
        .insights-list li::before {
            content: "•";
            color: #059669;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .competitor-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .competitor-table thead {
            background: #1e40af;
            color: white;
        }
        
        .competitor-table th,
        .competitor-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .competitor-table th {
            font-weight: 600;
            font-size: 14px;
        }
        
        .competitor-table td {
            font-size: 13px;
        }
        
        .competitor-table tbody tr:nth-child(even) {
            background: #f8fafc;
        }
        
        .growth-positive {
            color: #059669;
            font-weight: 600;
        }
        
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            font-size: 11px;
            color: #64748b;
            display: flex;
            justify-content: space-between;
        }
        
        .opportunity-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 8px solid #e0e7ff;
            position: relative;
            margin: 0 auto 20px;
            background: conic-gradient(#1e40af 0deg ${360 * (reportData.opportunityScore.overall / 100)}deg, #e0e7ff ${360 * (reportData.opportunityScore.overall / 100)}deg 360deg);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .opportunity-inner {
            width: 90px;
            height: 90px;
            background: white;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .opportunity-score {
            font-size: 32px;
            font-weight: 700;
            color: #1e40af;
        }
        
        .opportunity-total {
            font-size: 12px;
            color: #64748b;
        }
    </style>
</head>
<body>
    <!-- Page 1: Executive Summary -->
    <div class="header">
        <div class="header-top">
            <div class="logo-section">
                <div class="logo">📊</div>
                <div class="company-info">
                    <h1>${reportData.config.companyName}</h1>
                    <div class="division">${reportData.config.division || 'Market Research Division'}</div>
                </div>
            </div>
            <div class="report-id">
                <div class="label">Report ID</div>
                <div class="id">${reportData.config.reportId}</div>
            </div>
        </div>
        
        <div class="header-content">
            <div class="report-type">Market Intelligence Report</div>
            <h2 class="main-title">${reportData.config.title}</h2>
            <div class="subtitle">${reportData.config.subtitle}</div>
            
            <div class="meta-info">
                <div class="meta-item">📅 ${reportData.config.date}</div>
                <div class="meta-item">🌍 ${reportData.config.region}</div>
                <div class="meta-item">🏆 ${reportData.config.reliabilityScore}% Betrouwbaarheid</div>
            </div>
        </div>
    </div>
    
    <!-- Executive Summary -->
    <div class="section">
        <h3 class="section-title">Executive Summary</h3>
        <div class="summary-box">
            ${reportData.executiveSummary.paragraphs.map(p => `<p>${p.replace(/<strong>/g, '<strong style="color: #1e40af;">').replace(/\+\d+%/g, '<strong style="color: #059669;">$&</strong>')}</p>`).join('')}
        </div>
    </div>
    
    <!-- Key Metrics -->
    <div class="section">
        <h3 class="section-title">Key Market Indicators</h3>
        <div class="metrics-grid">
            <div class="metric-card green">
                <div class="metric-label">Active Openings</div>
                <div class="metric-value">${reportData.metrics.activeOpenings.toLocaleString()}</div>
                <div class="metric-change">↗ ${reportData.metrics.openingsGrowth}</div>
            </div>
            <div class="metric-card blue">
                <div class="metric-label">Avg Candidates</div>
                <div class="metric-value">${reportData.metrics.avgCandidates}</div>
                <div class="metric-change">↘ ${reportData.metrics.candidatesGrowth}</div>
            </div>
            <div class="metric-card purple">
                <div class="metric-label">Market Sweet Spot</div>
                <div class="metric-value">€${reportData.metrics.marketSweetSpot}k</div>
                <div class="metric-change">€${reportData.metrics.salaryRange.min}-${reportData.metrics.salaryRange.max}k</div>
            </div>
            <div class="metric-card amber">
                <div class="metric-label">Time to Hire</div>
                <div class="metric-value">${reportData.metrics.timeToHire}d</div>
                <div class="metric-change">↘ ${reportData.metrics.timeToHireChange}</div>
            </div>
        </div>
    </div>
    
    <!-- Opportunity Score -->
    <div class="section">
        <h3 class="section-title">Market Opportunity Analysis</h3>
        <div style="text-align: center; margin-bottom: 30px;">
            <div class="opportunity-circle">
                <div class="opportunity-inner">
                    <div class="opportunity-score">${reportData.opportunityScore.overall}</div>
                    <div class="opportunity-total">/100</div>
                </div>
            </div>
            <div style="font-weight: 600; margin-bottom: 10px;">Overall Opportunity Score</div>
            <div style="background: #dcfce7; color: #065f46; padding: 5px 15px; border-radius: 15px; display: inline-block; font-size: 12px;">
                ${reportData.opportunityScore.overall >= 80 ? 'Zeer gunstig momentum' : 
                  reportData.opportunityScore.overall >= 60 ? 'Gunstig momentum' : 
                  'Neutraal momentum'}
            </div>
        </div>
    </div>
    
    <!-- Key Insights -->
    <div class="section">
        <div class="insights-box">
            <div class="insights-title">Belangrijkste Inzichten</div>
            <ul class="insights-list">
                <li>Post vacatures <strong>binnen 72 uur</strong> om optimaal momentum te benutten</li>
                <li>Target <strong>€${reportData.metrics.marketSweetSpot-3}-${reportData.metrics.marketSweetSpot+1}k range</strong> voor optimale response</li>
                <li>Focus op <strong>hybrid werk</strong> (89% candidate preference in sector)</li>
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <div>${reportData.config.companyName} © 2025</div>
        <div>Pagina 1 van ${reportData.config.totalPages} • Volledige Versie</div>
    </div>
    
    <!-- Page 2: Competitor Analysis -->
    <div class="page-break">
        <div class="section">
            <h3 class="section-title">Concurrent Analyse - Top ${reportData.chartData.competitors.length} Spelers</h3>
            <table class="competitor-table">
                <thead>
                    <tr>
                        <th>Bedrijf</th>
                        <th style="text-align: right;">Openings</th>
                        <th style="text-align: right;">Avg Salaris</th>
                        <th style="text-align: right;">Groei YoY</th>
                    </tr>
                </thead>
                <tbody>
                    ${reportData.chartData.competitors.map(company => `
                        <tr>
                            <td>${company.company}</td>
                            <td style="text-align: right; color: #2563eb;">${company.openings}</td>
                            <td style="text-align: right; color: #7c3aed;">€${company.avgSalary}k</td>
                            <td style="text-align: right;" class="growth-positive">${company.growth}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h3 class="section-title">Salary Benchmark Details</h3>
            <div class="metrics-grid" style="grid-template-columns: repeat(3, 1fr);">
                <div class="metric-card blue">
                    <div class="metric-label">P25 (Entry-Mid)</div>
                    <div class="metric-value">€${reportData.metrics.salaryRange.min}k</div>
                </div>
                <div class="metric-card purple">
                    <div class="metric-label">P50 (Median) ★</div>
                    <div class="metric-value">€${reportData.metrics.marketSweetSpot}k</div>
                </div>
                <div class="metric-card green">
                    <div class="metric-label">P75 (Senior)</div>
                    <div class="metric-value">€${reportData.metrics.salaryRange.max}k</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div>${reportData.config.companyName} © 2025</div>
            <div>Pagina 2 van ${reportData.config.totalPages} • Confidential</div>
        </div>
    </div>
    
    <script>
        // Auto-print when loaded
        window.addEventListener('load', function() {
            setTimeout(function() {
                window.print();
            }, 500);
        });
    </script>
</body>
</html>
    `;
  }

  static fallbackPrint(): void {
    // Simple fallback - just trigger print for current page
    window.print();
  }

  static async downloadReport(reportData: ReportData): Promise<void> {
    try {
      // For demo purposes, create a simple text-based report
      const reportContent = this.generateTextReport(reportData);
      const blob = new Blob([reportContent], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `${reportData.config.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_market_intelligence_report.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Report download failed:', error);
      alert('Download mislukt. Probeer het opnieuw.');
    }
  }

  static generateTextReport(reportData: ReportData): string {
    return `
MARKET INTELLIGENCE REPORT
=${reportData.config.title}=
${reportData.config.subtitle}

Report ID: ${reportData.config.reportId}
Date: ${reportData.config.date}
Reliability: ${reportData.config.reliabilityScore}%

EXECUTIVE SUMMARY
${reportData.executiveSummary.paragraphs.join('\n\n')}

KEY METRICS
- Active Openings: ${reportData.metrics.activeOpenings} (${reportData.metrics.openingsGrowth})
- Average Candidates: ${reportData.metrics.avgCandidates} (${reportData.metrics.candidatesGrowth})
- Market Sweet Spot: €${reportData.metrics.marketSweetSpot}k
- Salary Range: €${reportData.metrics.salaryRange.min}k - €${reportData.metrics.salaryRange.max}k
- Time to Hire: ${reportData.metrics.timeToHire} days (${reportData.metrics.timeToHireChange})

OPPORTUNITY SCORES
- Overall: ${reportData.opportunityScore.overall}/100
- Demand Level: ${reportData.opportunityScore.demandLevel}/100
- Talent Availability: ${reportData.opportunityScore.talentAvailability}/100
- Salary Competitiveness: ${reportData.opportunityScore.salaryCompetitiveness}/100
- Market Timing: ${reportData.opportunityScore.marketTiming}/100

TOP COMPETITORS
${reportData.chartData.competitors.map((c, i) => 
  `${i+1}. ${c.company} - ${c.openings} openings, €${c.avgSalary}k avg salary, ${c.growth} growth`
).join('\n')}

DEMAND TREND (6 months)
${reportData.chartData.demandTrend.map(d => `${d.month}: ${d.openings} openings`).join('\n')}

KEY INSIGHTS
• Post vacatures binnen 72 uur om optimaal momentum te benutten
• Target €${reportData.metrics.marketSweetSpot-3}-${reportData.metrics.marketSweetSpot+1}k range voor optimale response  
• Focus op hybrid werk (89% candidate preference in sector)

---
Generated by ${reportData.config.companyName}
© 2025 - Confidential Market Intelligence Report
Total Pages: ${reportData.config.totalPages}
    `.trim();
  }
}