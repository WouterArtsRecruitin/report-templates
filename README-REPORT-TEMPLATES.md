# Professional Report Templates System

Een complete template-bibliotheek voor het genereren van professionele marktonderzoek rapporten en demo versies voor websites.

## 🎯 Overzicht

Dit systeem biedt:
- **Herbruikbare rapport templates** voor consistente branding
- **Demo versies** voor website previews met vergrendelde content
- **Professionele versies** voor volledige rapporten
- **Automatische data generatie** op basis van positie en sector
- **Print-geoptimaliseerde** layouts (A4 formaat)
- **Interactieve charts** met Recharts
- **TypeScript** voor type-veiligheid

## 📁 Bestand Structuur

```
src/
├── components/
│   ├── ReportTemplate.tsx      # Basis template component
│   ├── DemoReport.tsx         # Demo versie voor websites  
│   ├── ProfessionalReport.tsx # Volledige rapport versie
│   ├── charts/
│   │   └── ReportCharts.tsx   # Herbruikbare chart components
│   └── index.ts              # Export barrel
├── types/
│   └── report.ts             # TypeScript interfaces
├── utils/
│   └── reportDataGenerator.ts # Automatische data generatie
└── examples/
    └── ExampleUsage.tsx       # Gebruiksvoorbeelden
```

## 🚀 Snelle Start

### 1. Demo Report voor Website

```tsx
import { DemoReport } from './src/components';

function MarketingPage() {
  return (
    <DemoReport 
      position="Senior Marketing Manager"
      sector="Tech & Digital"
      region="Nederland"
      onOrderClick={() => {
        window.location.href = '/checkout';
      }}
    />
  );
}
```

### 2. Custom Data met Generator

```tsx
import { DemoReport, generateReportData } from './src/components';

function CustomReportDemo() {
  const data = generateReportData({
    position: "Data Scientist",
    sector: "FinTech", 
    region: "DACH Region",
    companyName: "Jouw Bedrijf"
  });

  return (
    <DemoReport 
      position={data.config.title}
      customData={data}
      onOrderClick={() => {
        // Analytics tracking
        gtag('event', 'report_purchase', { 
          value: data.config.price 
        });
      }}
    />
  );
}
```

### 3. Professional Report

```tsx
import { ProfessionalReport, createProfessionalReportData } from './src/components';

function InternalReport() {
  const data = createProfessionalReportData({
    config: {
      title: "Frontend Developer",
      companyName: "Internal Research",
      totalPages: 60
    },
    metrics: {
      activeOpenings: 3200,
      marketSweetSpot: 72,
      // ... andere metrics
    }
  });

  return (
    <ProfessionalReport 
      data={data}
      showPrintControls={true}
    />
  );
}
```

## 🎨 Template Features

### Demo Report
- **2 preview pagina's** + vergrendelde content
- **Call-to-action** voor volledige rapport
- **Pricing display** met download button
- **Print preview** functionality
- **Automatic data generation**

### Professional Report  
- **Volledige toegang** tot alle content
- **Geen vergrendelde secties**
- **Print geoptimaliseerd** voor A4
- **Custom branding** opties
- **Export functies**

### Charts & Visualisaties
- **Line charts** voor trend data
- **Bar charts** voor salaris distributie  
- **Competitor tables** met styling
- **Opportunity scores** met progress bars
- **Responsive design** voor alle schermformaten

## 🔧 Configuratie Opties

### Report Config
```typescript
interface ReportConfig {
  title: string;           // "Senior Marketing Manager"
  subtitle: string;        // "Tech Sector • Nederland"  
  sector: string;          // Voor data generatie
  region: string;          // Geografische scope
  companyName: string;     // Branding
  totalPages: number;      // Rapport lengte
  price: number;          // Demo pricing
  reliabilityScore: number; // Data betrouwbaarheid %
}
```

### Market Metrics
```typescript
interface MarketMetrics {
  activeOpenings: number;     // Actieve vacatures
  avgCandidates: number;      // Gemiddeld aantal sollicitanten  
  marketSweetSpot: number;    // Optimaal salaris (in k)
  salaryRange: {min, max};    // Salaris range
  timeToHire: number;         // Gemiddelde tijd (dagen)
  // + growth percentages
}
```

## 🤖 Automatische Data Generatie

Het systeem genereert automatisch realistische data op basis van:

### Positie Analyse
- **Seniority level** (Junior/Mid/Senior/Lead/Director)
- **Role type** (Engineer/Manager/Analyst/Designer)
- **Salary calculations** op basis van niveau en sector

### Sector Multipliers
```typescript
const sectorMultipliers = {
  'Technology': 1.3,    // +30% vraag/salaris
  'FinTech': 1.1,       // +10% 
  'Healthcare': 0.9,    // -10%
  'Education': 0.7      // -30%
};
```

### Smart Chart Generation
- **6 maanden trend data** met realistische groei
- **Salary distributie** met normale verdeling
- **Competitor data** op basis van sector
- **Executive summary** met dynamische content

## 💡 Gebruik Cases

### 1. Website Lead Generation
```tsx
// Gebruik op landing pages voor market intelligence
<DemoReport 
  position="Frontend Developer"
  onOrderClick={() => {
    // Lead capture
    openCheckoutModal();
  }}
/>
```

### 2. Sales Presentations  
```tsx
// Volledig rapport voor klanten
<ProfessionalReport 
  data={clientSpecificData}
  showPrintControls={true}
/>
```

### 3. Internal Research
```tsx
// Bulk rapport generatie
const reports = positions.map(pos => 
  generateReportData({
    position: pos,
    sector: "Technology"
  })
);
```

### 4. A/B Testing
```tsx
// Test verschillende posities/sectoren
const [testVariant, setTestVariant] = useState('A');

const reportConfig = testVariant === 'A' ? {
  position: "Marketing Manager",
  sector: "Technology" 
} : {
  position: "Senior Marketing Manager", 
  sector: "FinTech"
};
```

## 🎯 Best Practices

### Performance
- Use `React.useMemo` voor data generatie
- Lazy load charts met `ResponsiveContainer`  
- Optimize print CSS met `@media print`

### SEO & Analytics
```tsx
onOrderClick={() => {
  // Analytics tracking
  gtag('event', 'report_order', {
    position: selectedPosition,
    value: reportPrice
  });
  
  // Lead tracking
  trackConversion('market_report', reportPrice);
}
```

### Customization
```tsx
// Custom branding
const brandedData = createProfessionalReportData({
  config: {
    companyName: "Jouw Bedrijf Intelligence",
    division: "Market Research Team"
  }
});
```

## 🔒 Demo vs Professional

| Feature | Demo | Professional |
|---------|------|--------------|
| Preview Pages | 2 | Alle |
| Charts | Basis | Uitgebreid |
| Pricing Display | Ja | Nee |
| Print Controls | Beperkt | Volledig |
| Custom Branding | Template | Volledig |
| Data Access | Beperkt | Volledig |

## 🛠 Development

### Nieuwe Posities Toevoegen
```typescript
// In reportDataGenerator.ts
function calculateBaseSalary(position: string, sector: string) {
  if (position.includes('DevOps')) {
    baseSalary += 12; // Premium voor DevOps
  }
  // Voeg nieuwe posities toe...
}
```

### Nieuwe Charts
```tsx
// In ReportCharts.tsx
export function NewChartType({ data }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      {/* Jouw custom chart */}
    </ResponsiveContainer>
  );
}
```

### Custom Styling
```css
/* Print-specific styles */
@media print {
  .report-page {
    page-break-after: always;
    margin: 0;
    padding: 2rem;
  }
}
```

Dit template systeem biedt een solide basis voor professionele rapporten met maximale herbruikbaarheid en aanpasbaarheid.