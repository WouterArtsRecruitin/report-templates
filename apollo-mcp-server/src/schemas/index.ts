import { z } from "zod";

// Vacancy Analysis Schema
export const VacancyAnalysisSchema = z.object({
  vacancyText: z.string().describe("The job vacancy text to analyze"),
  companyName: z.string().optional().describe("Optional company name"),
  jobTitle: z.string().optional().describe("Optional job title"),
});

// ============ Configuration ============
export const ConfigureSchema = z.object({
  apiKey: z.string().min(10).describe("Apollo API key (starts with ODnd_ or similar)"),
  userId: z.string().optional().describe("Apollo User ID (optional)"),
}).strict();

// ============ Enrichment Schemas ============
export const PersonEnrichmentSchema = z.object({
  email: z.string().email().optional().describe("Email address to enrich"),
  firstName: z.string().optional().describe("First name"),
  lastName: z.string().optional().describe("Last name"),
  name: z.string().optional().describe("Full name"),
  domain: z.string().optional().describe("Company domain (e.g., apollo.io)"),
  organizationName: z.string().optional().describe("Company name"),
  linkedinUrl: z.string().url().optional().describe("LinkedIn profile URL"),
  revealPersonalEmails: z.boolean().default(false).describe("Reveal personal email addresses (uses credits)"),
  revealPhoneNumber: z.boolean().default(false).describe("Reveal phone numbers (uses credits)"),
}).strict().refine(
  data => data.email || data.linkedinUrl || (data.firstName && data.lastName && data.domain),
  { message: "Provide email, LinkedIn URL, or name+domain combination" }
);

export const BulkPersonEnrichmentSchema = z.object({
  people: z.array(z.object({
    email: z.string().email().optional(),
    firstName: z.string().optional(),
    lastName: z.string().optional(),
    domain: z.string().optional(),
    linkedinUrl: z.string().url().optional(),
  })).min(1).max(10).describe("Array of people to enrich (max 10)"),
  revealPersonalEmails: z.boolean().default(false).describe("Reveal personal emails"),
  revealPhoneNumber: z.boolean().default(false).describe("Reveal phone numbers"),
}).strict();

export const OrganizationEnrichmentSchema = z.object({
  domain: z.string().describe("Company domain (e.g., apollo.io)"),
}).strict();

// ============ People Search Schema ============
export const PeopleSearchSchema = z.object({
  personTitles: z.array(z.string()).optional().describe("Job titles to search (e.g., ['CEO', 'CTO'])"),
  personLocations: z.array(z.string()).optional().describe("Locations (e.g., ['Netherlands', 'Germany'])"),
  personSeniorities: z.array(z.enum([
    "owner", "founder", "c_suite", "partner", "vp", 
    "head", "director", "manager", "senior", "entry"
  ])).optional().describe("Seniority levels"),
  qOrganizationDomains: z.array(z.string()).optional().describe("Company domains to search within"),
  organizationLocations: z.array(z.string()).optional().describe("Company locations"),
  organizationNumEmployeesRanges: z.array(z.string()).optional().describe("Employee ranges (e.g., ['50,200', '200,500'])"),
  organizationIndustryTagIds: z.array(z.string()).optional().describe("Industry tag IDs"),
  qKeywords: z.string().optional().describe("Keyword search"),
  page: z.number().int().min(1).default(1).describe("Page number"),
  perPage: z.number().int().min(1).max(100).default(25).describe("Results per page"),
}).strict();

// ============ Organization Search Schema ============
export const OrganizationSearchSchema = z.object({
  qOrganizationName: z.string().optional().describe("Company name to search"),
  organizationLocations: z.array(z.string()).optional().describe("Company locations"),
  organizationNumEmployeesRanges: z.array(z.string()).optional().describe("Employee ranges"),
  organizationIndustryTagIds: z.array(z.string()).optional().describe("Industry tag IDs"),
  qKeywords: z.string().optional().describe("Keyword search"),
  page: z.number().int().min(1).default(1).describe("Page number"),
  perPage: z.number().int().min(1).max(100).default(25).describe("Results per page"),
}).strict();

// ============ Contact Schemas ============
export const CreateContactSchema = z.object({
  firstName: z.string().describe("First name"),
  lastName: z.string().describe("Last name"),
  email: z.string().email().optional().describe("Email address"),
  title: z.string().optional().describe("Job title"),
  organizationName: z.string().optional().describe("Company name"),
  websiteUrl: z.string().url().optional().describe("Company website"),
  accountId: z.string().optional().describe("Apollo account ID to link"),
  ownerId: z.string().optional().describe("Owner user ID"),
  phone: z.string().optional().describe("Phone number"),
  linkedinUrl: z.string().url().optional().describe("LinkedIn URL"),
  labelIds: z.array(z.string()).optional().describe("Label IDs to apply"),
}).strict();

export const UpdateContactSchema = z.object({
  contactId: z.string().describe("Contact ID to update"),
  firstName: z.string().optional().describe("First name"),
  lastName: z.string().optional().describe("Last name"),
  email: z.string().email().optional().describe("Email address"),
  title: z.string().optional().describe("Job title"),
  phone: z.string().optional().describe("Phone number"),
  accountId: z.string().optional().describe("Account ID to link"),
  ownerId: z.string().optional().describe("Owner user ID"),
  labelIds: z.array(z.string()).optional().describe("Label IDs"),
}).strict();

export const SearchContactsSchema = z.object({
  qKeywords: z.string().optional().describe("Keyword search"),
  contactLabelIds: z.array(z.string()).optional().describe("Filter by label IDs"),
  accountIds: z.array(z.string()).optional().describe("Filter by account IDs"),
  ownerIds: z.array(z.string()).optional().describe("Filter by owner user IDs"),
  page: z.number().int().min(1).default(1).describe("Page number"),
  perPage: z.number().int().min(1).max(100).default(25).describe("Results per page"),
}).strict();

// ============ Account Schemas ============
export const CreateAccountSchema = z.object({
  name: z.string().describe("Company name"),
  domain: z.string().optional().describe("Company domain"),
  phone: z.string().optional().describe("Phone number"),
  ownerId: z.string().optional().describe("Owner user ID"),
  labelIds: z.array(z.string()).optional().describe("Label IDs"),
}).strict();

export const UpdateAccountSchema = z.object({
  accountId: z.string().describe("Account ID to update"),
  name: z.string().optional().describe("Company name"),
  domain: z.string().optional().describe("Company domain"),
  phone: z.string().optional().describe("Phone number"),
  ownerId: z.string().optional().describe("Owner user ID"),
}).strict();

export const SearchAccountsSchema = z.object({
  qKeywords: z.string().optional().describe("Keyword search"),
  accountLabelIds: z.array(z.string()).optional().describe("Filter by label IDs"),
  ownerIds: z.array(z.string()).optional().describe("Filter by owner IDs"),
  page: z.number().int().min(1).default(1).describe("Page number"),
  perPage: z.number().int().min(1).max(100).default(25).describe("Results per page"),
}).strict();

// ============ Sequence Schemas ============
export const SearchSequencesSchema = z.object({
  qKeywords: z.string().optional().describe("Search by name"),
  activeOnly: z.boolean().default(false).describe("Only return active sequences"),
  page: z.number().int().min(1).default(1).describe("Page number"),
  perPage: z.number().int().min(1).max(100).default(25).describe("Results per page"),
}).strict();

export const AddContactsToSequenceSchema = z.object({
  sequenceId: z.string().describe("Sequence ID"),
  contactIds: z.array(z.string()).min(1).describe("Contact IDs to add"),
  emailAccountId: z.string().describe("Email account ID to send from"),
  userId: z.string().optional().describe("User ID (defaults to API key owner)"),
}).strict();

// ============ Task Schemas ============
export const CreateTaskSchema = z.object({
  userId: z.string().describe("Assignee user ID"),
  type: z.enum(["call", "email", "linkedin", "action_item", "other"]).describe("Task type"),
  priority: z.enum(["high", "medium", "low"]).default("medium").describe("Priority"),
  dueAt: z.string().optional().describe("Due date (ISO format)"),
  note: z.string().optional().describe("Task notes"),
  contactId: z.string().optional().describe("Related contact ID"),
  accountId: z.string().optional().describe("Related account ID"),
}).strict();

export const SearchTasksSchema = z.object({
  userIds: z.array(z.string()).optional().describe("Filter by assignee IDs"),
  contactIds: z.array(z.string()).optional().describe("Filter by contact IDs"),
  accountIds: z.array(z.string()).optional().describe("Filter by account IDs"),
  completed: z.boolean().optional().describe("Filter by completion status"),
  page: z.number().int().min(1).default(1).describe("Page number"),
  perPage: z.number().int().min(1).max(100).default(25).describe("Results per page"),
}).strict();

// ============ Deal Schemas ============
export const CreateDealSchema = z.object({
  name: z.string().describe("Deal name"),
  amount: z.number().optional().describe("Deal value"),
  accountId: z.string().optional().describe("Related account ID"),
  contactIds: z.array(z.string()).optional().describe("Related contact IDs"),
  ownerId: z.string().optional().describe("Deal owner user ID"),
  status: z.enum(["open", "won", "lost"]).default("open").describe("Deal status"),
}).strict();

export const ListDealsSchema = z.object({
  page: z.number().int().min(1).default(1).describe("Page number"),
  perPage: z.number().int().min(1).max(100).default(25).describe("Results per page"),
}).strict();

// ============ Utility Schemas ============
export const GetApiUsageSchema = z.object({}).strict();

export const ListUsersSchema = z.object({}).strict();

export const ListEmailAccountsSchema = z.object({}).strict();

// Type exports
export type VacancyAnalysisInput = z.infer<typeof VacancyAnalysisSchema>;
export type ConfigureInput = z.infer<typeof ConfigureSchema>;
export type PersonEnrichmentInput = z.infer<typeof PersonEnrichmentSchema>;
export type BulkPersonEnrichmentInput = z.infer<typeof BulkPersonEnrichmentSchema>;
export type OrganizationEnrichmentInput = z.infer<typeof OrganizationEnrichmentSchema>;
export type PeopleSearchInput = z.infer<typeof PeopleSearchSchema>;
export type OrganizationSearchInput = z.infer<typeof OrganizationSearchSchema>;
export type CreateContactInput = z.infer<typeof CreateContactSchema>;
export type UpdateContactInput = z.infer<typeof UpdateContactSchema>;
export type SearchContactsInput = z.infer<typeof SearchContactsSchema>;
export type CreateAccountInput = z.infer<typeof CreateAccountSchema>;
export type UpdateAccountInput = z.infer<typeof UpdateAccountSchema>;
export type SearchAccountsInput = z.infer<typeof SearchAccountsSchema>;
export type SearchSequencesInput = z.infer<typeof SearchSequencesSchema>;
export type AddContactsToSequenceInput = z.infer<typeof AddContactsToSequenceSchema>;
export type CreateTaskInput = z.infer<typeof CreateTaskSchema>;
export type SearchTasksInput = z.infer<typeof SearchTasksSchema>;
export type CreateDealInput = z.infer<typeof CreateDealSchema>;
export type ListDealsInput = z.infer<typeof ListDealsSchema>;
