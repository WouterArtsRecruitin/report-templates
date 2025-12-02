/**
 * Apollo.io API Client Service
 * Handles authentication and HTTP requests to Apollo API
 */
const API_BASE_URL = "https://api.apollo.io/api/v1";
let config = null;
export function setConfig(newConfig) {
    config = newConfig;
}
export function getConfig() {
    return config;
}
export async function makeApiRequest(endpoint, method = "GET", body, queryParams) {
    if (!config?.apiKey) {
        return {
            success: false,
            error: "Apollo API key not configured. Use apollo_configure tool first.",
        };
    }
    try {
        // Build URL with query params
        let url = `${API_BASE_URL}${endpoint}`;
        if (queryParams) {
            const params = new URLSearchParams();
            Object.entries(queryParams).forEach(([key, value]) => {
                if (value !== undefined) {
                    params.append(key, String(value));
                }
            });
            const paramString = params.toString();
            if (paramString) {
                url += `?${paramString}`;
            }
        }
        const headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "x-api-key": config.apiKey,
        };
        const fetchOptions = {
            method,
            headers,
        };
        if (body && ["POST", "PUT", "PATCH"].includes(method)) {
            fetchOptions.body = JSON.stringify(body);
        }
        const response = await fetch(url, fetchOptions);
        // Extract rate limit info from headers
        const rateLimitInfo = {
            remaining: parseInt(response.headers.get("x-rate-limit-remaining") || "0", 10),
            limit: parseInt(response.headers.get("x-rate-limit-limit") || "0", 10),
            resetAt: response.headers.get("x-rate-limit-reset") || "",
        };
        if (!response.ok) {
            const errorText = await response.text();
            let errorMessage = `Apollo API error: ${response.status}`;
            try {
                const errorJson = JSON.parse(errorText);
                errorMessage = errorJson.error || errorJson.message || errorMessage;
            }
            catch {
                if (errorText) {
                    errorMessage = errorText;
                }
            }
            // Handle specific error codes
            if (response.status === 401) {
                errorMessage = "Invalid Apollo API key. Please check your credentials.";
            }
            else if (response.status === 403) {
                errorMessage = "Access denied. This endpoint may require a master API key or higher plan.";
            }
            else if (response.status === 429) {
                errorMessage = `Rate limit exceeded. Resets at: ${rateLimitInfo.resetAt}`;
            }
            return {
                success: false,
                error: errorMessage,
                rateLimitInfo,
            };
        }
        const data = await response.json();
        return {
            success: true,
            data,
            rateLimitInfo,
        };
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
        return {
            success: false,
            error: `Network error: ${errorMessage}`,
        };
    }
}
export function formatPaginatedResponse(data, itemKey) {
    const items = data[itemKey] || [];
    const pagination = data.pagination || {
        page: 1,
        per_page: items.length,
        total_entries: items.length,
        total_pages: 1,
    };
    return {
        items,
        pagination: {
            page: pagination.page,
            perPage: pagination.per_page,
            totalEntries: pagination.total_entries,
            totalPages: pagination.total_pages,
        },
    };
}
// Format helpers for consistent output
export function formatPerson(person) {
    return {
        id: person.id,
        firstName: person.first_name,
        lastName: person.last_name,
        name: person.name,
        email: person.email,
        emailStatus: person.email_status,
        title: person.title,
        headline: person.headline,
        linkedinUrl: person.linkedin_url,
        photoUrl: person.photo_url,
        phone: person.phone_number || person.sanitized_phone,
        city: person.city,
        state: person.state,
        country: person.country,
        organizationId: person.organization_id,
        organizationName: person.organization?.name,
        seniority: person.seniority,
        departments: person.departments,
    };
}
export function formatOrganization(org) {
    return {
        id: org.id,
        name: org.name,
        websiteUrl: org.website_url,
        linkedinUrl: org.linkedin_url,
        twitterUrl: org.twitter_url,
        phone: org.phone,
        industry: org.industry,
        keywords: org.keywords,
        estimatedNumEmployees: org.estimated_num_employees,
        foundedYear: org.founded_year,
        city: org.city,
        state: org.state,
        country: org.country,
        shortDescription: org.short_description,
        annualRevenue: org.annual_revenue,
        totalFunding: org.total_funding,
        latestFundingRoundDate: org.latest_funding_round_date,
        techologies: org.technologies,
    };
}
export function formatContact(contact) {
    return {
        id: contact.id,
        firstName: contact.first_name,
        lastName: contact.last_name,
        name: contact.name,
        email: contact.email,
        title: contact.title,
        phone: contact.phone_numbers,
        linkedinUrl: contact.linkedin_url,
        accountId: contact.account_id,
        ownerId: contact.owner_id,
        createdAt: contact.created_at,
        updatedAt: contact.updated_at,
        labels: contact.label_ids,
        customFields: contact.typed_custom_fields,
    };
}
export function formatAccount(account) {
    return {
        id: account.id,
        name: account.name,
        domain: account.domain,
        websiteUrl: account.website_url,
        phone: account.phone,
        industry: account.industry,
        ownerId: account.owner_id,
        createdAt: account.created_at,
        updatedAt: account.updated_at,
        labels: account.label_ids,
        customFields: account.typed_custom_fields,
    };
}
export function formatSequence(sequence) {
    return {
        id: sequence.id,
        name: sequence.name,
        createdAt: sequence.created_at,
        active: sequence.active,
        labelIds: sequence.label_ids,
        numSteps: sequence.num_steps,
        userId: sequence.user_id,
        uniqueScheduled: sequence.unique_scheduled,
        uniqueDelivered: sequence.unique_delivered,
        uniqueOpened: sequence.unique_opened,
        uniqueClicked: sequence.unique_clicked,
        uniqueReplied: sequence.unique_replied,
        uniqueBounced: sequence.unique_bounced,
    };
}
