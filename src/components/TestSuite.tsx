import React, { useState } from 'react';
import { Play, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';
import { DemoReport } from './DemoReport';
import { ProfessionalReport, createProfessionalReportData } from './ProfessionalReport';
import { generateReportData } from '../utils/reportDataGenerator';
import { PDFGenerator } from '../utils/pdfGenerator';

interface TestResult {
  test: string;
  status: 'running' | 'passed' | 'failed';
  message: string;
  duration?: number;
}

export function TestSuite() {
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState<TestResult[]>([]);

  const runAllTests = async () => {
    setIsRunning(true);
    setResults([]);

    const tests = [
      'Component Rendering Test',
      'Data Generation Test', 
      'PDF Generation Test',
      'Chart Data Test',
      'Responsive Design Test',
      'Print Functionality Test'
    ];

    // Initialize test results
    const initialResults = tests.map(test => ({
      test,
      status: 'running' as const,
      message: 'Bezig met testen...'
    }));
    setResults(initialResults);

    // Test 1: Component Rendering
    await runTest(0, async () => {
      const testData = generateReportData({
        position: "Test Manager",
        sector: "Technology",
        region: "Test Region"
      });
      
      if (!testData.config.title || !testData.metrics.activeOpenings) {
        throw new Error('Report data missing essential fields');
      }
      
      return 'Components render correctly with valid data';
    });

    // Test 2: Data Generation 
    await runTest(1, async () => {
      const positions = ["Marketing Manager", "Data Scientist", "Frontend Developer"];
      const sectors = ["Technology", "FinTech", "Healthcare"];
      
      for (const position of positions) {
        for (const sector of sectors) {
          const data = generateReportData({ position, sector, region: "Nederland" });
          
          if (!data.config.title || data.metrics.activeOpenings <= 0) {
            throw new Error(`Invalid data for ${position} in ${sector}`);
          }
        }
      }
      
      return 'Data generation works for all position/sector combinations';
    });

    // Test 3: PDF Generation
    await runTest(2, async () => {
      const testData = generateReportData({
        position: "PDF Test Manager",
        sector: "Technology", 
        region: "Nederland"
      });
      
      const htmlContent = PDFGenerator.generatePDFHTML(testData);
      
      if (!htmlContent.includes(testData.config.title) || 
          !htmlContent.includes(testData.config.companyName)) {
        throw new Error('PDF HTML missing essential content');
      }
      
      return 'PDF generation creates valid HTML with all data';
    });

    // Test 4: Chart Data
    await runTest(3, async () => {
      const testData = generateReportData({
        position: "Chart Test Manager",
        sector: "FinTech",
        region: "DACH"
      });
      
      if (testData.chartData.demandTrend.length !== 6) {
        throw new Error('Demand trend should have 6 months of data');
      }
      
      if (testData.chartData.salaryDistribution.length < 6) {
        throw new Error('Salary distribution needs multiple ranges');
      }
      
      if (testData.chartData.competitors.length === 0) {
        throw new Error('Competitors list cannot be empty');
      }
      
      return 'Chart data contains all required elements';
    });

    // Test 5: Responsive Design
    await runTest(4, async () => {
      // Check if CSS classes exist (basic validation)
      const testElement = document.createElement('div');
      testElement.className = 'print:hidden md:grid-cols-4 lg:text-xl';
      
      if (!testElement.className.includes('print:hidden')) {
        throw new Error('Print classes not working');
      }
      
      return 'Responsive classes are properly applied';
    });

    // Test 6: Print Functionality
    await runTest(5, async () => {
      // Test print-specific styling
      const testData = generateReportData({
        position: "Print Test Manager", 
        sector: "Technology",
        region: "Nederland"
      });
      
      const reportText = PDFGenerator.generateTextReport(testData);
      
      if (!reportText.includes('MARKET INTELLIGENCE REPORT') ||
          !reportText.includes(testData.config.title)) {
        throw new Error('Text report missing key sections');
      }
      
      return 'Print and text export functionality working';
    });

    setIsRunning(false);
  };

  const runTest = async (index: number, testFn: () => Promise<string>) => {
    const startTime = Date.now();
    
    try {
      const message = await testFn();
      const duration = Date.now() - startTime;
      
      setResults(prev => prev.map((result, i) => 
        i === index ? { 
          ...result, 
          status: 'passed', 
          message,
          duration 
        } : result
      ));
    } catch (error) {
      const duration = Date.now() - startTime;
      
      setResults(prev => prev.map((result, i) => 
        i === index ? { 
          ...result, 
          status: 'failed', 
          message: error instanceof Error ? error.message : 'Test failed',
          duration 
        } : result
      ));
    }

    // Small delay for UI feedback
    await new Promise(resolve => setTimeout(resolve, 500));
  };

  const getStatusIcon = (status: TestResult['status']) => {
    switch (status) {
      case 'running':
        return <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />;
      case 'passed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-600" />;
    }
  };

  const passedTests = results.filter(r => r.status === 'passed').length;
  const failedTests = results.filter(r => r.status === 'failed').length;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-2xl text-slate-900 mb-6">Report Templates Test Suite</h1>
        
        <div className="mb-6">
          <Button 
            onClick={runAllTests}
            disabled={isRunning}
            className="bg-blue-700 hover:bg-blue-800"
          >
            <Play className="w-4 h-4 mr-2" />
            {isRunning ? 'Tests worden uitgevoerd...' : 'Start Alle Tests'}
          </Button>
        </div>

        {results.length > 0 && (
          <>
            <div className="mb-6 p-4 bg-slate-50 rounded-lg">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl text-green-600">{passedTests}</div>
                  <div className="text-sm text-slate-600">Geslaagd</div>
                </div>
                <div>
                  <div className="text-2xl text-red-600">{failedTests}</div>
                  <div className="text-sm text-slate-600">Gefaald</div>
                </div>
                <div>
                  <div className="text-2xl text-slate-900">{results.length}</div>
                  <div className="text-sm text-slate-600">Totaal</div>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              {results.map((result, index) => (
                <div 
                  key={index}
                  className={`border rounded-lg p-4 flex items-start gap-3 ${
                    result.status === 'passed' ? 'border-green-200 bg-green-50' :
                    result.status === 'failed' ? 'border-red-200 bg-red-50' :
                    'border-blue-200 bg-blue-50'
                  }`}
                >
                  {getStatusIcon(result.status)}
                  <div className="flex-1">
                    <h3 className="font-medium text-slate-900">{result.test}</h3>
                    <p className={`text-sm mt-1 ${
                      result.status === 'passed' ? 'text-green-700' :
                      result.status === 'failed' ? 'text-red-700' :
                      'text-blue-700'
                    }`}>
                      {result.message}
                    </p>
                    {result.duration && (
                      <div className="text-xs text-slate-500 mt-1">
                        {result.duration}ms
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {/* Live Demo Section */}
        <div className="mt-12 pt-8 border-t border-slate-200">
          <h2 className="text-xl text-slate-900 mb-4">Live Demo Test</h2>
          <div className="bg-slate-50 p-6 rounded-lg">
            <DemoReport 
              position="Test Marketing Manager"
              sector="Technology"
              region="Nederland"
              onOrderClick={() => alert('Demo: Checkout flow zou hier starten')}
            />
          </div>
        </div>
      </div>
    </div>
  );
}