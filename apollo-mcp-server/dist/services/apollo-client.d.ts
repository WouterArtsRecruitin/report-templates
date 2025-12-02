/**
 * Apollo.io API Client Service
 * Handles authentication and HTTP requests to Apollo API
 */
export interface ApolloConfig {
    apiKey: string;
    userId?: string;
}
export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
    rateLimitInfo?: {
        remaining: number;
        limit: number;
        resetAt: string;
    };
}
export declare function setConfig(newConfig: ApolloConfig): void;
export declare function getConfig(): ApolloConfig | null;
export declare function makeApiRequest<T>(endpoint: string, method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE", body?: Record<string, unknown>, queryParams?: Record<string, string | number | boolean | undefined>): Promise<ApiResponse<T>>;
export interface PaginatedResponse<T> {
    items: T[];
    pagination: {
        page: number;
        perPage: number;
        totalEntries: number;
        totalPages: number;
    };
}
export declare function formatPaginatedResponse<T>(data: {
    contacts?: T[];
    accounts?: T[];
    people?: T[];
    organizations?: T[];
    emailer_campaigns?: T[];
    tasks?: T[];
    opportunities?: T[];
    pagination?: {
        page: number;
        per_page: number;
        total_entries: number;
        total_pages: number;
    };
}, itemKey: string): PaginatedResponse<T>;
export declare function formatPerson(person: Record<string, unknown>): Record<string, unknown>;
export declare function formatOrganization(org: Record<string, unknown>): Record<string, unknown>;
export declare function formatContact(contact: Record<string, unknown>): Record<string, unknown>;
export declare function formatAccount(account: Record<string, unknown>): Record<string, unknown>;
export declare function formatSequence(sequence: Record<string, unknown>): Record<string, unknown>;
