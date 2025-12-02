# Apollo MCP Server

Een MCP (Model Context Protocol) server voor Apollo.io sales intelligence platform.

## Features

| Categorie | Tools |
|-----------|-------|
| **Enrichment** | Enrich person, Bulk enrich (10x), Enrich organization |
| **Search** | People search (210M+ database), Organization search |
| **Contacts** | Create, Update, Search contacts |
| **Accounts** | Create, Update, Search accounts |
| **Sequences** | Search sequences, Add contacts to sequence |
| **Tasks** | Create, Search tasks |
| **Deals** | Create, List deals |
| **Utility** | API usage, List users, List email accounts |

## Installatie

```bash
# Clone of download
cd apollo-mcp-server

# Dependencies installeren
npm install

# Builden
npm run build
```

## Configuratie

### Claude Desktop (macOS)

Voeg toe aan `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "apollo": {
      "command": "node",
      "args": ["/pad/naar/apollo-mcp-server/dist/index.js"],
      "env": {}
    }
  }
}
```

### Claude Desktop (Windows)

Voeg toe aan `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "apollo": {
      "command": "node",
      "args": ["C:\\pad\\naar\\apollo-mcp-server\\dist\\index.js"],
      "env": {}
    }
  }
}
```

### HTTP Server Mode

```bash
# Start HTTP server op poort 3000
TRANSPORT=http npm start

# Of met custom poort
TRANSPORT=http PORT=8080 npm start
```

## Gebruik

### 1. Configureren (verplicht eerste stap)

```
apollo_configure
- apiKey: "ODnd_iegDkNIEt6tNqd0Eg"
- userId: "14438360"
```

### 2. Person Enrichment

```
apollo_enrich_person
- email: "tim@apollo.io"
- revealPhoneNumber: true
```

### 3. People Search

```
apollo_search_people
- personTitles: ["HR Manager", "Recruiter"]
- personLocations: ["Netherlands"]
- organizationNumEmployeesRanges: ["50,200", "200,500"]
- perPage: 50
```

### 4. Organization Enrichment

```
apollo_enrich_organization
- domain: "apollo.io"
```

### 5. Contact Management

```
apollo_create_contact
- firstName: "Jan"
- lastName: "de Vries"
- email: "jan@bedrijf.nl"
- title: "HR Director"
- organizationName: "Bedrijf B.V."
```

### 6. Sequence Management

```
apollo_search_sequences
- activeOnly: true

apollo_add_contacts_to_sequence
- sequenceId: "seq_123"
- contactIds: ["contact_1", "contact_2"]
- emailAccountId: "email_acc_123"
```

## API Credits

| Actie | Credits |
|-------|---------|
| People Search | 1 per pagina |
| Person Enrichment | 1 per match |
| Reveal Email | +1 |
| Reveal Phone | +1 |
| Organization Enrichment | 1 per match |

Check usage met `apollo_get_api_usage`.

## Rate Limits

- Per-minute, hourly, en daily limits
- Rate limit info in elke response
- 429 error bij overschrijding

## Recruitment Use Cases

### ICP Prospecting

```
apollo_search_people
- personTitles: ["HR Manager", "Talent Acquisition", "Recruiter"]
- personLocations: ["Gelderland", "Overijssel", "Noord-Brabant"]
- organizationNumEmployeesRanges: ["50,200", "200,500", "500,1000"]
- perPage: 100
```

### Company Research

```
apollo_enrich_organization
- domain: "target-company.nl"
```

### Lead Import naar Pipedrive

1. Search people in Apollo
2. Create contacts in Apollo
3. Sync naar Pipedrive via Zapier

## Development

```bash
# Watch mode
npm run dev

# Build
npm run build

# Test
npm start
```

## Troubleshooting

| Error | Oplossing |
|-------|-----------|
| 401 Unauthorized | Check API key |
| 403 Forbidden | Master key vereist of plan upgrade |
| 429 Rate Limited | Wacht tot reset time |
| No match found | Meer data meegeven (email + domain) |

## License

MIT - Recruitin B.V.
