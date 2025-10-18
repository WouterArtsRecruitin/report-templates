/**
 * Rate Limiting Middleware
 * Prevents abuse by limiting request frequency
 */

import { Request, Response, NextFunction } from 'express';

interface RateLimitStore {
  [key: string]: {
    count: number;
    resetTime: number;
  };
}

const store: RateLimitStore = {};

/**
 * Simple in-memory rate limiter
 * @param maxAttempts - Maximum number of attempts allowed
 * @param windowMinutes - Time window in minutes
 */
export const rateLimiter = (maxAttempts: number, windowMinutes: number) => {
  const windowMs = windowMinutes * 60 * 1000; // Convert to milliseconds
  
  return (req: Request, res: Response, next: NextFunction) => {
    const key = `${req.ip}:${req.route?.path || req.path}`;
    const now = Date.now();
    
    // Clean up expired entries periodically
    if (Math.random() < 0.1) { // 10% chance to clean up on each request
      Object.keys(store).forEach(storeKey => {
        if (store[storeKey].resetTime <= now) {
          delete store[storeKey];
        }
      });
    }
    
    // Get or create rate limit entry
    if (!store[key] || store[key].resetTime <= now) {
      store[key] = {
        count: 1,
        resetTime: now + windowMs
      };
      
      // Set rate limit headers
      res.set({
        'X-RateLimit-Limit': maxAttempts.toString(),
        'X-RateLimit-Remaining': (maxAttempts - 1).toString(),
        'X-RateLimit-Reset': new Date(store[key].resetTime).toISOString()
      });
      
      return next();
    }
    
    // Increment counter
    store[key].count++;
    
    // Set rate limit headers
    const remaining = Math.max(0, maxAttempts - store[key].count);
    res.set({
      'X-RateLimit-Limit': maxAttempts.toString(),
      'X-RateLimit-Remaining': remaining.toString(),
      'X-RateLimit-Reset': new Date(store[key].resetTime).toISOString()
    });
    
    // Check if limit exceeded
    if (store[key].count > maxAttempts) {
      const retryAfter = Math.ceil((store[key].resetTime - now) / 1000);
      
      console.warn(`[RateLimit] Rate limit exceeded for ${req.ip} on ${req.path}`);
      
      return res.status(429).json({
        error: 'Too many requests',
        message: `Rate limit exceeded. Try again in ${Math.ceil(retryAfter / 60)} minutes.`,
        retryAfter: retryAfter,
        limit: maxAttempts,
        window: windowMinutes
      });
    }
    
    next();
  };
};