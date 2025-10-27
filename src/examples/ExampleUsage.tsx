import React from 'react';
import { 
  DemoReport, 
  ProfessionalReport, 
  generateReportData,
  createProfessionalReportData 
} from '../components';

// Example 1: Simple Demo Report
export function SimpleDemoExample() {
  return (
    <DemoReport 
      position="Senior Marketing Manager"
      sector="Tech & Digital"
      region="Nederland"
      onOrderClick={() => {
        console.log('Order clicked!');
        // Handle order logic here
      }}
    />
  );
}

// Example 2: Custom Demo Report with Generated Data
export function CustomDemoExample() {
  const customData = generateReportData({
    position: "Data Scientist",
    sector: "FinTech",
    region: "DACH Region",
    companyName: "TechCorp Intelligence"
  });

  return (
    <DemoReport 
      position={customData.config.title}
      sector={customData.config.sector}
      region={customData.config.region}
      customData={customData}
      onOrderClick={() => {
        window.open('/checkout', '_blank');
      }}
    />
  );
}

// Example 3: Professional Report
export function ProfessionalReportExample() {
  const reportData = createProfessionalReportData({
    config: {
      title: "Frontend Developer",
      subtitle: "Technology Sector • Nederland",
      sector: "Technology",
      region: "Nederland",
      reportId: "TECH-2025-001",
      companyName: "Internal Research",
      totalPages: 60,
      reliabilityScore: 98.5,
      date: new Date().toLocaleDateString('nl-NL'),
      previewPages: 3,
      price: 497,
      currency: "EUR"
    },
    metrics: {
      activeOpenings: 3200,
      openingsGrowth: "+45% YoY",
      avgCandidates: 28,
      candidatesGrowth: "-18% YoY",
      marketSweetSpot: 72,
      salaryRange: { min: 65, max: 82 },
      timeToHire: 18,
      timeToHireChange: "-35% vs avg"
    }
  });

  return (
    <ProfessionalReport 
      data={reportData}
      showPrintControls={true}
      onDownloadClick={() => {
        // Handle PDF generation and download
        console.log('Generating PDF...');
      }}
    />
  );
}

// Example 4: Website Integration Demo
export function WebsiteIntegrationExample() {
  const [selectedPosition, setSelectedPosition] = React.useState("Marketing Manager");
  const [selectedSector, setSelectedSector] = React.useState("Technology");
  
  const reportData = React.useMemo(() => {
    return generateReportData({
      position: selectedPosition,
      sector: selectedSector,
      region: "Nederland & DACH"
    });
  }, [selectedPosition, selectedSector]);

  return (
    <div className="space-y-6">
      {/* Configuration Controls */}
      <div className="bg-slate-50 p-6 rounded-lg print:hidden">
        <h3 className="text-lg font-medium mb-4">Configureer je rapport</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Positie</label>
            <select 
              value={selectedPosition} 
              onChange={(e) => setSelectedPosition(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded"
            >
              <option value="Marketing Manager">Marketing Manager</option>
              <option value="Senior Marketing Manager">Senior Marketing Manager</option>
              <option value="Data Scientist">Data Scientist</option>
              <option value="Frontend Developer">Frontend Developer</option>
              <option value="Product Manager">Product Manager</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Sector</label>
            <select 
              value={selectedSector} 
              onChange={(e) => setSelectedSector(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded"
            >
              <option value="Technology">Technology</option>
              <option value="FinTech">FinTech</option>
              <option value="E-commerce">E-commerce</option>
              <option value="Healthcare">Healthcare</option>
              <option value="Consulting">Consulting</option>
            </select>
          </div>
        </div>
      </div>

      {/* Generated Report */}
      <DemoReport 
        position={selectedPosition}
        sector={selectedSector}
        region="Nederland & DACH"
        customData={reportData}
        onOrderClick={() => {
          // Track analytics
          if (typeof window !== 'undefined' && (window as any).gtag) {
            (window as any).gtag('event', 'report_order_click', {
              position: selectedPosition,
              sector: selectedSector,
              price: reportData.config.price
            });
          }
          
          // Redirect to checkout
          window.location.href = `/checkout?product=market-intelligence&position=${encodeURIComponent(selectedPosition)}&sector=${encodeURIComponent(selectedSector)}`;
        }}
      />
    </div>
  );
}

// Example 5: Bulk Report Generation
export function BulkReportExample() {
  const positions = [
    "Marketing Manager",
    "Data Scientist", 
    "Frontend Developer",
    "Product Manager",
    "UX Designer"
  ];

  const sectors = ["Technology", "FinTech", "Healthcare"];
  
  const reports = React.useMemo(() => {
    return positions.map(position => 
      sectors.map(sector => 
        generateReportData({
          position,
          sector,
          region: "Nederland"
        })
      )
    ).flat();
  }, []);

  return (
    <div className="space-y-12">
      <div className="text-center py-8">
        <h2 className="text-2xl font-bold mb-4">
          {reports.length} Gegenereerde Market Intelligence Rapporten
        </h2>
        <p className="text-slate-600">
          Voorbeelden van automatisch gegenereerde rapporten voor verschillende posities en sectoren
        </p>
      </div>
      
      {reports.map((report, index) => (
        <div key={index} className="border-t-4 border-slate-900 pt-8">
          <ProfessionalReport 
            data={report}
            showPrintControls={false}
          />
        </div>
      ))}
    </div>
  );
}