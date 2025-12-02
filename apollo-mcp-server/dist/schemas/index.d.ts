import { z } from "zod";
export declare const VacancyAnalysisSchema: z.ZodObject<{
    vacancyText: z.ZodString;
    companyName: z.ZodOptional<z.ZodString>;
    jobTitle: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    vacancyText: string;
    companyName?: string | undefined;
    jobTitle?: string | undefined;
}, {
    vacancyText: string;
    companyName?: string | undefined;
    jobTitle?: string | undefined;
}>;
export declare const ConfigureSchema: z.ZodObject<{
    apiKey: z.ZodString;
    userId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    apiKey: string;
    userId?: string | undefined;
}, {
    apiKey: string;
    userId?: string | undefined;
}>;
export declare const PersonEnrichmentSchema: z.ZodEffects<z.ZodObject<{
    email: z.ZodOptional<z.ZodString>;
    firstName: z.ZodOptional<z.ZodString>;
    lastName: z.ZodOptional<z.ZodString>;
    name: z.ZodOptional<z.ZodString>;
    domain: z.ZodOptional<z.ZodString>;
    organizationName: z.ZodOptional<z.ZodString>;
    linkedinUrl: z.ZodOptional<z.ZodString>;
    revealPersonalEmails: z.ZodDefault<z.ZodBoolean>;
    revealPhoneNumber: z.ZodDefault<z.ZodBoolean>;
}, "strict", z.ZodTypeAny, {
    revealPersonalEmails: boolean;
    revealPhoneNumber: boolean;
    firstName?: string | undefined;
    lastName?: string | undefined;
    name?: string | undefined;
    email?: string | undefined;
    linkedinUrl?: string | undefined;
    organizationName?: string | undefined;
    domain?: string | undefined;
}, {
    firstName?: string | undefined;
    lastName?: string | undefined;
    name?: string | undefined;
    email?: string | undefined;
    linkedinUrl?: string | undefined;
    organizationName?: string | undefined;
    domain?: string | undefined;
    revealPersonalEmails?: boolean | undefined;
    revealPhoneNumber?: boolean | undefined;
}>, {
    revealPersonalEmails: boolean;
    revealPhoneNumber: boolean;
    firstName?: string | undefined;
    lastName?: string | undefined;
    name?: string | undefined;
    email?: string | undefined;
    linkedinUrl?: string | undefined;
    organizationName?: string | undefined;
    domain?: string | undefined;
}, {
    firstName?: string | undefined;
    lastName?: string | undefined;
    name?: string | undefined;
    email?: string | undefined;
    linkedinUrl?: string | undefined;
    organizationName?: string | undefined;
    domain?: string | undefined;
    revealPersonalEmails?: boolean | undefined;
    revealPhoneNumber?: boolean | undefined;
}>;
export declare const BulkPersonEnrichmentSchema: z.ZodObject<{
    people: z.ZodArray<z.ZodObject<{
        email: z.ZodOptional<z.ZodString>;
        firstName: z.ZodOptional<z.ZodString>;
        lastName: z.ZodOptional<z.ZodString>;
        domain: z.ZodOptional<z.ZodString>;
        linkedinUrl: z.ZodOptional<z.ZodString>;
    }, "strip", z.ZodTypeAny, {
        firstName?: string | undefined;
        lastName?: string | undefined;
        email?: string | undefined;
        linkedinUrl?: string | undefined;
        domain?: string | undefined;
    }, {
        firstName?: string | undefined;
        lastName?: string | undefined;
        email?: string | undefined;
        linkedinUrl?: string | undefined;
        domain?: string | undefined;
    }>, "many">;
    revealPersonalEmails: z.ZodDefault<z.ZodBoolean>;
    revealPhoneNumber: z.ZodDefault<z.ZodBoolean>;
}, "strict", z.ZodTypeAny, {
    people: {
        firstName?: string | undefined;
        lastName?: string | undefined;
        email?: string | undefined;
        linkedinUrl?: string | undefined;
        domain?: string | undefined;
    }[];
    revealPersonalEmails: boolean;
    revealPhoneNumber: boolean;
}, {
    people: {
        firstName?: string | undefined;
        lastName?: string | undefined;
        email?: string | undefined;
        linkedinUrl?: string | undefined;
        domain?: string | undefined;
    }[];
    revealPersonalEmails?: boolean | undefined;
    revealPhoneNumber?: boolean | undefined;
}>;
export declare const OrganizationEnrichmentSchema: z.ZodObject<{
    domain: z.ZodString;
}, "strict", z.ZodTypeAny, {
    domain: string;
}, {
    domain: string;
}>;
export declare const PeopleSearchSchema: z.ZodObject<{
    personTitles: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    personLocations: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    personSeniorities: z.ZodOptional<z.ZodArray<z.ZodEnum<["owner", "founder", "c_suite", "partner", "vp", "head", "director", "manager", "senior", "entry"]>, "many">>;
    qOrganizationDomains: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    organizationLocations: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    organizationNumEmployeesRanges: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    organizationIndustryTagIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    qKeywords: z.ZodOptional<z.ZodString>;
    page: z.ZodDefault<z.ZodNumber>;
    perPage: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    page: number;
    perPage: number;
    personTitles?: string[] | undefined;
    personLocations?: string[] | undefined;
    personSeniorities?: ("owner" | "founder" | "c_suite" | "partner" | "vp" | "head" | "director" | "manager" | "senior" | "entry")[] | undefined;
    qOrganizationDomains?: string[] | undefined;
    organizationLocations?: string[] | undefined;
    organizationNumEmployeesRanges?: string[] | undefined;
    organizationIndustryTagIds?: string[] | undefined;
    qKeywords?: string | undefined;
}, {
    page?: number | undefined;
    personTitles?: string[] | undefined;
    personLocations?: string[] | undefined;
    personSeniorities?: ("owner" | "founder" | "c_suite" | "partner" | "vp" | "head" | "director" | "manager" | "senior" | "entry")[] | undefined;
    qOrganizationDomains?: string[] | undefined;
    organizationLocations?: string[] | undefined;
    organizationNumEmployeesRanges?: string[] | undefined;
    organizationIndustryTagIds?: string[] | undefined;
    qKeywords?: string | undefined;
    perPage?: number | undefined;
}>;
export declare const OrganizationSearchSchema: z.ZodObject<{
    qOrganizationName: z.ZodOptional<z.ZodString>;
    organizationLocations: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    organizationNumEmployeesRanges: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    organizationIndustryTagIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    qKeywords: z.ZodOptional<z.ZodString>;
    page: z.ZodDefault<z.ZodNumber>;
    perPage: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    page: number;
    perPage: number;
    organizationLocations?: string[] | undefined;
    organizationNumEmployeesRanges?: string[] | undefined;
    organizationIndustryTagIds?: string[] | undefined;
    qKeywords?: string | undefined;
    qOrganizationName?: string | undefined;
}, {
    page?: number | undefined;
    organizationLocations?: string[] | undefined;
    organizationNumEmployeesRanges?: string[] | undefined;
    organizationIndustryTagIds?: string[] | undefined;
    qKeywords?: string | undefined;
    perPage?: number | undefined;
    qOrganizationName?: string | undefined;
}>;
export declare const CreateContactSchema: z.ZodObject<{
    firstName: z.ZodString;
    lastName: z.ZodString;
    email: z.ZodOptional<z.ZodString>;
    title: z.ZodOptional<z.ZodString>;
    organizationName: z.ZodOptional<z.ZodString>;
    websiteUrl: z.ZodOptional<z.ZodString>;
    accountId: z.ZodOptional<z.ZodString>;
    ownerId: z.ZodOptional<z.ZodString>;
    phone: z.ZodOptional<z.ZodString>;
    linkedinUrl: z.ZodOptional<z.ZodString>;
    labelIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
}, "strict", z.ZodTypeAny, {
    firstName: string;
    lastName: string;
    email?: string | undefined;
    title?: string | undefined;
    linkedinUrl?: string | undefined;
    phone?: string | undefined;
    organizationName?: string | undefined;
    websiteUrl?: string | undefined;
    accountId?: string | undefined;
    ownerId?: string | undefined;
    labelIds?: string[] | undefined;
}, {
    firstName: string;
    lastName: string;
    email?: string | undefined;
    title?: string | undefined;
    linkedinUrl?: string | undefined;
    phone?: string | undefined;
    organizationName?: string | undefined;
    websiteUrl?: string | undefined;
    accountId?: string | undefined;
    ownerId?: string | undefined;
    labelIds?: string[] | undefined;
}>;
export declare const UpdateContactSchema: z.ZodObject<{
    contactId: z.ZodString;
    firstName: z.ZodOptional<z.ZodString>;
    lastName: z.ZodOptional<z.ZodString>;
    email: z.ZodOptional<z.ZodString>;
    title: z.ZodOptional<z.ZodString>;
    phone: z.ZodOptional<z.ZodString>;
    accountId: z.ZodOptional<z.ZodString>;
    ownerId: z.ZodOptional<z.ZodString>;
    labelIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
}, "strict", z.ZodTypeAny, {
    contactId: string;
    firstName?: string | undefined;
    lastName?: string | undefined;
    email?: string | undefined;
    title?: string | undefined;
    phone?: string | undefined;
    accountId?: string | undefined;
    ownerId?: string | undefined;
    labelIds?: string[] | undefined;
}, {
    contactId: string;
    firstName?: string | undefined;
    lastName?: string | undefined;
    email?: string | undefined;
    title?: string | undefined;
    phone?: string | undefined;
    accountId?: string | undefined;
    ownerId?: string | undefined;
    labelIds?: string[] | undefined;
}>;
export declare const SearchContactsSchema: z.ZodObject<{
    qKeywords: z.ZodOptional<z.ZodString>;
    contactLabelIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    accountIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    ownerIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    page: z.ZodDefault<z.ZodNumber>;
    perPage: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    page: number;
    perPage: number;
    qKeywords?: string | undefined;
    contactLabelIds?: string[] | undefined;
    accountIds?: string[] | undefined;
    ownerIds?: string[] | undefined;
}, {
    page?: number | undefined;
    qKeywords?: string | undefined;
    perPage?: number | undefined;
    contactLabelIds?: string[] | undefined;
    accountIds?: string[] | undefined;
    ownerIds?: string[] | undefined;
}>;
export declare const CreateAccountSchema: z.ZodObject<{
    name: z.ZodString;
    domain: z.ZodOptional<z.ZodString>;
    phone: z.ZodOptional<z.ZodString>;
    ownerId: z.ZodOptional<z.ZodString>;
    labelIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
}, "strict", z.ZodTypeAny, {
    name: string;
    phone?: string | undefined;
    ownerId?: string | undefined;
    domain?: string | undefined;
    labelIds?: string[] | undefined;
}, {
    name: string;
    phone?: string | undefined;
    ownerId?: string | undefined;
    domain?: string | undefined;
    labelIds?: string[] | undefined;
}>;
export declare const UpdateAccountSchema: z.ZodObject<{
    accountId: z.ZodString;
    name: z.ZodOptional<z.ZodString>;
    domain: z.ZodOptional<z.ZodString>;
    phone: z.ZodOptional<z.ZodString>;
    ownerId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    accountId: string;
    name?: string | undefined;
    phone?: string | undefined;
    ownerId?: string | undefined;
    domain?: string | undefined;
}, {
    accountId: string;
    name?: string | undefined;
    phone?: string | undefined;
    ownerId?: string | undefined;
    domain?: string | undefined;
}>;
export declare const SearchAccountsSchema: z.ZodObject<{
    qKeywords: z.ZodOptional<z.ZodString>;
    accountLabelIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    ownerIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    page: z.ZodDefault<z.ZodNumber>;
    perPage: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    page: number;
    perPage: number;
    qKeywords?: string | undefined;
    ownerIds?: string[] | undefined;
    accountLabelIds?: string[] | undefined;
}, {
    page?: number | undefined;
    qKeywords?: string | undefined;
    perPage?: number | undefined;
    ownerIds?: string[] | undefined;
    accountLabelIds?: string[] | undefined;
}>;
export declare const SearchSequencesSchema: z.ZodObject<{
    qKeywords: z.ZodOptional<z.ZodString>;
    activeOnly: z.ZodDefault<z.ZodBoolean>;
    page: z.ZodDefault<z.ZodNumber>;
    perPage: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    page: number;
    perPage: number;
    activeOnly: boolean;
    qKeywords?: string | undefined;
}, {
    page?: number | undefined;
    qKeywords?: string | undefined;
    perPage?: number | undefined;
    activeOnly?: boolean | undefined;
}>;
export declare const AddContactsToSequenceSchema: z.ZodObject<{
    sequenceId: z.ZodString;
    contactIds: z.ZodArray<z.ZodString, "many">;
    emailAccountId: z.ZodString;
    userId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    sequenceId: string;
    contactIds: string[];
    emailAccountId: string;
    userId?: string | undefined;
}, {
    sequenceId: string;
    contactIds: string[];
    emailAccountId: string;
    userId?: string | undefined;
}>;
export declare const CreateTaskSchema: z.ZodObject<{
    userId: z.ZodString;
    type: z.ZodEnum<["call", "email", "linkedin", "action_item", "other"]>;
    priority: z.ZodDefault<z.ZodEnum<["high", "medium", "low"]>>;
    dueAt: z.ZodOptional<z.ZodString>;
    note: z.ZodOptional<z.ZodString>;
    contactId: z.ZodOptional<z.ZodString>;
    accountId: z.ZodOptional<z.ZodString>;
}, "strict", z.ZodTypeAny, {
    userId: string;
    type: "email" | "call" | "linkedin" | "action_item" | "other";
    priority: "high" | "medium" | "low";
    accountId?: string | undefined;
    contactId?: string | undefined;
    dueAt?: string | undefined;
    note?: string | undefined;
}, {
    userId: string;
    type: "email" | "call" | "linkedin" | "action_item" | "other";
    accountId?: string | undefined;
    contactId?: string | undefined;
    priority?: "high" | "medium" | "low" | undefined;
    dueAt?: string | undefined;
    note?: string | undefined;
}>;
export declare const SearchTasksSchema: z.ZodObject<{
    userIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    contactIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    accountIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    completed: z.ZodOptional<z.ZodBoolean>;
    page: z.ZodDefault<z.ZodNumber>;
    perPage: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    page: number;
    perPage: number;
    completed?: boolean | undefined;
    accountIds?: string[] | undefined;
    contactIds?: string[] | undefined;
    userIds?: string[] | undefined;
}, {
    page?: number | undefined;
    completed?: boolean | undefined;
    perPage?: number | undefined;
    accountIds?: string[] | undefined;
    contactIds?: string[] | undefined;
    userIds?: string[] | undefined;
}>;
export declare const CreateDealSchema: z.ZodObject<{
    name: z.ZodString;
    amount: z.ZodOptional<z.ZodNumber>;
    accountId: z.ZodOptional<z.ZodString>;
    contactIds: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    ownerId: z.ZodOptional<z.ZodString>;
    status: z.ZodDefault<z.ZodEnum<["open", "won", "lost"]>>;
}, "strict", z.ZodTypeAny, {
    name: string;
    status: "open" | "won" | "lost";
    accountId?: string | undefined;
    ownerId?: string | undefined;
    contactIds?: string[] | undefined;
    amount?: number | undefined;
}, {
    name: string;
    accountId?: string | undefined;
    ownerId?: string | undefined;
    status?: "open" | "won" | "lost" | undefined;
    contactIds?: string[] | undefined;
    amount?: number | undefined;
}>;
export declare const ListDealsSchema: z.ZodObject<{
    page: z.ZodDefault<z.ZodNumber>;
    perPage: z.ZodDefault<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    page: number;
    perPage: number;
}, {
    page?: number | undefined;
    perPage?: number | undefined;
}>;
export declare const GetApiUsageSchema: z.ZodObject<{}, "strict", z.ZodTypeAny, {}, {}>;
export declare const ListUsersSchema: z.ZodObject<{}, "strict", z.ZodTypeAny, {}, {}>;
export declare const ListEmailAccountsSchema: z.ZodObject<{}, "strict", z.ZodTypeAny, {}, {}>;
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
