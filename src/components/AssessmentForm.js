import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const REGULAR_QUESTIONS = [
  {
    id: 1,
    text: "In welke sector is jouw bedrijf actief?",
    type: 'select',
    options: [
      'Tech', 'Industrie', 'Dienstverlening', 
      'Zorg', 'Overheid', 'Onderwijs', 'Andere'
    ]
  },
  {
    id: 2,
    text: "Wat is je grootste recruitment uitdaging?",
    type: 'select',
    options: [
      'Kandidaten vinden', 
      'Juiste kandidaten selecteren', 
      'Snelheid van werving', 
      'Kosten beheersen', 
      'Diversiteit'
    ]
  },
  {
    id: 3,
    text: "Hoeveel mensen werf je per jaar?",
    type: 'select',
    options: [
      '1-5', '6-10', '11-25', '26-50', '51-100', '100+'
    ]
  },
  {
    id: 4,
    text: "Hoe vaak slaag je erin vacatures in te vullen?",
    type: 'select',
    options: [
      '< 25%', '25-50%', '50-75%', '75-90%', '> 90%'
    ]
  },
  {
    id: 5,
    text: "Hoe lang duurt het gemiddeld om een kandidaat aan te nemen?",
    type: 'select',
    options: [
      '< 2 weken', '2-4 weken', '1-2 maanden', 
      '2-3 maanden', '3-6 maanden', '> 6 maanden'
    ]
  },
  {
    id: 6,
    text: "Wat zijn de kosten per aanname?",
    type: 'select',
    options: [
      '< €2.500', '€2.500-5.000', '€5.000-7.500', 
      '€7.500-10.000', '> €10.000'
    ]
  },
  {
    id: 7,
    text: "Hoe lang blijven nieuwe medewerkers gemiddeld?",
    type: 'select',
    options: [
      '< 6 maanden', '6-12 maanden', '1-2 jaar', 
      '2-3 jaar', '3-5 jaar', '> 5 jaar'
    ]
  },
  {
    id: 8,
    text: "Waar vind je kandidaten?",
    type: 'multiselect',
    options: [
      'LinkedIn', 'Indeed', 'Recruitmentbureaus', 
      'Eigen netwerk', 'Vacaturesites', 'Social media'
    ]
  },
  {
    id: 9,
    text: "Hoeveel mensen zijn betrokken in het selectieproces?",
    type: 'select',
    options: [
      '1-2', '3-4', '5-6', '7-8', '9-10', '> 10'
    ]
  },
  {
    id: 10,
    text: "Hoe ervaar je de kwaliteit van kandidaten?",
    type: 'select',
    options: [
      'Zeer laag', 'Laag', 'Gemiddeld', 'Hoog', 'Zeer hoog'
    ]
  },
  {
    id: 11,
    text: "Welke recruitment tools gebruik je?",
    type: 'multiselect',
    options: [
      'ATS', 'LinkedIn Recruiter', 'Indeed', 
      'Greenhouse', 'Workday', 'Andere'
    ]
  },
  {
    id: 12,
    text: "Hoe professioneel zijn je vacatureteksten?",
    type: 'select',
    options: [
      'Zeer basaal', 'Standaard', 'Goed', 'Excellent', 'Toonaangevend'
    ]
  },
  {
    id: 13,
    text: "Welk kanaal levert de beste kandidaten?",
    type: 'select',
    options: [
      'LinkedIn', 'Referrals', 'Recruitmentbureaus', 
      'Eigen website', 'Vakgerichte netwerken'
    ]
  },
  {
    id: 14,
    text: "Hoe duidelijk is je werkgeversmerk?",
    type: 'select',
    options: [
      'Niet zichtbaar', 'Beperkt', 'Redelijk', 'Duidelijk', 'Zeer sterk'
    ]
  },
  {
    id: 15,
    text: "Hoe gestructureerd is je recruitment proces?",
    type: 'select',
    options: [
      'Ad-hoc', 'Basaal', 'Gedefinieerd', 'Geoptimaliseerd', 'Hoogwaardige standaard'
    ]
  }
];

const BINARY_QUESTIONS = [
  {
    id: 16,
    text: "Prioriteit: Snelheid of Perfecte Match?",
    options: ['Snelheid', 'Perfecte Match']
  },
  {
    id: 17,
    text: "Focus: Kostenbeheersing of Kwaliteit?",
    options: ['Kostenbeheersing', 'Kwaliteit']
  },
  {
    id: 18,
    text: "Aanpak: Persoonlijk of Data-driven?",
    options: ['Persoonlijk', 'Data-driven']
  },
  {
    id: 19,
    text: "Urgentie: Hoge prioriteit of Strategische verbetering?",
    options: ['Hoge prioriteit', 'Strategische verbetering']
  }
];

function AssessmentForm() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [leadData, setLeadData] = useState({
    name: '',
    email: '',
    company: ''
  });

  const totalSteps = REGULAR_QUESTIONS.length + BINARY_QUESTIONS.length + 1;

  const handleAnswer = (questionId, answer) => {
    setAnswers(prev => ({...prev, [questionId]: answer}));
    setCurrentStep(prev => prev + 1);
  };

  const handleLeadSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/.netlify/functions/pipedrive-sync', {
        answers,
        binaryAnswers: BINARY_QUESTIONS.reduce((acc, q) => ({
          ...acc, 
          [q.id]: answers[q.id]
        }), {}),
        leadData
      });
      alert('Assessment succesvol ingediend!');
      navigate('/');
    } catch (error) {
      alert('Er ging iets mis. Probeer opnieuw.');
    }
  };

  const renderStep = () => {
    if (currentStep === 0) {
      return (
        <div className="welcome-step">
          <h2>RecruitPro Assessment</h2>
          <p>Ontdek de staat van jouw recruitment proces in slechts 3 minuten!</p>
          <button onClick={() => setCurrentStep(1)}>Start Assessment</button>
        </div>
      );
    }

    if (currentStep <= REGULAR_QUESTIONS.length) {
      const question = REGULAR_QUESTIONS[currentStep - 1];
      return (
        <div className="question-step">
          <h3>{question.text}</h3>
          {question.type === 'select' && (
            <div className="options">
              {question.options.map((option, index) => (
                <button 
                  key={index} 
                  onClick={() => handleAnswer(question.id, option)}
                >
                  {option}
                </button>
              ))}
            </div>
          )}
        </div>
      );
    }

    if (currentStep <= REGULAR_QUESTIONS.length + BINARY_QUESTIONS.length) {
      const question = BINARY_QUESTIONS[currentStep - REGULAR_QUESTIONS.length - 1];
      return (
        <div className="binary-step">
          <h3>{question.text}</h3>
          <div className="options">
            {question.options.map((option, index) => (
              <button 
                key={index} 
                onClick={() => handleAnswer(question.id, option)}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      );
    }

    return (
      <form onSubmit={handleLeadSubmit} className="lead-form">
        <h2>Ontvang je persoonlijke rapport</h2>
        <input
          type="text"
          placeholder="Naam"
          value={leadData.name}
          onChange={(e) => setLeadData(prev => ({...prev, name: e.target.value}))}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={leadData.email}
          onChange={(e) => setLeadData(prev => ({...prev, email: e.target.value}))}
          required
        />
        <input
          type="text"
          placeholder="Bedrijf"
          value={leadData.company}
          onChange={(e) => setLeadData(prev => ({...prev, company: e.target.value}))}
          required
        />
        <button type="submit">Rapport Ontvangen</button>
      </form>
    );
  };

  return (
    <div className="assessment-container">
      <div className="progress-bar" style={{width: `${(currentStep / totalSteps) * 100}%`}}></div>
      {renderStep()}
    </div>
  );
}

export default AssessmentForm;
