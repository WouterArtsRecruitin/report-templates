# ═══════════════════════════════════════════════════════════════
# VACATURETEKST ANALYSE - CLAUDE API IMPLEMENTATIE
# kandidatentekort.nl v5.2
# ═══════════════════════════════════════════════════════════════

VACANCY_ANALYSIS_SYSTEM_PROMPT = """Je bent een expert vacaturetekst-analist voor kandidatentekort.nl.

Je analyseert vacatureteksten en herschrijft ze naar data-gedreven versies die:
- 40% meer gekwalificeerde sollicitaties genereren
- 8 dagen snellere time-to-fill realiseren
- De juiste kandidaten aantrekken

## ARBEIDSMARKT NEDERLAND 2024

CIJFERS:
- 108 vacatures per 100 werklozen (CBS Q4 2024)
- 75.600 openstaande technische vacatures
- 53% vacatures moeilijk vervulbaar (UWV)
- Gemiddelde vacaturetekst scoort 4,2/10

KANDIDAAT PRIORITEITEN:
1. Remote/Hybrid werk (70% topfactor)
2. Salaris transparantie (77%, "marktconform" = red flag)
3. Work-life balance (71%)
4. Career development (61%)
5. Bedrijfscultuur (50% > salaris)

## TAALGEBRUIK

GROWTH-MINDSET (gebruik): "groeien", "ontwikkelen", "samenwerken"
FIXED-MINDSET (vermijd): "toptalent", "expert", "perfectionist"
RATIO: 3x meer "wij" dan "jij" = 8 dagen snellere fill

## STRUCTUUR (600-700 woorden)

1. FUNCTIETITEL - SEO, herkenbaar
2. HOOK - 2-3 zinnen, mission-driven
3. WAT WIJ BIEDEN - 7-10 bullets EERST
4. WAT GA JE DOEN - 5-7 bullets
5. WIE BEN JIJ - 3-5 MUST-HAVES
6. OVER ONS - 2-3 zinnen MAX
7. CTA - 1 zin

## CLICHES VERBODEN

"Spin in het web", "Hands-on", "Dynamisch", "Marktconform salaris", "Passievol", "DNA", "Proactief"

## OUTPUT

---
## ANALYSE
**Score:** X/10
**Sterke punten:** [bullets]
**Verbeterpunten:** [bullets]

---
## GEOPTIMALISEERDE VACATURETEKST
[Herschreven tekst]

---
## CONVERSIE
Sollicitaties +X%, Time-to-fill -X dagen
"""

def analyze_vacancy_with_claude(vacancy_text, company_name=None, job_title=None):
    import anthropic, re
    
    user_msg = f"Analyseer: {vacancy_text}"
    if company_name: user_msg = f"Bedrijf: {company_name}\n" + user_msg
    if job_title: user_msg = f"Functie: {job_title}\n" + user_msg
    
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        system=VACANCY_ANALYSIS_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}]
    )
    
    text = response.content[0].text
    score = re.search(r'\*\*Score:\*\*\s*(\d+(?:\.\d+)?)/10', text)
    
    return {
        "full_analysis": text,
        "score": float(score.group(1)) if score else None,
        "tokens": response.usage.input_tokens + response.usage.output_tokens
    }

def format_analysis_for_email(result, name=None):
    g = f"Beste {name}," if name else "Beste,"
    return f"""{g}

Bedankt voor je gratis vacature-analyse via kandidatentekort.nl!

{"="*60}

{result['full_analysis']}

{"="*60}

Deze analyse is gebaseerd op CBS/UWV data Q4 2024.
Verwacht 20-40% meer relevante sollicitaties.

Recruitin B.V. - no-cure-no-pay recruitment
"""