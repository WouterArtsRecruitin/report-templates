/**
 * Performance Monitor Module
 * Handles performance monitoring, metrics collection, and optimization tracking
 */

export interface PerformanceMetric {
  id: string;
  name: string;
  value: number;
  unit: string;
  timestamp: Date;
  category: MetricCategory;
  tags?: Record<string, string>;
}

export enum MetricCategory {
  SYSTEM = 'SYSTEM',
  APPLICATION = 'APPLICATION',
  DATABASE = 'DATABASE',
  API = 'API',
  USER_EXPERIENCE = 'USER_EXPERIENCE',
  BUSINESS = 'BUSINESS'
}

export interface PerformanceThreshold {
  metricName: string;
  warning: number;
  critical: number;
  unit: string;
}

export interface AlertConfig {
  enabled: boolean;
  thresholds: PerformanceThreshold[];
  notificationEndpoint?: string;
}

export interface TimingData {
  startTime: number;
  endTime?: number;
  duration?: number;
  operation: string;
  metadata?: Record<string, any>;
}

export class PerformanceMonitor {
  private metrics: Map<string, PerformanceMetric[]>;
  private timers: Map<string, TimingData>;
  private thresholds: Map<string, PerformanceThreshold>;
  private alertConfig: AlertConfig;
  private collectors: Map<string, () => Promise<PerformanceMetric[]>>;

  constructor(alertConfig?: Partial<AlertConfig>) {
    this.metrics = new Map();
    this.timers = new Map();
    this.thresholds = new Map();
    this.collectors = new Map();
    
    this.alertConfig = {
      enabled: true,
      thresholds: [],
      ...alertConfig
    };
    
    console.log('[PerformanceMonitor] Service initialized');
    this.setupSystemCollectors();
    this.startPeriodicCollection();
  }

  recordMetric(metric: Omit<PerformanceMetric, 'id' | 'timestamp'>): void {
    const fullMetric: PerformanceMetric = {
      id: `metric_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
      ...metric
    };
    
    const metricList = this.metrics.get(metric.name) || [];
    metricList.push(fullMetric);
    
    // Keep only last 1000 metrics per type
    if (metricList.length > 1000) {
      metricList.shift();
    }
    
    this.metrics.set(metric.name, metricList);
    
    console.log(`[PerformanceMonitor] Recorded metric: ${metric.name} = ${metric.value} ${metric.unit}`);
    
    // Check thresholds
    this.checkThresholds(fullMetric);
  }

  startTimer(operation: string, metadata?: Record<string, any>): string {
    const timerId = `timer_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const timerData: TimingData = {
      startTime: performance.now(),
      operation,
      metadata
    };
    
    this.timers.set(timerId, timerData);
    console.log(`[PerformanceMonitor] Started timer for operation: ${operation}`);
    
    return timerId;
  }

  stopTimer(timerId: string): number | null {
    const timerData = this.timers.get(timerId);
    
    if (!timerData) {
      console.warn(`[PerformanceMonitor] Timer not found: ${timerId}`);
      return null;
    }
    
    const endTime = performance.now();
    const duration = endTime - timerData.startTime;
    
    timerData.endTime = endTime;
    timerData.duration = duration;
    
    // Record as metric
    this.recordMetric({
      name: `operation_duration_${timerData.operation}`,
      value: duration,
      unit: 'ms',
      category: MetricCategory.APPLICATION,
      tags: {
        operation: timerData.operation,
        ...timerData.metadata
      }
    });
    
    this.timers.delete(timerId);
    console.log(`[PerformanceMonitor] Stopped timer for ${timerData.operation}: ${duration.toFixed(2)}ms`);
    
    return duration;
  }

  async measureAsync<T>(operation: string, fn: () => Promise<T>, metadata?: Record<string, any>): Promise<T> {
    const timerId = this.startTimer(operation, metadata);
    
    try {
      const result = await fn();
      this.stopTimer(timerId);
      return result;
    } catch (error) {
      this.stopTimer(timerId);
      
      // Record error metric
      this.recordMetric({
        name: `operation_error_${operation}`,
        value: 1,
        unit: 'count',
        category: MetricCategory.APPLICATION,
        tags: {
          operation,
          error: error instanceof Error ? error.message : 'Unknown error'
        }
      });
      
      throw error;
    }
  }

  measureSync<T>(operation: string, fn: () => T, metadata?: Record<string, any>): T {
    const timerId = this.startTimer(operation, metadata);
    
    try {
      const result = fn();
      this.stopTimer(timerId);
      return result;
    } catch (error) {
      this.stopTimer(timerId);
      
      // Record error metric
      this.recordMetric({
        name: `operation_error_${operation}`,
        value: 1,
        unit: 'count',
        category: MetricCategory.APPLICATION,
        tags: {
          operation,
          error: error instanceof Error ? error.message : 'Unknown error'
        }
      });
      
      throw error;
    }
  }

  getMetrics(metricName?: string, category?: MetricCategory, limit?: number): PerformanceMetric[] {
    console.log('[PerformanceMonitor] Retrieving metrics...');
    
    let allMetrics: PerformanceMetric[] = [];
    
    if (metricName) {
      allMetrics = this.metrics.get(metricName) || [];
    } else {
      // Get all metrics
      for (const metricList of this.metrics.values()) {
        allMetrics.push(...metricList);
      }
    }
    
    // Filter by category
    if (category) {
      allMetrics = allMetrics.filter(metric => metric.category === category);
    }
    
    // Sort by timestamp (newest first)
    allMetrics.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    
    // Apply limit
    if (limit && limit > 0) {
      allMetrics = allMetrics.slice(0, limit);
    }
    
    return allMetrics;
  }

  getAverageMetric(metricName: string, timeWindow?: number): number | null {
    const metrics = this.metrics.get(metricName);
    
    if (!metrics || metrics.length === 0) {
      return null;
    }
    
    let filteredMetrics = metrics;
    
    // Filter by time window (in minutes)
    if (timeWindow) {
      const cutoff = new Date(Date.now() - timeWindow * 60 * 1000);
      filteredMetrics = metrics.filter(metric => metric.timestamp > cutoff);
    }
    
    if (filteredMetrics.length === 0) {
      return null;
    }
    
    const sum = filteredMetrics.reduce((acc, metric) => acc + metric.value, 0);
    return sum / filteredMetrics.length;
  }

  setThreshold(threshold: PerformanceThreshold): void {
    console.log(`[PerformanceMonitor] Setting threshold for ${threshold.metricName}`);
    this.thresholds.set(threshold.metricName, threshold);
  }

  removeThreshold(metricName: string): void {
    console.log(`[PerformanceMonitor] Removing threshold for ${metricName}`);
    this.thresholds.delete(metricName);
  }

  registerCollector(name: string, collector: () => Promise<PerformanceMetric[]>): void {
    console.log(`[PerformanceMonitor] Registering collector: ${name}`);
    this.collectors.set(name, collector);
  }

  unregisterCollector(name: string): void {
    console.log(`[PerformanceMonitor] Unregistering collector: ${name}`);
    this.collectors.delete(name);
  }

  async getSystemHealth(): Promise<Record<string, any>> {
    console.log('[PerformanceMonitor] Generating system health report...');
    
    const health = {
      timestamp: new Date(),
      overall: 'healthy',
      metrics: {} as Record<string, any>,
      alerts: [] as string[]
    };
    
    // Check key metrics
    const cpuUsage = this.getAverageMetric('cpu_usage', 5);
    const memoryUsage = this.getAverageMetric('memory_usage', 5);
    const responseTime = this.getAverageMetric('api_response_time', 10);
    
    health.metrics = {
      cpuUsage: cpuUsage ? `${cpuUsage.toFixed(1)}%` : 'N/A',
      memoryUsage: memoryUsage ? `${memoryUsage.toFixed(1)}%` : 'N/A',
      averageResponseTime: responseTime ? `${responseTime.toFixed(2)}ms` : 'N/A'
    };
    
    // Check for alerts
    if (cpuUsage && cpuUsage > 80) {
      health.alerts.push('High CPU usage detected');
      health.overall = 'warning';
    }
    
    if (memoryUsage && memoryUsage > 85) {
      health.alerts.push('High memory usage detected');
      health.overall = 'critical';
    }
    
    if (responseTime && responseTime > 1000) {
      health.alerts.push('Slow API response times detected');
      health.overall = health.overall === 'critical' ? 'critical' : 'warning';
    }
    
    return health;
  }

  private setupSystemCollectors(): void {
    // CPU usage collector
    this.registerCollector('cpu', async () => {
      const usage = Math.random() * 100; // Mock data
      return [{
        id: `cpu_${Date.now()}`,
        name: 'cpu_usage',
        value: usage,
        unit: 'percent',
        timestamp: new Date(),
        category: MetricCategory.SYSTEM
      }];
    });
    
    // Memory usage collector
    this.registerCollector('memory', async () => {
      const usage = Math.random() * 100; // Mock data
      return [{
        id: `mem_${Date.now()}`,
        name: 'memory_usage',
        value: usage,
        unit: 'percent',
        timestamp: new Date(),
        category: MetricCategory.SYSTEM
      }];
    });
    
    // API response time collector
    this.registerCollector('api', async () => {
      const responseTime = 50 + Math.random() * 500; // Mock data
      return [{
        id: `api_${Date.now()}`,
        name: 'api_response_time',
        value: responseTime,
        unit: 'ms',
        timestamp: new Date(),
        category: MetricCategory.API
      }];
    });
  }

  private startPeriodicCollection(): void {
    console.log('[PerformanceMonitor] Starting periodic metric collection...');
    
    setInterval(async () => {
      for (const [name, collector] of this.collectors) {
        try {
          const metrics = await collector();
          metrics.forEach(metric => {
            const metricList = this.metrics.get(metric.name) || [];
            metricList.push(metric);
            
            if (metricList.length > 1000) {
              metricList.shift();
            }
            
            this.metrics.set(metric.name, metricList);
            this.checkThresholds(metric);
          });
        } catch (error) {
          console.error(`[PerformanceMonitor] Collector ${name} failed:`, error);
        }
      }
    }, 30000); // Collect every 30 seconds
  }

  private checkThresholds(metric: PerformanceMetric): void {
    const threshold = this.thresholds.get(metric.name);
    
    if (!threshold || !this.alertConfig.enabled) {
      return;
    }
    
    if (metric.value >= threshold.critical) {
      console.error(`[PerformanceMonitor] CRITICAL: ${metric.name} = ${metric.value} ${metric.unit} (threshold: ${threshold.critical})`);
      this.sendAlert('critical', metric, threshold);
    } else if (metric.value >= threshold.warning) {
      console.warn(`[PerformanceMonitor] WARNING: ${metric.name} = ${metric.value} ${metric.unit} (threshold: ${threshold.warning})`);
      this.sendAlert('warning', metric, threshold);
    }
  }

  private sendAlert(severity: 'warning' | 'critical', metric: PerformanceMetric, threshold: PerformanceThreshold): void {
    // In real implementation, this would send alerts to configured endpoints
    console.log(`[PerformanceMonitor] ${severity.toUpperCase()} ALERT:`, {
      metric: metric.name,
      value: metric.value,
      threshold: severity === 'critical' ? threshold.critical : threshold.warning,
      timestamp: metric.timestamp
    });
  }

  clearMetrics(metricName?: string): void {
    if (metricName) {
      console.log(`[PerformanceMonitor] Clearing metrics for: ${metricName}`);
      this.metrics.delete(metricName);
    } else {
      console.log('[PerformanceMonitor] Clearing all metrics');
      this.metrics.clear();
    }
  }

  getStats(): Record<string, any> {
    return {
      totalMetrics: Array.from(this.metrics.values()).reduce((sum, list) => sum + list.length, 0),
      metricTypes: this.metrics.size,
      activeTimers: this.timers.size,
      thresholds: this.thresholds.size,
      collectors: this.collectors.size
    };
  }
}

// Default export
export default PerformanceMonitor;