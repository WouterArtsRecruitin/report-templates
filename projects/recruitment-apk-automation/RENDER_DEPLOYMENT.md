# Render Deployment - Recruitment APK Webhook Handler

## Overview

Deze webhook handler verwerkt Typeform submissions voor de Recruitment APK maturity scan en:
1. Ontvangt Typeform webhook
2. Berekent recruitment maturity score
3. Genereert APK rapport met Claude AI
4. Maakt/update deal in Pipedrive
5. Stuurt APK rapport email
6. Triggert email automation sequence

## Deployment naar Render

### Stap 1: Render Account Setup

1. Ga naar [render.com](https://render.com) en log in
2. Klik op "New" → "Web Service"
3. Connect je GitHub repository

### Stap 2: Service Configuratie

| Setting | Value |
|---------|-------|
| Name | `recruitment-apk-webhook` |
| Region | `Frankfurt (EU)` |
| Branch | `main` of `stoic-payne` |
| Root Directory | `projects/recruitment-apk-automation` |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn webhook_handler_apk:app` |

### Stap 3: Environment Variables

Stel deze in via Render Dashboard → Environment:

| Variable | Value | Description |
|----------|-------|-------------|
| `CLAUDE_API_KEY` | `sk-ant-...` | Anthropic API key voor rapport generatie |
| `PIPEDRIVE_API_TOKEN` | `57720aa...` | Pipedrive API token |
| `SMTP_HOST` | `smtp.gmail.com` | Email server |
| `SMTP_PORT` | `587` | SMTP port |
| `SMTP_USER` | `artsrecruitin@gmail.com` | Afzender email |
| `SMTP_PASS` | `xxxx xxxx xxxx xxxx` | Gmail App Password |

### Stap 4: Deploy

1. Klik "Create Web Service"
2. Wacht tot deployment klaar is
3. Noteer de service URL: `https://recruitment-apk-webhook.onrender.com`

## Typeform Webhook Configureren

### In Typeform:

1. Open form: https://form.typeform.com/to/cuGe3IEC
2. Ga naar "Connect" → "Webhooks"
3. Klik "Add a webhook"
4. URL: `https://recruitment-apk-webhook.onrender.com/webhook/typeform`
5. Klik "Save webhook"

### Test de Webhook:

```bash
curl -X POST https://recruitment-apk-webhook.onrender.com/webhook/typeform \
  -H "Content-Type: application/json" \
  -d '{
    "form_response": {
      "token": "test123",
      "answers": [
        {
          "type": "contact_info",
          "contact_info": {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "company": "Test BV"
          }
        }
      ]
    }
  }'
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Health check |
| `/webhook/typeform` | POST | Typeform webhook handler |

## Flow Diagram

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Typeform   │────▶│  Render Webhook │────▶│   Claude AI  │
│  (cuGe3IEC) │     │    Handler      │     │ (APK Report) │
└─────────────┘     └────────┬────────┘     └──────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Pipedrive    │
                    │  Deal Creation  │
                    │  Stage: "APK    │
                    │   Verzonden"    │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                              ▼
     ┌─────────────────┐          ┌─────────────────┐
     │  Email Report   │          │   Automation    │
     │  (Direct SMTP)  │          │   Triggered     │
     └─────────────────┘          │  (8 emails over │
                                  │    30 dagen)    │
                                  └─────────────────┘
```

## Pipedrive Automation

Wanneer een deal in stage "APK Verzonden" (id: 108) komt:

1. **Email 1** - Dag 1: APK ontvangen check
2. **Email 2** - Dag 3: Al bekeken?
3. **Email 3** - Dag 5: Eerste stappen?
4. **Email 4** - Dag 8: Tip: Time-to-hire
5. **Email 5** - Dag 11: Tip: Candidate Experience
6. **Email 6** - Dag 14: Tip: Meten = Weten
7. **Email 7** - Dag 21: Gesprek aanbod
8. **Email 8** - Dag 30: Final check-in

## Monitoring

### Render Logs

```bash
# Via Render Dashboard
# Go to: Services → recruitment-apk-webhook → Logs
```

### Health Check

```bash
curl https://recruitment-apk-webhook.onrender.com/health
# Expected: {"status": "ok"}
```

## Troubleshooting

### Webhook niet ontvangen
- Check Typeform webhook status (groene checkmark)
- Verify Render service is running
- Check Render logs voor errors

### Email niet verstuurd
- Verify SMTP credentials
- Check Gmail "Less secure apps" of App Password
- Review Render logs

### Pipedrive deal niet aangemaakt
- Verify PIPEDRIVE_API_TOKEN
- Check API rate limits
- Review custom field keys

### Claude rapport generatie faalt
- Verify CLAUDE_API_KEY
- Check API quota
- Falls back to basic report if unavailable

## Local Development

```bash
cd projects/recruitment-apk-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export CLAUDE_API_KEY="sk-ant-..."
export PIPEDRIVE_API_TOKEN="..."
export SMTP_PASS="..."

# Run locally
python webhook_handler_apk.py

# Test
curl -X POST http://localhost:5000/webhook/typeform \
  -H "Content-Type: application/json" \
  -d '{"form_response": {"token": "test", "answers": []}}'
```

## Files

| File | Description |
|------|-------------|
| `webhook_handler_apk.py` | Main Flask application |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render Blueprint configuration |
| `RENDER_DEPLOYMENT.md` | This documentation |

---

*Last updated: November 2024*
