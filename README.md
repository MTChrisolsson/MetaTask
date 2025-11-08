# MetaTask

A comprehensive multi-tenant Django platform for hosting distinct web applications under a unified domain structure with subdomain-based routing.

## 🎯 Project Overview

MetaTask (formerly Mediap) is designed to host multiple related web applications under a single organizational domain. The platform features:

- **Subdomain-based routing** using django-hosts
- **Multi-tenant architecture** with organization-level data segregation
- **Custom authentication** with email-based login
- **Modular app structure** allowing independent but integrated applications

## 🏗️ Architecture

### Subdomain Routing

The project uses `django-hosts` to route traffic to different Django applications:

- **Main Host** (`metatask.org` or `www.metatask.org`): Landing page, authentication flows (`/login/`, `/register/`)
- **Sub-Hosts** (e.g., `cflows.metatask.org`): Dedicated application instances

### Multi-Tenancy

All business data is isolated by [`Organization`](accounts/models.py):

- Each [`Account`](accounts/models.py) belongs to one [`Organization`](accounts/models.py)
- Business models (e.g., [`Car`](cflows/models.py) in CFlows) link to [`Organization`](accounts/models.py) via `ForeignKey`
- Views filter data strictly by the user's organization

### Custom User Model

The [`accounts`](accounts/) app provides a custom [`Account`](accounts/models.py) model:

- Extends `AbstractBaseUser`
- Uses **email** as the primary identifier (no username)
- Linked to [`Organization`](accounts/models.py) via `ForeignKey` (related_name='members')

## 📁 Project Structure

```
MetaTask/
├── accounts/           # Custom user & authentication
│   ├── models.py      # Account, Organization models
│   ├── views.py       # login, logout, register views
│   ├── forms.py       # Registration & auth forms
│   └── urls.py        # Auth URL patterns
├── cflows/            # Car management application
│   ├── models.py      # Car model (multi-tenant)
│   ├── views.py       # CRUD views
│   └── urls.py        # CFlows URL patterns
├── home/              # Main landing page app
│   ├── views.py       # Home views
│   └── urls.py        # Home URL patterns
├── Mediap/            # Project settings & configuration
│   ├── settings.py    # Django settings
│   ├── hosts.py       # django-hosts configuration
│   ├── urls.py        # Root URL configuration
│   └── wsgi.py        # WSGI application
├── templates/         # Global templates
│   └── base.html      # Base template with navigation
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/MetaTask.git
cd MetaTask
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

7. **Access the application**

- Main site: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin

## 🔧 Configuration

### Key Settings

Edit [`Mediap/settings.py`](Mediap/settings.py) for:

- `SECRET_KEY`: Django secret key (change in production!)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain names
- `AUTH_USER_MODEL`: Points to `'accounts.Account'`

### Hosts Configuration

See [`Mediap/hosts.py`](Mediap/hosts.py) for subdomain routing rules:

```python
host_patterns = [
    host(r'www', 'home.urls', name='www'),
    host(r'cflows', 'cflows.urls', name='cflows'),
    # Add more subdomains here
]
```

## 📦 Core Dependencies

- **Django 5.2.7**: Web framework
- **django-hosts**: Subdomain routing
- **Pillow**: Image handling (if using ImageFields)
- **pytest & pytest-django**: Testing framework

See [`requirements.txt`](requirements.txt) for the complete list.

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

Run Django's system checks:

```bash
python manage.py check
```

## 🗄️ Database

Currently using SQLite (`db.sqlite3`) for development. For production, configure PostgreSQL or MySQL in [`Mediap/settings.py`](Mediap/settings.py).

## 🔐 Authentication

Authentication is handled by the [`accounts`](accounts/) app:

- **Registration**: [`/register/`](accounts/urls.py)
- **Login**: [`/login/`](accounts/urls.py)
- **Logout**: [`/logout/`](accounts/urls.py)

All authentication URLs are served from the main host.

## 🎨 Apps

### Home

Landing page and general information served at the root domain.

### CFlows

Car fleet management application:
- Accessible at `cflows.metatask.org`
- Multi-tenant: data filtered by organization
- CRUD operations for vehicles

### Accounts

User and organization management:
- Custom [`Account`](accounts/models.py) model
- [`Organization`](accounts/models.py) model for multi-tenancy
- Authentication views and forms

## 📝 Development Notes

- **Old Project Name**: Some references to "Mediap" may still exist in the codebase
- **Multi-tenancy**: Always filter queries by `request.user.organization`
- **Testing**: Test files include [`home/tests_hello.py`](home/tests_hello.py), use pytest for running tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Contact

Project Link: [https://github.com/yourusername/MetaTask](https://github.com/yourusername/MetaTask)

## 🙏 Acknowledgments

- Django Framework
- django-hosts for subdomain routing
- All contributors to the project
