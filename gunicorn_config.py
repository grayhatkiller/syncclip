# gunicorn_config.py

# Number of worker processes
workers = 4

# Bind to localhost only, since Nginx will proxy the requests
bind = '127.0.0.1:5000'

# Worker class
worker_class = 'sync'  # You might want to experiment with 'gevent' for better performance

# Timeout
timeout = 120  # Increase timeout to handle long-running requests

# Limit the number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50  # Add some randomness to the max_requests setting

# Logging
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'

# Disable the use of sendfile()
sendfile = False

# Preload the application before forking worker processes
preload_app = True

# Daemon mode
daemon = False  # Set to True if you want to run Gunicorn in the background

# User and group to run the workers as
user = 'www-data'
group = 'www-data'

# Process naming
proc_name = 'syncclip_gunicorn'

# Paste logger for more detailed logs
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'level': 'INFO',
            'filename': '/var/log/gunicorn/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}
