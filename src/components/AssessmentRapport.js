import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function AssessmentRapport() {
  const location = useLocation();
  const navigate = useNavigate();
  const { report } = location.state || {};

  if (!report) {
    return <div>Geen rapport beschikbaar</div>;
  }

  const renderScoreIndicator = (score) => {
    let color, label;
    if (score < 40) {
      color = 'red';
      label = 'Verbetering nodig';
    } else if (score < 70) {
      color = 'orange';
      label = 'Gemiddeld';
    } else {
      color = 'green';
      label = 'Excellent';
    }

    return (
      <div className="score-indicator">
        <div 
          className="score-circle" 
          style={{
            backgroundColor: color,
            width: '100px',
            height: '100px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold'
          }}
        >
          {report.overallScore}
        </div>
        <p>{label}</p>
      </div>
    );
  };

  return (
    <div className="rapport-container">
      <header>
        <h1>Jouw Recruitment Assessment Rapport</h1>
      </header>

      <section className="overall-score">
        <h2>Totaal Score</h2>
        {renderScoreIndicator(report.overallScore)}
      </section>

      <section className="benchmarks">
        <h2>Benchmark Vergelijking</h2>
        <div className="benchmark-grid">
          <div className="benchmark-item">
            <h3>Time to Hire</h3>
            <p>Jouw score: {report.benchmarks.timeToHire.yourscore} dagen</p>
            <p>Branche gemiddelde: {report.benchmarks.timeToHire.industry_average} dagen</p>
          </div>
          <div className="benchmark-item">
            <h3>Kosten per Aanname</h3>
            <p>Jouw score: €{report.benchmarks.costPerHire.yourscore}</p>
            <p>Branche gemiddelde: €{report.benchmarks.costPerHire.industry_average}</p>
          </div>
        </div>
      </section>

      <section className="personalized-insights">
        <h2>Gepersonaliseerde Insights</h2>
        <div className="insights-content">
          {report.personalizedInsights}
        </div>
      </section>

      <section className="recommendations">
        <h2>Top Aanbevelingen</h2>
        <ul>
          {report.recommendations.map((rec, index) => (
            <li key={index}>{rec}</li>
          ))}
        </ul>
      </section>

      <section className="next-steps">
        <h2>Volgende Stappen</h2>
        <button onClick={() => navigate('/assessment')}>
          Nog een assessment doen
        </button>
        <button onClick={() => {/* Boek consultatie */}}>
          Plan een consultatie
        </button>
      </section>
    </div>
  );
}

export default AssessmentRapport;
