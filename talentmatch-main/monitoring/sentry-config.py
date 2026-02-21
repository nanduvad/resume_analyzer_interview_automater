import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

def init_sentry():
    """Initialize Sentry for production monitoring"""
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[
            FlaskIntegration(),
            RedisIntegration(),
            SqlalchemyIntegration()
        ],
        # Performance monitoring
        traces_sample_rate=1.0,
        # Session replay
        replays_session_sample_rate=0.1,
        replays_on_error_sample_rate=1.0,
        
        # Environment
        environment=os.getenv('ENVIRONMENT', 'production'),
        release=os.getenv('APP_VERSION', '1.0.0'),
        
        # Security
        send_default_pii=False,  # Don't send personal data
        
        # Debugging
        debug=False,
        attach_stacktrace=True
    )
    
    # Add custom tags
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("service", "talentmatch-backend")
        scope.set_tag("region", os.getenv('AWS_REGION', 'us-east-1'))
