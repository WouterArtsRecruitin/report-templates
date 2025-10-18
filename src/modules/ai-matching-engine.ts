/**
 * AI Matching Engine Module
 * Handles AI-powered candidate matching and scoring
 */

export interface Candidate {
  id: string;
  name: string;
  skills: string[];
  experience: number;
  education: string;
  location: string;
}

export interface JobRequirement {
  id: string;
  title: string;
  requiredSkills: string[];
  preferredSkills: string[];
  minExperience: number;
  educationLevel: string;
  location: string;
}

export interface MatchResult {
  candidateId: string;
  jobId: string;
  score: number;
  matchDetails: {
    skillMatch: number;
    experienceMatch: number;
    educationMatch: number;
    locationMatch: number;
  };
  recommendations: string[];
}

export class AIMatchingEngine {
  private modelVersion: string = '1.0.0';
  private threshold: number = 0.7;

  constructor() {
    console.log('[AIMatchingEngine] Initialized with model version:', this.modelVersion);
  }

  async matchCandidateToJob(candidate: Candidate, job: JobRequirement): Promise<MatchResult> {
    console.log(`[AIMatchingEngine] Matching candidate ${candidate.id} to job ${job.id}...`);
    
    // Calculate individual match scores
    const skillMatch = this.calculateSkillMatch(candidate.skills, job.requiredSkills, job.preferredSkills);
    const experienceMatch = this.calculateExperienceMatch(candidate.experience, job.minExperience);
    const educationMatch = this.calculateEducationMatch(candidate.education, job.educationLevel);
    const locationMatch = this.calculateLocationMatch(candidate.location, job.location);
    
    // Calculate overall score (weighted average)
    const overallScore = (
      skillMatch * 0.4 +
      experienceMatch * 0.3 +
      educationMatch * 0.2 +
      locationMatch * 0.1
    );
    
    const recommendations = this.generateRecommendations(candidate, job, overallScore);
    
    const result: MatchResult = {
      candidateId: candidate.id,
      jobId: job.id,
      score: Math.round(overallScore * 100) / 100,
      matchDetails: {
        skillMatch,
        experienceMatch,
        educationMatch,
        locationMatch
      },
      recommendations
    };
    
    console.log('[AIMatchingEngine] Match result:', result);
    return result;
  }

  async batchMatch(candidates: Candidate[], job: JobRequirement): Promise<MatchResult[]> {
    console.log(`[AIMatchingEngine] Batch matching ${candidates.length} candidates to job ${job.id}...`);
    
    const results = await Promise.all(
      candidates.map(candidate => this.matchCandidateToJob(candidate, job))
    );
    
    // Sort by score (highest first)
    return results.sort((a, b) => b.score - a.score);
  }

  private calculateSkillMatch(candidateSkills: string[], requiredSkills: string[], preferredSkills: string[]): number {
    console.log('[AIMatchingEngine] Calculating skill match...');
    
    // Placeholder logic - in real implementation, this would use NLP/AI
    const requiredMatches = requiredSkills.filter(skill => 
      candidateSkills.some(cs => cs.toLowerCase().includes(skill.toLowerCase()))
    ).length;
    
    const preferredMatches = preferredSkills.filter(skill => 
      candidateSkills.some(cs => cs.toLowerCase().includes(skill.toLowerCase()))
    ).length;
    
    const requiredScore = requiredSkills.length > 0 ? requiredMatches / requiredSkills.length : 1;
    const preferredScore = preferredSkills.length > 0 ? preferredMatches / preferredSkills.length : 1;
    
    return requiredScore * 0.8 + preferredScore * 0.2;
  }

  private calculateExperienceMatch(candidateExp: number, minExp: number): number {
    console.log('[AIMatchingEngine] Calculating experience match...');
    
    if (candidateExp >= minExp) {
      // Extra points for more experience, capped at 1
      return Math.min(1, 0.8 + (candidateExp - minExp) * 0.05);
    }
    
    // Penalty for less experience
    return Math.max(0, candidateExp / minExp);
  }

  private calculateEducationMatch(candidateEdu: string, requiredEdu: string): number {
    console.log('[AIMatchingEngine] Calculating education match...');
    
    // Placeholder logic
    const educationLevels = ['high school', 'bachelor', 'master', 'phd'];
    const candidateLevel = educationLevels.indexOf(candidateEdu.toLowerCase());
    const requiredLevel = educationLevels.indexOf(requiredEdu.toLowerCase());
    
    if (candidateLevel >= requiredLevel) {
      return 1;
    }
    
    return Math.max(0, 1 - (requiredLevel - candidateLevel) * 0.3);
  }

  private calculateLocationMatch(candidateLoc: string, jobLoc: string): number {
    console.log('[AIMatchingEngine] Calculating location match...');
    
    // Placeholder logic - in real implementation, this would use geolocation
    if (candidateLoc.toLowerCase() === jobLoc.toLowerCase()) {
      return 1;
    }
    
    // Assume same country gives partial match
    return 0.5;
  }

  private generateRecommendations(candidate: Candidate, job: JobRequirement, score: number): string[] {
    const recommendations: string[] = [];
    
    if (score >= this.threshold) {
      recommendations.push('Strong match - proceed with interview');
    } else if (score >= 0.5) {
      recommendations.push('Moderate match - consider for preliminary screening');
    } else {
      recommendations.push('Weak match - may not meet minimum requirements');
    }
    
    // Add specific recommendations based on missing skills
    const missingSkills = job.requiredSkills.filter(skill => 
      !candidate.skills.some(cs => cs.toLowerCase().includes(skill.toLowerCase()))
    );
    
    if (missingSkills.length > 0) {
      recommendations.push(`Consider training in: ${missingSkills.join(', ')}`);
    }
    
    return recommendations;
  }

  setThreshold(threshold: number): void {
    console.log(`[AIMatchingEngine] Setting threshold to ${threshold}`);
    this.threshold = Math.max(0, Math.min(1, threshold));
  }

  getThreshold(): number {
    return this.threshold;
  }
}

// Default export
export default AIMatchingEngine;