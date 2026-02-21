# monitoring/production_monitor.py
import os
import logging
import psutil
from datetime import datetime
import boto3
import requests
import redis
import psycopg2
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Configure Sentry for error tracking
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    environment="production",
    release=os.getenv('APP_VERSION', '1.0.0')
)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/talentmatch/production.log'),
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            '/var/log/talentmatch/production_rotating.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
    ]
)

logger = logging.getLogger(__name__)

class ProductionMonitor:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        self.metrics_namespace = 'TalentMatch/Production'
        
        # Prometheus metrics
        self.request_count = Counter('http_requests_total', 'Total HTTP requests', ['endpoint', 'method'])
        self.request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['endpoint'])
        self.error_count = Counter('http_errors_total', 'Total HTTP errors', ['endpoint', 'status_code'])
        self.active_users = Gauge('active_users_total', 'Total active users')
        self.response_size = Histogram('http_response_size_bytes', 'HTTP response size in bytes', ['endpoint'])
        
        # Start Prometheus metrics server
        start_http_server(8000)
    
    def log_auth_event(self, user_id, event_type, metadata=None):
        """Log authentication events for security monitoring"""
        if metadata is None:
            metadata = {}
            
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'event_type': event_type,
            'ip_address': metadata.get('ip'),
            'user_agent': metadata.get('user_agent'),
            'success': metadata.get('success', True),
            'details': metadata
        }
        
        # Send to CloudWatch
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.metrics_namespace,
                MetricData=[
                    {
                        'MetricName': 'AuthenticationEvents',
                        'Dimensions': [
                            {'Name': 'EventType', 'Value': event_type},
                            {'Name': 'Success', 'Value': str(metadata.get('success', True))}
                        ],
                        'Value': 1,
                        'Unit': 'Count',
                        'Timestamp': datetime.now()
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to send CloudWatch metrics: {e}")
        
        # Log for security audit
        if not metadata.get('success'):
            logger.warning(f"Auth failure: {log_entry}")
            # Trigger security alert
            self.send_security_alert(log_entry)
            # Send to Sentry
            sentry_sdk.capture_message(
                f"Authentication failure for user {user_id}",
                level='warning',
                extra=log_entry
            )
        else:
            logger.info(f"Auth event: {log_entry}")
    
    def send_security_alert(self, log_entry):
        """Send security alerts to SOC team"""
        try:
            # Example: Send to AWS SNS for alerting
            sns = boto3.client('sns')
            sns.publish(
                TopicArn=os.getenv('SECURITY_ALERT_SNS_ARN'),
                Subject='Security Alert: Authentication Failure',
                Message=json.dumps(log_entry, indent=2)
            )
            
            # Could also integrate with:
            # - PagerDuty: https://developer.pagerduty.com/
            # - OpsGenie: https://docs.opsgenie.com/docs/aws-sns-integration
            # - Slack webhook
            # - Microsoft Teams webhook
            
        except Exception as e:
            logger.error(f"Failed to send security alert: {e}")
    
    def monitor_performance(self, endpoint, duration, status_code, method='GET', response_size=0):
        """Monitor API performance"""
        self.request_count.labels(endpoint=endpoint, method=method).inc()
        self.request_duration.labels(endpoint=endpoint).observe(duration)
        self.response_size.labels(endpoint=endpoint).observe(response_size)
        
        if status_code >= 400:
            self.error_count.labels(endpoint=endpoint, status_code=str(status_code)).inc()
        
        # Send to CloudWatch for AWS integration
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.metrics_namespace,
                MetricData=[
                    {
                        'MetricName': 'RequestDuration',
                        'Dimensions': [
                            {'Name': 'Endpoint', 'Value': endpoint},
                            {'Name': 'Method', 'Value': method},
                            {'Name': 'StatusCode', 'Value': str(status_code)}
                        ],
                        'Value': duration,
                        'Unit': 'Seconds',
                        'Timestamp': datetime.now()
                    },
                    {
                        'MetricName': 'ResponseSize',
                        'Dimensions': [
                            {'Name': 'Endpoint', 'Value': endpoint}
                        ],
                        'Value': response_size,
                        'Unit': 'Bytes',
                        'Timestamp': datetime.now()
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to send CloudWatch metrics: {e}")
    
    def health_check(self):
        """Production health check endpoint"""
        checks = {
            'database': self.check_database(),
            'redis': self.check_redis(),
            'external_apis': self.check_external_apis(),
            'disk_space': self.check_disk_space(),
            'memory_usage': self.check_memory_usage(),
            'cpu_usage': self.check_cpu_usage()
        }
        
        overall_health = all(checks.values())
        
        # Send health status to CloudWatch
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.metrics_namespace,
                MetricData=[
                    {
                        'MetricName': 'HealthStatus',
                        'Value': 1 if overall_health else 0,
                        'Unit': 'Count',
                        'Timestamp': datetime.now()
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to send health check metrics: {e}")
        
        return {
            'status': 'healthy' if overall_health else 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'checks': checks,
            'version': os.getenv('APP_VERSION', 'unknown'),
            'environment': os.getenv('ENVIRONMENT', 'production')
        }
    
    def check_database(self):
        """Check database connectivity"""
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                connect_timeout=5
            )
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def check_redis(self):
        """Check Redis connectivity"""
        try:
            redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                password=os.getenv('REDIS_PASSWORD'),
                socket_timeout=5
            )
            redis_client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
    
    def check_external_apis(self):
        """Check external API dependencies"""
        try:
            # Check Google OAuth endpoint
            response = requests.get('https://accounts.google.com/.well-known/openid-configuration', timeout=5)
            response.raise_for_status()
            
            # Check other critical APIs if needed
            # response = requests.get('https://api.someservice.com/health', timeout=5)
            
            return True
        except Exception as e:
            logger.error(f"External API health check failed: {e}")
            return False
    
    def check_disk_space(self):
        """Check disk space availability"""
        try:
            disk_usage = psutil.disk_usage('/')
            return disk_usage.percent < 90  # Alert if > 90% used
        except Exception as e:
            logger.error(f"Disk space check failed: {e}")
            return False
    
    def check_memory_usage(self):
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            return memory.percent < 85  # Alert if > 85% used
        except Exception as e:
            logger.error(f"Memory check failed: {e}")
            return False
    
    def check_cpu_usage(self):
        """Check CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            return cpu_percent < 80  # Alert if > 80% used
        except Exception as e:
            logger.error(f"CPU check failed: {e}")
            return False
    
    def track_user_activity(self, user_id, action):
        """Track user activity for analytics"""
        self.active_users.inc()
        
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.metrics_namespace,
                MetricData=[
                    {
                        'MetricName': 'UserActivity',
                        'Dimensions': [
                            {'Name': 'Action', 'Value': action}
                        ],
                        'Value': 1,
                        'Unit': 'Count',
                        'Timestamp': datetime.now()
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to track user activity: {e}")

# Singleton instance
monitor = ProductionMonitor()

