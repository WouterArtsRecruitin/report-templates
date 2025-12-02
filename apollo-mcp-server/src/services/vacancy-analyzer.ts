/**
 * Vacancy Analysis Service
 * Bridge to Python vacancy analysis module
 */

import { spawn } from "child_process";
import path from "path";

export interface VacancyAnalysisResult {
  success: boolean;
  fullAnalysis: string;
  score: number | null;
  tokens: number;
  error?: string;
}

export async function analyzeVacancy(
  vacancyText: string,
  companyName?: string,
  jobTitle?: string
): Promise<VacancyAnalysisResult> {
  return new Promise((resolve, reject) => {
    const pythonPath = process.env.PYTHON_PATH || path.join(process.cwd(), "venv", "bin", "python");
    const scriptPath = path.join(process.cwd(), "vacancy_analysis_module.py");
    
    // Create input JSON for Python script
    const input = JSON.stringify({
      vacancy_text: vacancyText,
      company_name: companyName,
      job_title: jobTitle,
    });

    // Spawn Python process
    const pythonProcess = spawn(pythonPath, ["-c", `
import sys
import json
sys.path.append('${process.cwd()}')
from vacancy_analysis_module import analyze_vacancy_with_claude

try:
    input_data = json.loads('${input.replace(/'/g, "\\'")}')
    result = analyze_vacancy_with_claude(
        input_data['vacancy_text'],
        input_data.get('company_name'),
        input_data.get('job_title')
    )
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e)}))
    `]);

    let stdout = "";
    let stderr = "";

    pythonProcess.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    pythonProcess.on("close", (code) => {
      if (code !== 0) {
        resolve({
          success: false,
          fullAnalysis: "",
          score: null,
          tokens: 0,
          error: `Python process failed: ${stderr || "Unknown error"}`,
        });
        return;
      }

      try {
        const result = JSON.parse(stdout.trim());
        
        if (result.error) {
          resolve({
            success: false,
            fullAnalysis: "",
            score: null,
            tokens: 0,
            error: result.error,
          });
          return;
        }

        resolve({
          success: true,
          fullAnalysis: result.full_analysis || "",
          score: result.score || null,
          tokens: result.tokens || 0,
        });
      } catch (parseError) {
        resolve({
          success: false,
          fullAnalysis: "",
          score: null,
          tokens: 0,
          error: `Failed to parse Python output: ${parseError}`,
        });
      }
    });

    pythonProcess.on("error", (error) => {
      resolve({
        success: false,
        fullAnalysis: "",
        score: null,
        tokens: 0,
        error: `Failed to start Python process: ${error.message}`,
      });
    });

    // Set timeout to prevent hanging
    setTimeout(() => {
      pythonProcess.kill();
      resolve({
        success: false,
        fullAnalysis: "",
        score: null,
        tokens: 0,
        error: "Analysis timeout after 30 seconds",
      });
    }, 30000);
  });
}

export function formatAnalysisForPipedrive(result: VacancyAnalysisResult) {
  return {
    score: result.score || 0,
    analysis_summary: result.fullAnalysis.split('\n').slice(0, 3).join(' '), // First few lines
    tokens_used: result.tokens,
    analysis_status: result.success ? 'completed' : 'failed',
    error_message: result.error || null,
  };
}