# Mediap App Documentation

## Overview
The Mediap app serves as the core configuration app for the MetaTask project, containing the main settings, URL configurations, and WSGI/ASGI application setup.

## Configuration Files

### settings.py
Contains all Django settings for the project:
- Database configuration
- Installed apps
- Middleware settings
- Template configuration
- Static/Media files settings
- Authentication settings

### urls.py
Main URL configuration file that includes all app URLs:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('cflows/', include('cflows.urls')),
]
```

### hosts.py
Defines the host configurations for the project:
```python
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', 'Mediap.urls', name='www'),
    host(r'(\w+)', 'Mediap.urls', name='wildcard'),
)
```

### wsgi.py
WSGI application configuration for production deployment:
```python
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### asgi.py
ASGI application configuration for async capabilities:
```python
from django.core.asgi import get_asgi_application
application = get_asgi_application()
```

## Static Files
Static files are configured in settings.py and served from:
- Development: 'static/' directory
- Production: 'staticfiles/' directory (after collectstatic)

### Structure
```
static/
├── css/
│   └── global.css
├── js/
│   └── global.js
└── images/
```

## Templates
Global templates are stored in the templates directory:
```
templates/
└── base.html
```

## Environment Variables
Important environment variables used by the application:
- `DEBUG`: Debug mode flag
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: List of allowed hosts

## Usage

### Development Setup
1. Configure environment variables
2. Run migrations
3. Create superuser
4. Run development server

### Production Deployment
1. Set DEBUG=False
2. Configure production database
3. Run collectstatic
4. Set up WSGI/ASGI server
5. Configure allowed hosts

## Security
Key security features configured in settings.py:
- CSRF protection
- XSS prevention
- Session security
- Password validation
- SSL/HTTPS settings