# META CAMPAIGN AUTOMATION - SETUP GUIDE

## Complete setup voor kandidatentekort.nl Meta campagnes

---

## 📋 OVERZICHT

Dit systeem automatiseert:
1. **OAuth Token Management** - Beheer Meta API toegang
2. **Meta Pixel Tracking** - Client-side en server-side tracking
3. **Lead Ads Processing** - Automatische lead verwerking naar Slack/Pipedrive
4. **Campaign Automation** - Voorgebouwde campagne templates en audiences
5. **Conversion API** - Server-side event tracking voor betere attributie

---

## 🔴 STAP 1: TECHNISCHE BLOCKERS FIXEN

### 1.1 Nieuwe OAuth Token Genereren (15 min)

1. Ga naar [Meta Business Suite](https://business.facebook.com)
2. Navigeer naar **Settings > Business Settings > Users > System Users**
3. Maak een nieuwe System User aan of selecteer bestaande
4. Ga naar **Assets > Add Assets** en voeg toe:
   - Ad Account
   - Pages
   - Pixels
5. Genereer een nieuw token met deze permissions:
   - `ads_read`
   - `ads_management`
   - `leads_retrieval`
   - `pages_read_engagement`
   - `pages_manage_ads`
   - `business_management`

**Alternatief via Graph API Explorer:**
1. Ga naar [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Selecteer je App
3. Voeg permissions toe (ads_read, ads_management, leads_retrieval)
4. Generate Access Token
5. Wissel om naar Long-Lived Token:

```bash
curl "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
```

### 1.2 Meta Pixel Deployen op kandidatentekort.nl (30 min)

**Pixel ID:** `1443564313411457`

#### Via Netlify (kandidatentekortv2):

1. Open `index.html` van je Netlify site
2. Voeg deze code toe in de `<head>` sectie:

```html
<!-- Meta Pixel Code for kandidatentekort.nl -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1443564313411457');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1443564313411457&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
```

3. Deploy naar Netlify
4. Verifieer met [Facebook Pixel Helper](https://chrome.google.com/webstore/detail/facebook-pixel-helper/fdgfkebogiimcoedlicjlajpkdmockpc) Chrome extensie

#### Event Tracking toevoegen:

```html
<!-- Voeg toe voor </body> -->
<script>
// Lead event op form submit
document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function() {
        fbq('track', 'Lead', {
            content_name: 'Form Submission',
            value: 50,
            currency: 'EUR'
        });
    });
});

// InitiateCheckout op assessment start
if (window.location.pathname.includes('/assessment')) {
    fbq('track', 'InitiateCheckout', {
        content_name: 'Assessment Started'
    });
}
</script>
```

---

## 🟡 STAP 2: CONVERSION TRACKING OPZETTEN

### 2.1 Typeform Webhook Herstellen (20 min)

1. Ga naar [Typeform](https://admin.typeform.com)
2. Open je formulier > **Connect** > **Webhooks**
3. Voeg webhook toe:
   - URL: `https://your-render-app.onrender.com/webhook/typeform`
   - Status: Active

**Test de webhook:**
```bash
curl -X POST https://your-render-app.onrender.com/webhook/typeform \
  -H "Content-Type: application/json" \
  -d '{"form_response":{"answers":[{"type":"email","email":"test@test.com"}]}}'
```

### 2.2 Server-Side Conversion API (20 min)

De server stuurt automatisch events naar Meta wanneer:
- Lead formulier wordt ingevuld
- Assessment wordt gestart
- Assessment wordt voltooid

**Test conversie event:**
```bash
curl -X POST https://your-render-app.onrender.com/api/conversion/lead \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "content_name": "Test Lead"
  }'
```

### 2.3 Verifieer Tracking (15 min)

1. Installeer [Facebook Pixel Helper](https://chrome.google.com/webstore/detail/facebook-pixel-helper/fdgfkebogiimcoedlicjlajpkdmockpc)
2. Ga naar kandidatentekort.nl
3. Check of PageView event wordt getriggerd
4. Vul test formulier in
5. Check in [Events Manager](https://business.facebook.com/events_manager) of Lead event binnenkomt

---

## 🟢 STAP 3: CAMPAGNE LANCEREN

### 3.1 Audiences Aanmaken (30 min)

Het systeem heeft 15 voorgebouwde audience segments:

| Segment | Beschrijving | Bereik |
|---------|--------------|--------|
| HR Directors | Senior HR beslissers | 15-25K |
| HR Managers | HR Managers & HRBP's | 40-60K |
| Operations/COO | Operations leiders | 20-35K |
| Recruitment Agencies | Bureau eigenaren | 5-10K |
| SME Owners | MKB ondernemers | 80-120K |
| Tech Sector | HR in tech bedrijven | 10-18K |
| Industry/Manufacturing | HR in industrie | 12-20K |
| Healthcare | HR in zorg | 8-15K |
| Retargeting 7d | Recente bezoekers | 500-2K |
| Retargeting 30d | Website bezoekers | 1.5-5K |

**Audiences bekijken:**
```bash
curl https://your-render-app.onrender.com/api/audiences
```

### 3.2 Campagne Templates (45 min)

Beschikbare templates:

#### Cold - HR Directors
- Budget: €35/dag
- Objective: Lead Generation
- Audiences: HR Directors
- 3 ad copy varianten

#### Cold - Operations
- Budget: €25/dag
- Objective: Lead Generation
- Audiences: Operations, SME Owners
- 2 ad copy varianten

#### Retargeting
- Budget: €15/dag
- Objective: Conversions
- Audiences: Website Visitors 7d, 30d
- 2 ad copy varianten

**Campagne aanmaken via API:**
```bash
curl -X POST https://your-render-app.onrender.com/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "template": "Kandidatentekort - Cold HR Directors",
    "status": "PAUSED"
  }'
```

### 3.3 Budget Instellen (15 min)

Aanbevolen start budget: **€175/week (€25/dag)**

| Campagne | Daily Budget | Weekly |
|----------|--------------|--------|
| Cold HR Directors | €15 | €105 |
| Cold Operations | €5 | €35 |
| Retargeting | €5 | €35 |
| **Totaal** | **€25** | **€175** |

---

## 🔵 STAP 4: AUTOMATION AANZETTEN

### 4.1 Slack Notifications (#high-priority-intakes)

1. Ga naar [Slack App Directory](https://api.slack.com/apps)
2. Create New App > From scratch
3. Incoming Webhooks > Activate
4. Add New Webhook to Workspace
5. Selecteer #high-priority-intakes
6. Kopieer Webhook URL
7. Voeg toe aan environment:
   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

**Test Slack notification:**
```bash
curl -X POST https://your-render-app.onrender.com/test/lead \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@company.nl",
    "first_name": "Test",
    "company_name": "Test BV"
  }'
```

### 4.2 Pipedrive Integration

Leads worden automatisch als deal aangemaakt:
- Pipeline: Kandidatentekort (ID: 3)
- Stage: New Leads (ID: 15)

Environment variabelen:
```
PIPEDRIVE_API_TOKEN=your_token
PIPEDRIVE_PIPELINE_ID=3
PIPEDRIVE_STAGE_ID=15
```

### 4.3 Meta Lead Ads Webhook

1. Ga naar [Facebook App Dashboard](https://developers.facebook.com/apps)
2. Selecteer je app > Webhooks
3. Add Subscription:
   - Object: Page
   - Field: leadgen
   - Callback URL: `https://your-render-app.onrender.com/webhook/meta-leads`
   - Verify Token: `kandidatentekort_verify_2024`

---

## 🚀 DEPLOYMENT

### Deploy naar Render

1. Push code naar GitHub
2. Ga naar [Render Dashboard](https://dashboard.render.com)
3. New > Web Service
4. Connect GitHub repository
5. Configureer:
   - Name: `meta-campaign-automation`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main_server:app`
6. Add Environment Variables (zie `.env.example`)
7. Deploy!

**Health check:**
```bash
curl https://your-render-app.onrender.com/health
```

---

## 📊 API ENDPOINTS OVERZICHT

| Endpoint | Method | Beschrijving |
|----------|--------|--------------|
| `/` | GET | Health check + endpoints lijst |
| `/webhook/meta-leads` | GET/POST | Meta Lead Ads webhook |
| `/webhook/typeform` | POST | Typeform webhook |
| `/api/pixel/code` | GET | Pixel installatie code |
| `/api/pixel/netlify` | GET | Complete Netlify integratie |
| `/api/conversion/lead` | POST | Send Lead event |
| `/api/conversion/assessment` | POST | Send Assessment events |
| `/api/campaigns` | GET/POST | List/Create campaigns |
| `/api/campaigns/<id>/insights` | GET | Campaign insights |
| `/api/templates` | GET | Campaign templates |
| `/api/audiences` | GET | Audience segments |
| `/api/report` | GET | Performance report |
| `/api/token/status` | GET | Check token status |
| `/test/lead` | POST | Test lead processing |

---

## ⚠️ TROUBLESHOOTING

### Token Expired
```bash
# Check token status
curl https://your-render-app.onrender.com/api/token/status

# Refresh token (requires APP_ID and APP_SECRET)
curl -X POST https://your-render-app.onrender.com/api/token/refresh
```

### Pixel Not Firing
1. Check Facebook Pixel Helper extensie
2. Verifieer dat pixel code in `<head>` staat
3. Check browser console voor errors
4. Test met Events Manager Test Events

### Leads Not Coming Through
1. Check webhook URL in Typeform/Meta
2. Verify webhook endpoint: `curl https://your-app.onrender.com/webhook/typeform`
3. Check Render logs voor errors
4. Verify environment variables zijn ingesteld

### Slack Notifications Not Working
1. Test webhook URL direct:
   ```bash
   curl -X POST $SLACK_WEBHOOK_URL \
     -H "Content-Type: application/json" \
     -d '{"text":"Test message"}'
   ```
2. Check channel permissions
3. Verify webhook URL format

---

## 📞 SUPPORT

Bij problemen:
- Check Render logs: `render logs`
- Test endpoints met curl
- Verify environment variables
- Check Meta Events Manager voor events

---

*Last updated: 2024*
