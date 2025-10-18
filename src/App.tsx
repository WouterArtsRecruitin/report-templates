import React, { useState } from 'react';
import { DemoReport } from './components/DemoReport';
import { CheckoutModal } from './components/CheckoutModal';
import { generateReportData } from './utils/reportDataGenerator';
import { PDFGenerator } from './utils/pdfGenerator';
import { ReportData } from './types/report';

export default function App() {
  const [version, setVersion] = useState<'a' | 'b' | 'c'>('a');
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState<ReportData | null>(null);

  // Generate different data sets for A/B/C testing
  const reportDataA = generateReportData({
    position: "Marketing Manager",
    sector: "Technology",
    region: "Nederland",
    companyName: "Classic Intelligence"
  });

  const reportDataB = generateReportData({
    position: "Senior Data Scientist", 
    sector: "FinTech",
    region: "Nederland & DACH",
    companyName: "Interactive Analytics"
  });

  const reportDataC = generateReportData({
    position: "Frontend Developer",
    sector: "E-commerce", 
    region: "Nederland",
    companyName: "Professional Reports"
  });

  const handleOrderClick = (reportData: ReportData) => {
    setSelectedReport(reportData);
    setIsCheckoutOpen(true);
  };

  const handlePaymentSuccess = async (reportData: ReportData) => {
    // Generate and download both PDF and text versions
    try {
      await PDFGenerator.generateReport(reportData);
      await PDFGenerator.downloadReport(reportData);
      
      // Show success message
      alert(`Succes! Je ${reportData.config.title} rapport is gedownload in PDF én tekst formaat.`);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Er is een probleem opgetreden bij het downloaden. Neem contact op met support.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Version Switcher */}
      <div className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm print:hidden">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="text-sm text-slate-600">A/B/C Test Varianten</div>
            <div className="flex gap-2">
              <button
                onClick={() => setVersion('a')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'a'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie A - Marketing Manager
              </button>
              <button
                onClick={() => setVersion('b')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'b'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie B - Data Scientist  
              </button>
              <button
                onClick={() => setVersion('c')}
                className={`px-6 py-2 text-sm rounded-sm transition-colors ${
                  version === 'c'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                Versie C - Frontend Developer
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      {version === 'a' && (
        <DemoReport 
          position={reportDataA.config.title}
          sector={reportDataA.config.sector}
          region={reportDataA.config.region}
          customData={reportDataA}
          onOrderClick={() => {
            console.log('Version A order clicked');
            // Track analytics for version A
            if (typeof window !== 'undefined' && (window as any).gtag) {
              (window as any).gtag('event', 'report_order_a', {
                position: reportDataA.config.title,
                price: reportDataA.config.price
              });
            }
            handleOrderClick(reportDataA);
          }}
        />
      )}
      
      {version === 'b' && (
        <DemoReport 
          position={reportDataB.config.title}
          sector={reportDataB.config.sector}
          region={reportDataB.config.region}
          customData={reportDataB}
          onOrderClick={() => {
            console.log('Version B order clicked');
            // Track analytics for version B
            if (typeof window !== 'undefined' && (window as any).gtag) {
              (window as any).gtag('event', 'report_order_b', {
                position: reportDataB.config.title,
                price: reportDataB.config.price
              });
            }
            handleOrderClick(reportDataB);
          }}
        />
      )}
      
      {version === 'c' && (
        <DemoReport 
          position={reportDataC.config.title}
          sector={reportDataC.config.sector}
          region={reportDataC.config.region}
          customData={reportDataC}
          onOrderClick={() => {
            console.log('Version C order clicked');
            // Track analytics for version C
            if (typeof window !== 'undefined' && (window as any).gtag) {
              (window as any).gtag('event', 'report_order_c', {
                position: reportDataC.config.title,
                price: reportDataC.config.price
              });
            }
            handleOrderClick(reportDataC);
          }}
        />
      )}

      {/* Checkout Modal */}
      {selectedReport && (
        <CheckoutModal
          isOpen={isCheckoutOpen}
          onClose={() => {
            setIsCheckoutOpen(false);
            setSelectedReport(null);
          }}
          reportData={selectedReport}
          onPaymentSuccess={handlePaymentSuccess}
        />
      )}
    </div>
  );
}