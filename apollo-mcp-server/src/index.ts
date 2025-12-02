#!/usr/bin/env node
/**
 * Apollo.io MCP Server
 * 
 * A comprehensive MCP server for Apollo.io sales intelligence platform.
 * Supports enrichment, contacts, accounts, sequences, tasks, and deals.
 * 
 * @author Recruitin B.V.
 * @version 1.0.0
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";

import {
  setConfig,
  getConfig,
  makeApiRequest,
  formatPerson,
  formatOrganization,
  formatContact,
  formatAccount,
  formatSequence,
  formatPaginatedResponse,
} from "./services/apollo-client.js";

import { analyzeVacancy, formatAnalysisForPipedrive } from "./services/vacancy-analyzer.js";

import {
  VacancyAnalysisSchema,
  ConfigureSchema,
  PersonEnrichmentSchema,
  BulkPersonEnrichmentSchema,
  OrganizationEnrichmentSchema,
  PeopleSearchSchema,
  OrganizationSearchSchema,
  CreateContactSchema,
  UpdateContactSchema,
  SearchContactsSchema,
  CreateAccountSchema,
  UpdateAccountSchema,
  SearchAccountsSchema,
  SearchSequencesSchema,
  AddContactsToSequenceSchema,
  CreateTaskSchema,
  SearchTasksSchema,
  CreateDealSchema,
  ListDealsSchema,
  GetApiUsageSchema,
  ListUsersSchema,
  ListEmailAccountsSchema,
  type VacancyAnalysisInput,
  type ConfigureInput,
  type PersonEnrichmentInput,
  type BulkPersonEnrichmentInput,
  type OrganizationEnrichmentInput,
  type PeopleSearchInput,
  type OrganizationSearchInput,
  type CreateContactInput,
  type UpdateContactInput,
  type SearchContactsInput,
  type CreateAccountInput,
  type UpdateAccountInput,
  type SearchAccountsInput,
  type SearchSequencesInput,
  type AddContactsToSequenceInput,
  type CreateTaskInput,
  type SearchTasksInput,
  type CreateDealInput,
  type ListDealsInput,
} from "./schemas/index.js";

// Initialize MCP Server
const server = new McpServer({
  name: "apollo-mcp-server",
  version: "1.0.0",
});

// ============================================================
// CONFIGURATION TOOL
// ============================================================

server.registerTool(
  "apollo_configure",
  {
    title: "Configure Apollo API",
    description: `Configure the Apollo.io API connection with your API key.

This tool MUST be called first before using any other Apollo tools.

Args:
  - apiKey (string): Your Apollo API key
  - userId (string, optional): Your Apollo User ID

Returns:
  Confirmation of successful configuration.

Example:
  { "apiKey": "ODnd_iegDkNIEt6tNqd0Eg", "userId": "14438360" }`,
    inputSchema: ConfigureSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: ConfigureInput) => {
    setConfig({
      apiKey: params.apiKey,
      userId: params.userId,
    });

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          message: "Apollo API configured successfully",
          userId: params.userId || "not provided",
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// VACANCY ANALYSIS TOOL
// ============================================================

server.registerTool(
  "apollo_analyze_vacancy",
  {
    title: "Analyze Job Vacancy Text",
    description: `Analyze and optimize job vacancy text using kandidatentekort.nl methodology.

This tool analyzes job vacancy texts and provides:
- Quality score (0-10)
- Detailed improvement suggestions
- Optimized rewritten vacancy text
- Expected conversion improvements

Based on Dutch labor market data Q4 2024:
- 108 vacancies per 100 job seekers
- 40% increase in qualified applications
- 8 days faster time-to-fill

Args:
  - vacancyText (string): The job vacancy text to analyze
  - companyName (string, optional): Company name for context
  - jobTitle (string, optional): Job title for context

Returns:
  Comprehensive analysis with score, improvements, and optimized text.`,
    inputSchema: VacancyAnalysisSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: VacancyAnalysisInput) => {
    const result = await analyzeVacancy(
      params.vacancyText,
      params.companyName,
      params.jobTitle
    );

    if (!result.success) {
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            success: false,
            error: result.error,
          }, null, 2),
        }],
      };
    }

    const pipedriveData = formatAnalysisForPipedrive(result);

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          analysis: result.fullAnalysis,
          score: result.score,
          tokensUsed: result.tokens,
          pipedriveData,
          conversionEstimate: {
            applicationsIncrease: `${Math.round((result.score || 0) * 4)}%`,
            timeToFillReduction: `${Math.round((result.score || 0) * 0.8)} days`,
          },
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// ENRICHMENT TOOLS
// ============================================================

server.registerTool(
  "apollo_enrich_person",
  {
    title: "Enrich Person Data",
    description: `Enrich data for a single person using Apollo's database.

Provide email, LinkedIn URL, or name+domain to find and enrich a person's data.
Returns comprehensive professional information including email, phone, title, company, etc.

Args:
  - email (string, optional): Email address
  - firstName (string, optional): First name
  - lastName (string, optional): Last name  
  - domain (string, optional): Company domain
  - linkedinUrl (string, optional): LinkedIn profile URL
  - revealPersonalEmails (boolean): Reveal personal emails (uses credits)
  - revealPhoneNumber (boolean): Reveal phone numbers (uses credits)

Returns:
  Enriched person data including contact info, employment history, social profiles.

Note: Uses API credits. Requires email OR linkedinUrl OR (firstName+lastName+domain).`,
    inputSchema: PersonEnrichmentSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: PersonEnrichmentInput) => {
    const queryParams: Record<string, string | boolean | undefined> = {
      email: params.email,
      first_name: params.firstName,
      last_name: params.lastName,
      name: params.name,
      domain: params.domain,
      organization_name: params.organizationName,
      linkedin_url: params.linkedinUrl,
      reveal_personal_emails: params.revealPersonalEmails,
      reveal_phone_number: params.revealPhoneNumber,
    };

    const response = await makeApiRequest<{ person: Record<string, unknown> }>(
      "/people/match",
      "POST",
      undefined,
      queryParams as Record<string, string | number | boolean | undefined>
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const formatted = response.data?.person ? formatPerson(response.data.person) : null;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          person: formatted,
          rateLimitInfo: response.rateLimitInfo,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_enrich_person_bulk",
  {
    title: "Bulk Enrich People",
    description: `Enrich data for up to 10 people in a single API call.

More efficient than individual calls when enriching multiple people.

Args:
  - people (array): Array of people objects with email/name/domain/linkedinUrl
  - revealPersonalEmails (boolean): Reveal personal emails
  - revealPhoneNumber (boolean): Reveal phone numbers

Returns:
  Array of enriched person data.

Note: Uses API credits for each successful match.`,
    inputSchema: BulkPersonEnrichmentSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: BulkPersonEnrichmentInput) => {
    const details = params.people.map(p => ({
      email: p.email,
      first_name: p.firstName,
      last_name: p.lastName,
      domain: p.domain,
      linkedin_url: p.linkedinUrl,
    }));

    const response = await makeApiRequest<{ matches: Array<{ person: Record<string, unknown> }> }>(
      "/people/bulk_match",
      "POST",
      {
        details,
        reveal_personal_emails: params.revealPersonalEmails,
        reveal_phone_number: params.revealPhoneNumber,
      }
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const formatted = response.data?.matches?.map(m => formatPerson(m.person)) || [];

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: formatted.length,
          people: formatted,
          rateLimitInfo: response.rateLimitInfo,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_enrich_organization",
  {
    title: "Enrich Organization Data",
    description: `Enrich company data using Apollo's database.

Provide a company domain to retrieve comprehensive organization information.

Args:
  - domain (string): Company domain (e.g., "apollo.io")

Returns:
  Organization data including industry, size, funding, technologies, etc.`,
    inputSchema: OrganizationEnrichmentSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: OrganizationEnrichmentInput) => {
    const response = await makeApiRequest<{ organization: Record<string, unknown> }>(
      "/organizations/enrich",
      "GET",
      undefined,
      { domain: params.domain }
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const formatted = response.data?.organization 
      ? formatOrganization(response.data.organization) 
      : null;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          organization: formatted,
          rateLimitInfo: response.rateLimitInfo,
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// SEARCH TOOLS
// ============================================================

server.registerTool(
  "apollo_search_people",
  {
    title: "Search People Database",
    description: `Search Apollo's 210M+ person database with advanced filters.

Find prospects by title, location, seniority, company attributes, and more.

Args:
  - personTitles (array): Job titles (e.g., ["CEO", "VP Sales"])
  - personLocations (array): Locations (e.g., ["Netherlands", "Amsterdam"])
  - personSeniorities (array): Seniority levels (owner, founder, c_suite, vp, director, manager, senior, entry)
  - qOrganizationDomains (array): Company domains to search within
  - organizationLocations (array): Company locations
  - organizationNumEmployeesRanges (array): Employee ranges (e.g., ["50,200"])
  - qKeywords (string): Keyword search
  - page (number): Page number (default: 1)
  - perPage (number): Results per page (default: 25, max: 100)

Returns:
  Paginated list of matching people with professional details.`,
    inputSchema: PeopleSearchSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: PeopleSearchInput) => {
    const body: Record<string, unknown> = {
      page: params.page,
      per_page: params.perPage,
    };

    if (params.personTitles) body.person_titles = params.personTitles;
    if (params.personLocations) body.person_locations = params.personLocations;
    if (params.personSeniorities) body.person_seniorities = params.personSeniorities;
    if (params.qOrganizationDomains) body.q_organization_domains = params.qOrganizationDomains;
    if (params.organizationLocations) body.organization_locations = params.organizationLocations;
    if (params.organizationNumEmployeesRanges) body.organization_num_employees_ranges = params.organizationNumEmployeesRanges;
    if (params.organizationIndustryTagIds) body.organization_industry_tag_ids = params.organizationIndustryTagIds;
    if (params.qKeywords) body.q_keywords = params.qKeywords;

    const response = await makeApiRequest<{
      people: Array<Record<string, unknown>>;
      pagination: { page: number; per_page: number; total_entries: number; total_pages: number };
    }>("/mixed_people/search", "POST", body);

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const people = response.data?.people?.map(formatPerson) || [];
    const pagination = response.data?.pagination;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: people.length,
          pagination: pagination ? {
            page: pagination.page,
            perPage: pagination.per_page,
            totalEntries: pagination.total_entries,
            totalPages: pagination.total_pages,
          } : null,
          people,
          rateLimitInfo: response.rateLimitInfo,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_search_organizations",
  {
    title: "Search Organizations Database",
    description: `Search Apollo's company database with filters.

Args:
  - qOrganizationName (string): Company name search
  - organizationLocations (array): Company locations
  - organizationNumEmployeesRanges (array): Employee ranges
  - qKeywords (string): Keyword search
  - page (number): Page number
  - perPage (number): Results per page

Returns:
  Paginated list of matching organizations.`,
    inputSchema: OrganizationSearchSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: OrganizationSearchInput) => {
    const body: Record<string, unknown> = {
      page: params.page,
      per_page: params.perPage,
    };

    if (params.qOrganizationName) body.q_organization_name = params.qOrganizationName;
    if (params.organizationLocations) body.organization_locations = params.organizationLocations;
    if (params.organizationNumEmployeesRanges) body.organization_num_employees_ranges = params.organizationNumEmployeesRanges;
    if (params.organizationIndustryTagIds) body.organization_industry_tag_ids = params.organizationIndustryTagIds;
    if (params.qKeywords) body.q_keywords = params.qKeywords;

    const response = await makeApiRequest<{
      organizations: Array<Record<string, unknown>>;
      pagination: { page: number; per_page: number; total_entries: number; total_pages: number };
    }>("/mixed_companies/search", "POST", body);

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const orgs = response.data?.organizations?.map(formatOrganization) || [];
    const pagination = response.data?.pagination;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: orgs.length,
          pagination: pagination ? {
            page: pagination.page,
            perPage: pagination.per_page,
            totalEntries: pagination.total_entries,
            totalPages: pagination.total_pages,
          } : null,
          organizations: orgs,
          rateLimitInfo: response.rateLimitInfo,
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// CONTACT TOOLS
// ============================================================

server.registerTool(
  "apollo_create_contact",
  {
    title: "Create Contact",
    description: `Create a new contact in your Apollo account.

A contact is a person explicitly added to your database with enriched data.

Args:
  - firstName (string): First name
  - lastName (string): Last name
  - email (string, optional): Email address
  - title (string, optional): Job title
  - organizationName (string, optional): Company name
  - accountId (string, optional): Link to existing account
  - phone (string, optional): Phone number
  - linkedinUrl (string, optional): LinkedIn URL

Returns:
  Created contact data with ID.`,
    inputSchema: CreateContactSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false,
    },
  },
  async (params: CreateContactInput) => {
    const body: Record<string, unknown> = {
      first_name: params.firstName,
      last_name: params.lastName,
    };

    if (params.email) body.email = params.email;
    if (params.title) body.title = params.title;
    if (params.organizationName) body.organization_name = params.organizationName;
    if (params.websiteUrl) body.website_url = params.websiteUrl;
    if (params.accountId) body.account_id = params.accountId;
    if (params.ownerId) body.owner_id = params.ownerId;
    if (params.phone) body.direct_phone = params.phone;
    if (params.linkedinUrl) body.linkedin_url = params.linkedinUrl;
    if (params.labelIds) body.label_ids = params.labelIds;

    const response = await makeApiRequest<{ contact: Record<string, unknown> }>(
      "/contacts",
      "POST",
      body
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          contact: response.data?.contact ? formatContact(response.data.contact) : null,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_update_contact",
  {
    title: "Update Contact",
    description: `Update an existing contact in your Apollo account.

Args:
  - contactId (string): Contact ID to update
  - firstName, lastName, email, title, phone, etc. (optional): Fields to update

Returns:
  Updated contact data.`,
    inputSchema: UpdateContactSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: UpdateContactInput) => {
    const body: Record<string, unknown> = {};

    if (params.firstName) body.first_name = params.firstName;
    if (params.lastName) body.last_name = params.lastName;
    if (params.email) body.email = params.email;
    if (params.title) body.title = params.title;
    if (params.phone) body.direct_phone = params.phone;
    if (params.accountId) body.account_id = params.accountId;
    if (params.ownerId) body.owner_id = params.ownerId;
    if (params.labelIds) body.label_ids = params.labelIds;

    const response = await makeApiRequest<{ contact: Record<string, unknown> }>(
      `/contacts/${params.contactId}`,
      "PUT",
      body
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          contact: response.data?.contact ? formatContact(response.data.contact) : null,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_search_contacts",
  {
    title: "Search Contacts",
    description: `Search contacts in your Apollo account.

Only returns contacts you've added to your database, not Apollo's full database.

Args:
  - qKeywords (string, optional): Keyword search
  - contactLabelIds (array, optional): Filter by labels
  - accountIds (array, optional): Filter by accounts
  - ownerIds (array, optional): Filter by owners
  - page, perPage: Pagination

Returns:
  Paginated list of your contacts.`,
    inputSchema: SearchContactsSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: SearchContactsInput) => {
    const body: Record<string, unknown> = {
      page: params.page,
      per_page: params.perPage,
    };

    if (params.qKeywords) body.q_keywords = params.qKeywords;
    if (params.contactLabelIds) body.contact_label_ids = params.contactLabelIds;
    if (params.accountIds) body.account_ids = params.accountIds;
    if (params.ownerIds) body.owner_ids = params.ownerIds;

    const response = await makeApiRequest<{
      contacts: Array<Record<string, unknown>>;
      pagination: { page: number; per_page: number; total_entries: number; total_pages: number };
    }>("/contacts/search", "POST", body);

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const contacts = response.data?.contacts?.map(formatContact) || [];
    const pagination = response.data?.pagination;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: contacts.length,
          pagination: pagination ? {
            page: pagination.page,
            perPage: pagination.per_page,
            totalEntries: pagination.total_entries,
            totalPages: pagination.total_pages,
          } : null,
          contacts,
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// ACCOUNT TOOLS
// ============================================================

server.registerTool(
  "apollo_create_account",
  {
    title: "Create Account",
    description: `Create a new account (company) in your Apollo database.

Args:
  - name (string): Company name
  - domain (string, optional): Company domain
  - phone (string, optional): Phone number
  - ownerId (string, optional): Owner user ID

Returns:
  Created account data with ID.`,
    inputSchema: CreateAccountSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false,
    },
  },
  async (params: CreateAccountInput) => {
    const body: Record<string, unknown> = {
      name: params.name,
    };

    if (params.domain) body.domain = params.domain;
    if (params.phone) body.phone = params.phone;
    if (params.ownerId) body.owner_id = params.ownerId;
    if (params.labelIds) body.label_ids = params.labelIds;

    const response = await makeApiRequest<{ account: Record<string, unknown> }>(
      "/accounts",
      "POST",
      body
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          account: response.data?.account ? formatAccount(response.data.account) : null,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_update_account",
  {
    title: "Update Account",
    description: `Update an existing account in your Apollo database.

Args:
  - accountId (string): Account ID to update
  - name, domain, phone, ownerId (optional): Fields to update

Returns:
  Updated account data.`,
    inputSchema: UpdateAccountSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: UpdateAccountInput) => {
    const body: Record<string, unknown> = {};

    if (params.name) body.name = params.name;
    if (params.domain) body.domain = params.domain;
    if (params.phone) body.phone = params.phone;
    if (params.ownerId) body.owner_id = params.ownerId;

    const response = await makeApiRequest<{ account: Record<string, unknown> }>(
      `/accounts/${params.accountId}`,
      "PATCH",
      body
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          account: response.data?.account ? formatAccount(response.data.account) : null,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_search_accounts",
  {
    title: "Search Accounts",
    description: `Search accounts in your Apollo database.

Args:
  - qKeywords (string, optional): Keyword search
  - accountLabelIds (array, optional): Filter by labels
  - ownerIds (array, optional): Filter by owners
  - page, perPage: Pagination

Returns:
  Paginated list of your accounts.`,
    inputSchema: SearchAccountsSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: SearchAccountsInput) => {
    const body: Record<string, unknown> = {
      page: params.page,
      per_page: params.perPage,
    };

    if (params.qKeywords) body.q_keywords = params.qKeywords;
    if (params.accountLabelIds) body.account_label_ids = params.accountLabelIds;
    if (params.ownerIds) body.owner_ids = params.ownerIds;

    const response = await makeApiRequest<{
      accounts: Array<Record<string, unknown>>;
      pagination: { page: number; per_page: number; total_entries: number; total_pages: number };
    }>("/accounts/search", "POST", body);

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const accounts = response.data?.accounts?.map(formatAccount) || [];
    const pagination = response.data?.pagination;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: accounts.length,
          pagination: pagination ? {
            page: pagination.page,
            perPage: pagination.per_page,
            totalEntries: pagination.total_entries,
            totalPages: pagination.total_pages,
          } : null,
          accounts,
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// SEQUENCE TOOLS
// ============================================================

server.registerTool(
  "apollo_search_sequences",
  {
    title: "Search Sequences",
    description: `Search email sequences in your Apollo account.

Args:
  - qKeywords (string, optional): Search by name
  - activeOnly (boolean): Only return active sequences
  - page, perPage: Pagination

Returns:
  List of sequences with performance metrics.`,
    inputSchema: SearchSequencesSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: SearchSequencesInput) => {
    const body: Record<string, unknown> = {
      page: params.page,
      per_page: params.perPage,
    };

    if (params.qKeywords) body.q_keywords = params.qKeywords;
    if (params.activeOnly) body.active = true;

    const response = await makeApiRequest<{
      emailer_campaigns: Array<Record<string, unknown>>;
      pagination: { page: number; per_page: number; total_entries: number; total_pages: number };
    }>("/emailer_campaigns/search", "POST", body);

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    const sequences = response.data?.emailer_campaigns?.map(formatSequence) || [];
    const pagination = response.data?.pagination;

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: sequences.length,
          pagination: pagination ? {
            page: pagination.page,
            perPage: pagination.per_page,
            totalEntries: pagination.total_entries,
            totalPages: pagination.total_pages,
          } : null,
          sequences,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_add_contacts_to_sequence",
  {
    title: "Add Contacts to Sequence",
    description: `Add contacts to an email sequence.

Requires a master API key for this operation.

Args:
  - sequenceId (string): Sequence/campaign ID
  - contactIds (array): Contact IDs to add
  - emailAccountId (string): Email account to send from
  - userId (string, optional): User ID

Returns:
  Confirmation of contacts added.`,
    inputSchema: AddContactsToSequenceSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false,
    },
  },
  async (params: AddContactsToSequenceInput) => {
    const config = getConfig();
    const body: Record<string, unknown> = {
      contact_ids: params.contactIds,
      emailer_campaign_id: params.sequenceId,
      send_email_from_email_account_id: params.emailAccountId,
      user_id: params.userId || config?.userId,
    };

    const response = await makeApiRequest<{ contacts: Array<Record<string, unknown>> }>(
      `/emailer_campaigns/${params.sequenceId}/add_contact_ids`,
      "POST",
      body
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          message: `Added ${params.contactIds.length} contacts to sequence`,
          contacts: response.data?.contacts?.map(formatContact) || [],
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// TASK TOOLS
// ============================================================

server.registerTool(
  "apollo_create_task",
  {
    title: "Create Task",
    description: `Create a new task in Apollo.

Args:
  - userId (string): Assignee user ID
  - type (string): Task type (call, email, linkedin, action_item, other)
  - priority (string): Priority (high, medium, low)
  - dueAt (string, optional): Due date (ISO format)
  - note (string, optional): Task notes
  - contactId (string, optional): Related contact
  - accountId (string, optional): Related account

Returns:
  Created task data.`,
    inputSchema: CreateTaskSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false,
    },
  },
  async (params: CreateTaskInput) => {
    const body: Record<string, unknown> = {
      user_id: params.userId,
      type: params.type,
      priority: params.priority,
    };

    if (params.dueAt) body.due_at = params.dueAt;
    if (params.note) body.note = params.note;
    if (params.contactId) body.contact_id = params.contactId;
    if (params.accountId) body.account_id = params.accountId;

    const response = await makeApiRequest<{ task: Record<string, unknown> }>(
      "/tasks",
      "POST",
      body
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          task: response.data?.task,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_search_tasks",
  {
    title: "Search Tasks",
    description: `Search tasks in your Apollo account.

Args:
  - userIds (array, optional): Filter by assignees
  - contactIds (array, optional): Filter by contacts
  - accountIds (array, optional): Filter by accounts
  - completed (boolean, optional): Filter by status
  - page, perPage: Pagination

Returns:
  List of matching tasks.`,
    inputSchema: SearchTasksSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: SearchTasksInput) => {
    const body: Record<string, unknown> = {
      page: params.page,
      per_page: params.perPage,
    };

    if (params.userIds) body.user_ids = params.userIds;
    if (params.contactIds) body.contact_ids = params.contactIds;
    if (params.accountIds) body.account_ids = params.accountIds;
    if (params.completed !== undefined) body.completed = params.completed;

    const response = await makeApiRequest<{
      tasks: Array<Record<string, unknown>>;
      pagination: { page: number; per_page: number; total_entries: number; total_pages: number };
    }>("/tasks/search", "POST", body);

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: response.data?.tasks?.length || 0,
          tasks: response.data?.tasks,
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// DEAL TOOLS
// ============================================================

server.registerTool(
  "apollo_create_deal",
  {
    title: "Create Deal",
    description: `Create a new deal/opportunity in Apollo.

Args:
  - name (string): Deal name
  - amount (number, optional): Deal value
  - accountId (string, optional): Related account
  - contactIds (array, optional): Related contacts
  - ownerId (string, optional): Deal owner
  - status (string): Status (open, won, lost)

Returns:
  Created deal data.`,
    inputSchema: CreateDealSchema,
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false,
    },
  },
  async (params: CreateDealInput) => {
    const body: Record<string, unknown> = {
      name: params.name,
      status: params.status,
    };

    if (params.amount) body.amount = params.amount;
    if (params.accountId) body.account_id = params.accountId;
    if (params.contactIds) body.contact_ids = params.contactIds;
    if (params.ownerId) body.owner_id = params.ownerId;

    const response = await makeApiRequest<{ opportunity: Record<string, unknown> }>(
      "/opportunities",
      "POST",
      body
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          deal: response.data?.opportunity,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_list_deals",
  {
    title: "List Deals",
    description: `List all deals/opportunities in your Apollo account.

Args:
  - page, perPage: Pagination

Returns:
  Paginated list of deals.`,
    inputSchema: ListDealsSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async (params: ListDealsInput) => {
    const response = await makeApiRequest<{
      opportunities: Array<Record<string, unknown>>;
      pagination: { page: number; per_page: number; total_entries: number; total_pages: number };
    }>("/opportunities", "GET", undefined, {
      page: params.page,
      per_page: params.perPage,
    });

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          count: response.data?.opportunities?.length || 0,
          deals: response.data?.opportunities,
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// UTILITY TOOLS
// ============================================================

server.registerTool(
  "apollo_get_api_usage",
  {
    title: "Get API Usage & Rate Limits",
    description: `View your Apollo API usage statistics and rate limits.

Returns:
  Current usage stats, rate limits, and remaining credits.`,
    inputSchema: GetApiUsageSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async () => {
    const response = await makeApiRequest<Record<string, unknown>>(
      "/auth/health",
      "POST",
      {}
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          usage: response.data,
          rateLimitInfo: response.rateLimitInfo,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_list_users",
  {
    title: "List Users",
    description: `Get all users in your Apollo team.

Returns:
  List of team members with IDs and roles.`,
    inputSchema: ListUsersSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async () => {
    const response = await makeApiRequest<{ users: Array<Record<string, unknown>> }>(
      "/users",
      "GET"
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          users: response.data?.users,
        }, null, 2),
      }],
    };
  }
);

server.registerTool(
  "apollo_list_email_accounts",
  {
    title: "List Email Accounts",
    description: `Get all connected email accounts for sending sequences.

Returns:
  List of email accounts with IDs for use in sequences.`,
    inputSchema: ListEmailAccountsSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async () => {
    const response = await makeApiRequest<{ email_accounts: Array<Record<string, unknown>> }>(
      "/email_accounts",
      "GET"
    );

    if (!response.success) {
      return {
        content: [{ type: "text", text: `Error: ${response.error}` }],
      };
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          success: true,
          emailAccounts: response.data?.email_accounts,
        }, null, 2),
      }],
    };
  }
);

// ============================================================
// SERVER STARTUP
// ============================================================

async function runStdio(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Apollo MCP server running on stdio");
}

async function runHTTP(): Promise<void> {
  const app = express();
  app.use(express.json());

  app.get("/health", (_req, res) => {
    res.json({ status: "ok", server: "apollo-mcp-server" });
  });

  app.post("/mcp", async (req, res) => {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
      enableJsonResponse: true,
    });
    res.on("close", () => transport.close());
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  });

  const port = parseInt(process.env.PORT || "3000", 10);
  app.listen(port, () => {
    console.error(`Apollo MCP server running on http://localhost:${port}/mcp`);
  });
}

// Choose transport based on environment
const transport = process.env.TRANSPORT || "stdio";
if (transport === "http") {
  runHTTP().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
  });
} else {
  runStdio().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
  });
}
