/**
 * Logging Service Module
 * Handles application logging, monitoring, and debugging
 */

export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
  FATAL = 'FATAL'
}

export interface LogEntry {
  id: string;
  timestamp: Date;
  level: LogLevel;
  message: string;
  context?: string;
  userId?: string;
  metadata?: Record<string, any>;
  stackTrace?: string;
}

export interface LoggerConfig {
  minLevel: LogLevel;
  maxEntries: number;
  enableConsole: boolean;
  enableFile: boolean;
  enableRemote: boolean;
  remoteEndpoint?: string;
  rotationSize?: number; // MB
}

export interface LogFilter {
  level?: LogLevel;
  startDate?: Date;
  endDate?: Date;
  context?: string;
  userId?: string;
  searchTerm?: string;
}

export class LoggingService {
  private logs: LogEntry[];
  private config: LoggerConfig;
  private contexts: Set<string>;
  private logHandlers: Map<string, (entry: LogEntry) => void>;

  constructor(config?: Partial<LoggerConfig>) {
    this.logs = [];
    this.contexts = new Set();
    this.logHandlers = new Map();
    
    // Default configuration
    this.config = {
      minLevel: LogLevel.INFO,
      maxEntries: 10000,
      enableConsole: true,
      enableFile: false,
      enableRemote: false,
      rotationSize: 10,
      ...config
    };
    
    console.log('[LoggingService] Service initialized with config:', this.config);
    this.setupHandlers();
  }

  log(level: LogLevel, message: string, context?: string, metadata?: Record<string, any>): void {
    // Check if we should log this level
    if (!this.shouldLog(level)) {
      return;
    }
    
    const entry: LogEntry = {
      id: `log_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
      level,
      message,
      context,
      metadata,
      userId: metadata?.userId
    };
    
    // Add stack trace for errors
    if (level === LogLevel.ERROR || level === LogLevel.FATAL) {
      entry.stackTrace = new Error().stack;
    }
    
    // Store log entry
    this.addLogEntry(entry);
    
    // Process through handlers
    this.processHandlers(entry);
    
    // Track context
    if (context) {
      this.contexts.add(context);
    }
  }

  debug(message: string, context?: string, metadata?: Record<string, any>): void {
    this.log(LogLevel.DEBUG, message, context, metadata);
  }

  info(message: string, context?: string, metadata?: Record<string, any>): void {
    this.log(LogLevel.INFO, message, context, metadata);
  }

  warn(message: string, context?: string, metadata?: Record<string, any>): void {
    this.log(LogLevel.WARN, message, context, metadata);
  }

  error(message: string, error?: Error, context?: string, metadata?: Record<string, any>): void {
    const errorMetadata = {
      ...metadata,
      errorName: error?.name,
      errorMessage: error?.message,
      errorStack: error?.stack
    };
    
    this.log(LogLevel.ERROR, message, context, errorMetadata);
  }

  fatal(message: string, error?: Error, context?: string, metadata?: Record<string, any>): void {
    const errorMetadata = {
      ...metadata,
      errorName: error?.name,
      errorMessage: error?.message,
      errorStack: error?.stack
    };
    
    this.log(LogLevel.FATAL, message, context, errorMetadata);
  }

  async getLogs(filter?: LogFilter): Promise<LogEntry[]> {
    console.log('[LoggingService] Retrieving logs with filter:', filter);
    
    let filteredLogs = [...this.logs];
    
    if (filter) {
      // Filter by level
      if (filter.level) {
        filteredLogs = filteredLogs.filter(log => log.level === filter.level);
      }
      
      // Filter by date range
      if (filter.startDate) {
        filteredLogs = filteredLogs.filter(log => log.timestamp >= filter.startDate!);
      }
      
      if (filter.endDate) {
        filteredLogs = filteredLogs.filter(log => log.timestamp <= filter.endDate!);
      }
      
      // Filter by context
      if (filter.context) {
        filteredLogs = filteredLogs.filter(log => log.context === filter.context);
      }
      
      // Filter by user
      if (filter.userId) {
        filteredLogs = filteredLogs.filter(log => log.userId === filter.userId);
      }
      
      // Filter by search term
      if (filter.searchTerm) {
        const searchLower = filter.searchTerm.toLowerCase();
        filteredLogs = filteredLogs.filter(log => 
          log.message.toLowerCase().includes(searchLower) ||
          JSON.stringify(log.metadata).toLowerCase().includes(searchLower)
        );
      }
    }
    
    return filteredLogs;
  }

  async exportLogs(format: 'json' | 'csv', filter?: LogFilter): Promise<string> {
    console.log(`[LoggingService] Exporting logs as ${format}...`);
    
    const logs = await this.getLogs(filter);
    
    if (format === 'json') {
      return JSON.stringify(logs, null, 2);
    } else {
      // CSV format
      const headers = ['ID', 'Timestamp', 'Level', 'Message', 'Context', 'User ID'];
      const rows = logs.map(log => [
        log.id,
        log.timestamp.toISOString(),
        log.level,
        `"${log.message.replace(/"/g, '""')}"`,
        log.context || '',
        log.userId || ''
      ]);
      
      return [headers, ...rows].map(row => row.join(',')).join('\n');
    }
  }

  clearLogs(olderThan?: Date): number {
    console.log('[LoggingService] Clearing logs...');
    
    const initialCount = this.logs.length;
    
    if (olderThan) {
      this.logs = this.logs.filter(log => log.timestamp > olderThan);
    } else {
      this.logs = [];
    }
    
    const clearedCount = initialCount - this.logs.length;
    console.log(`[LoggingService] Cleared ${clearedCount} log entries`);
    
    return clearedCount;
  }

  registerHandler(name: string, handler: (entry: LogEntry) => void): void {
    console.log(`[LoggingService] Registering log handler: ${name}`);
    this.logHandlers.set(name, handler);
  }

  unregisterHandler(name: string): void {
    console.log(`[LoggingService] Unregistering log handler: ${name}`);
    this.logHandlers.delete(name);
  }

  private setupHandlers(): void {
    // Console handler
    if (this.config.enableConsole) {
      this.registerHandler('console', (entry) => {
        const prefix = `[${entry.timestamp.toISOString()}] [${entry.level}]`;
        const contextStr = entry.context ? ` [${entry.context}]` : '';
        
        switch (entry.level) {
          case LogLevel.DEBUG:
            console.debug(`${prefix}${contextStr} ${entry.message}`, entry.metadata || '');
            break;
          case LogLevel.INFO:
            console.info(`${prefix}${contextStr} ${entry.message}`, entry.metadata || '');
            break;
          case LogLevel.WARN:
            console.warn(`${prefix}${contextStr} ${entry.message}`, entry.metadata || '');
            break;
          case LogLevel.ERROR:
          case LogLevel.FATAL:
            console.error(`${prefix}${contextStr} ${entry.message}`, entry.metadata || '');
            break;
        }
      });
    }
    
    // File handler (placeholder)
    if (this.config.enableFile) {
      this.registerHandler('file', (entry) => {
        // In real implementation, this would write to a file
        console.log('[LoggingService] Would write to file:', entry);
      });
    }
    
    // Remote handler (placeholder)
    if (this.config.enableRemote && this.config.remoteEndpoint) {
      this.registerHandler('remote', (entry) => {
        // In real implementation, this would send to remote logging service
        console.log('[LoggingService] Would send to remote:', entry);
      });
    }
  }

  private shouldLog(level: LogLevel): boolean {
    const levels = Object.values(LogLevel);
    const currentLevelIndex = levels.indexOf(level);
    const minLevelIndex = levels.indexOf(this.config.minLevel);
    
    return currentLevelIndex >= minLevelIndex;
  }

  private addLogEntry(entry: LogEntry): void {
    this.logs.push(entry);
    
    // Rotate logs if necessary
    if (this.logs.length > this.config.maxEntries) {
      const overflow = this.logs.length - this.config.maxEntries;
      this.logs.splice(0, overflow);
    }
  }

  private processHandlers(entry: LogEntry): void {
    this.logHandlers.forEach((handler) => {
      try {
        handler(entry);
      } catch (error) {
        console.error('[LoggingService] Handler error:', error);
      }
    });
  }

  getContexts(): string[] {
    return Array.from(this.contexts);
  }

  getConfig(): LoggerConfig {
    return { ...this.config };
  }

  updateConfig(updates: Partial<LoggerConfig>): void {
    console.log('[LoggingService] Updating config:', updates);
    this.config = { ...this.config, ...updates };
    
    // Re-setup handlers with new config
    this.logHandlers.clear();
    this.setupHandlers();
  }

  getStats(): Record<string, any> {
    const stats = {
      totalLogs: this.logs.length,
      byLevel: {} as Record<LogLevel, number>,
      contexts: this.contexts.size,
      oldestLog: this.logs[0]?.timestamp,
      newestLog: this.logs[this.logs.length - 1]?.timestamp
    };
    
    // Count by level
    Object.values(LogLevel).forEach(level => {
      stats.byLevel[level] = this.logs.filter(log => log.level === level).length;
    });
    
    return stats;
  }
}

// Default export
export default LoggingService;