/**
 * Request Validation Middleware
 * Validates incoming requests using Zod schemas
 */

import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

export const validateRequest = (schema: z.ZodSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    try {
      // Validate request body
      const validatedData = schema.parse(req.body);
      req.body = validatedData;
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errors = error.issues.map((err: z.ZodIssue) => ({
          field: err.path.join('.'),
          message: err.message,
          code: err.code
        }));
        
        console.warn('[Validation] Request validation failed:', errors);
        
        res.status(400).json({
          error: 'Validation failed',
          message: 'The request data is invalid.',
          details: errors
        });
        return;
      }
      
      console.error('[Validation] Unexpected validation error:', error);
      
      res.status(500).json({
        error: 'Validation error',
        message: 'An internal error occurred during validation.'
      });
    }
  };
};