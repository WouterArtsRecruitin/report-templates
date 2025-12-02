/**
 * Vacancy Analysis Service
 * Bridge to Python vacancy analysis module
 */
export interface VacancyAnalysisResult {
    success: boolean;
    fullAnalysis: string;
    score: number | null;
    tokens: number;
    error?: string;
}
export declare function analyzeVacancy(vacancyText: string, companyName?: string, jobTitle?: string): Promise<VacancyAnalysisResult>;
export declare function formatAnalysisForPipedrive(result: VacancyAnalysisResult): {
    score: number;
    analysis_summary: string;
    tokens_used: number;
    analysis_status: string;
    error_message: string | null;
};
