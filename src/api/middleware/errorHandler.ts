/**
 * Global Error Handler Middleware
 * Handles and formats errors consistently
 */

import { Request, Response, NextFunction } from 'express';

export interface APIError extends Error {
  status?: number;
  code?: string;
  details?: any;
}

export const errorHandler = (
  error: APIError, 
  req: Request, 
  res: Response, 
  next: NextFunction
) => {
  // Log error details
  console.error('[ErrorHandler] API Error:', {
    message: error.message,
    status: error.status,
    code: error.code,
    stack: error.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    timestamp: new Date().toISOString()
  });

  // Don't handle if response already sent
  if (res.headersSent) {
    return next(error);
  }

  // Default error response
  let status = error.status || 500;
  let message = 'Internal server error';
  let code = error.code || 'INTERNAL_ERROR';

  // Handle specific error types
  if (error.name === 'ValidationError') {
    status = 400;
    message = 'Invalid request data';
    code = 'VALIDATION_ERROR';
  } else if (error.name === 'UnauthorizedError') {
    status = 401;
    message = 'Authentication required';
    code = 'UNAUTHORIZED';
  } else if (error.name === 'ForbiddenError') {
    status = 403;
    message = 'Access denied';
    code = 'FORBIDDEN';
  } else if (error.name === 'NotFoundError') {
    status = 404;
    message = 'Resource not found';
    code = 'NOT_FOUND';
  } else if (error.name === 'ConflictError') {
    status = 409;
    message = 'Resource conflict';
    code = 'CONFLICT';
  } else if (error.name === 'RateLimitError') {
    status = 429;
    message = 'Too many requests';
    code = 'RATE_LIMIT_EXCEEDED';
  }

  // In development, include error details
  const isDevelopment = process.env.NODE_ENV === 'development';
  
  const errorResponse: any = {
    error: code,
    message: message,
    timestamp: new Date().toISOString(),
    path: req.path,
    method: req.method
  };

  // Add debug info in development
  if (isDevelopment) {
    errorResponse.debug = {
      stack: error.stack,
      details: error.details
    };
  }

  // Add correlation ID if available
  if (req.headers['x-correlation-id']) {
    errorResponse.correlationId = req.headers['x-correlation-id'];
  }

  res.status(status).json(errorResponse);
};