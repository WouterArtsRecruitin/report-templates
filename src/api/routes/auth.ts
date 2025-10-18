/**
 * Authentication Routes
 * Handles user login, logout, token refresh, and registration
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { SecurityManager, UserRole } from '../../modules/security-manager';
import { validateRequest } from '../middleware/validation';
import { rateLimiter } from '../middleware/rateLimiter';

const router = Router();
const securityManager = new SecurityManager({
  tokenExpiration: 60, // 1 hour
  maxLoginAttempts: 5,
  passwordMinLength: 8,
  requireMFA: false,
  sessionTimeout: 30
});

// Validation schemas
const loginSchema = z.object({
  email: z.string()
    .email('Invalid email format')
    .min(1, 'Email is required'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password too long')
});

const registerSchema = z.object({
  email: z.string()
    .email('Invalid email format')
    .min(1, 'Email is required'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password too long')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain uppercase, lowercase, and number'),
  role: z.nativeEnum(UserRole).optional().default(UserRole.VIEWER)
});

const refreshTokenSchema = z.object({
  refreshToken: z.string().min(1, 'Refresh token is required')
});

/**
 * POST /api/auth/login
 * Authenticate user and return access token
 */
router.post('/login', 
  rateLimiter(process.env.NODE_ENV === 'test' ? 100 : 5, 15), // Higher limit for tests
  validateRequest(loginSchema), 
  async (req: Request, res: Response): Promise<void> => {
    try {
      const { email, password } = req.body;
      
      console.log(`[Auth] Login attempt for: ${email}`);
      
      // Authenticate user
      const authToken = await securityManager.authenticate(email, password);
      
      if (!authToken) {
        console.warn(`[Auth] Failed login attempt for: ${email}`);
        res.status(401).json({ 
          error: 'Invalid credentials',
          message: 'The email or password you entered is incorrect.'
        });
        return;
      }
      
      console.log(`[Auth] Successful login for: ${email}`);
      
      // Return tokens (exclude sensitive data)
      res.json({
        success: true,
        data: {
          token: authToken.token,
          refreshToken: authToken.refreshToken,
          expiresAt: authToken.expiresAt,
          tokenType: 'Bearer'
        },
        message: 'Login successful'
      });
      
    } catch (error: any) {
      console.error('[Auth] Login error:', error.message);
      
      if (error.message.includes('Account locked')) {
        res.status(423).json({
          error: 'Account locked',
          message: 'Too many failed login attempts. Please try again later.',
          retryAfter: 900 // 15 minutes
        });
        return;
      }
      
      res.status(500).json({
        error: 'Authentication failed',
        message: 'An internal error occurred during login.'
      });
    }
  }
);

/**
 * POST /api/auth/register
 * Register new user account
 */
router.post('/register',
  rateLimiter(3, 60), // 3 registrations per hour
  validateRequest(registerSchema),
  async (req: Request, res: Response): Promise<void> => {
    try {
      const { email, password, role } = req.body;
      
      console.log(`[Auth] Registration attempt for: ${email}`);
      
      // Create new user
      const user = await securityManager.createUser({
        email,
        role: role || UserRole.VIEWER,
        permissions: [],
        isActive: true
      });
      
      console.log(`[Auth] User registered successfully: ${user.id}`);
      
      // Auto-login after registration
      const authToken = await securityManager.authenticate(email, password);
      
      res.status(201).json({
        success: true,
        data: {
          user: {
            id: user.id,
            email: user.email,
            role: user.role,
            isActive: user.isActive
          },
          token: authToken?.token,
          refreshToken: authToken?.refreshToken,
          expiresAt: authToken?.expiresAt,
          tokenType: 'Bearer'
        },
        message: 'Registration successful'
      });
      
    } catch (error: any) {
      console.error('[Auth] Registration error:', error.message);
      
      if (error.message.includes('already exists')) {
        res.status(409).json({
          error: 'User already exists',
          message: 'An account with this email already exists.'
        });
        return;
      }
      
      res.status(500).json({
        error: 'Registration failed',
        message: 'An internal error occurred during registration.'
      });
    }
  }
);

/**
 * POST /api/auth/refresh
 * Refresh access token using refresh token
 */
router.post('/refresh',
  rateLimiter(10, 60), // 10 refreshes per hour
  validateRequest(refreshTokenSchema),
  async (req: Request, res: Response): Promise<void> => {
    try {
      const { refreshToken } = req.body;
      
      console.log('[Auth] Token refresh attempt');
      
      const newAuthToken = await securityManager.refreshToken(refreshToken);
      
      if (!newAuthToken) {
        console.warn('[Auth] Invalid refresh token provided');
        res.status(401).json({
          error: 'Invalid refresh token',
          message: 'Please log in again.'
        });
        return;
      }
      
      console.log('[Auth] Token refreshed successfully');
      
      res.json({
        success: true,
        data: {
          token: newAuthToken.token,
          refreshToken: newAuthToken.refreshToken,
          expiresAt: newAuthToken.expiresAt,
          tokenType: 'Bearer'
        },
        message: 'Token refreshed successfully'
      });
      
    } catch (error: any) {
      console.error('[Auth] Token refresh error:', error.message);
      
      res.status(500).json({
        error: 'Token refresh failed',
        message: 'An internal error occurred during token refresh.'
      });
    }
  }
);

/**
 * POST /api/auth/logout
 * Logout user and revoke session
 */
router.post('/logout', async (req: Request, res: Response): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      await securityManager.revokeSession(token);
      console.log('[Auth] User logged out successfully');
    }
    
    res.json({
      success: true,
      message: 'Logout successful'
    });
    
  } catch (error: any) {
    console.error('[Auth] Logout error:', error.message);
    
    // Even if there's an error, we should return success for logout
    res.json({
      success: true,
      message: 'Logout completed'
    });
  }
});

/**
 * GET /api/auth/validate
 * Validate current token
 */
router.get('/validate', async (req: Request, res: Response): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({
        valid: false,
        error: 'No token provided'
      });
      return;
    }
    
    const token = authHeader.substring(7);
    const isValid = await securityManager.validateToken(token);
    
    if (!isValid) {
      res.status(401).json({
        valid: false,
        error: 'Invalid or expired token'
      });
      return;
    }
    
    res.json({
      valid: true,
      message: 'Token is valid'
    });
    
  } catch (error: any) {
    console.error('[Auth] Token validation error:', error.message);
    
    res.status(500).json({
      valid: false,
      error: 'Token validation failed'
    });
  }
});

/**
 * GET /api/auth/me
 * Get current user information
 */
router.get('/me', async (req: Request, res: Response): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({
        error: 'Authentication required'
      });
      return;
    }
    
    const token = authHeader.substring(7);
    const isValid = await securityManager.validateToken(token);
    
    if (!isValid) {
      res.status(401).json({
        error: 'Invalid or expired token'
      });
      return;
    }
    
    // In a real implementation, you'd fetch user data from database
    // For now, return mock user data
    res.json({
      success: true,
      data: {
        id: 'current_user_id',
        email: 'user@example.com',
        role: UserRole.RECRUITER,
        permissions: ['VIEW_CANDIDATES', 'EDIT_CANDIDATES'],
        isActive: true,
        lastLogin: new Date()
      }
    });
    
  } catch (error: any) {
    console.error('[Auth] User info error:', error.message);
    
    res.status(500).json({
      error: 'Failed to fetch user information'
    });
  }
});

export { router as authRouter };