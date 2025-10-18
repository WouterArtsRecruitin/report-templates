import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './Dashboard';
import AssessmentForm from './components/AssessmentForm';
import AssessmentRapport from './components/AssessmentRapport';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/assessment" element={<AssessmentForm />} />
          <Route path="/rapport" element={<AssessmentRapport />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
