# Home App Documentation

## Overview
The Home app serves as the main landing page and dashboard for the MetaTask application. It provides basic views and templates for the application's home page.

## Models
The Home app currently doesn't contain any models as it primarily serves as a presentation layer for the application.

## Views

### home_index
Main landing page view that renders the dashboard.

```python
from django.shortcuts import render

def home_index(request):
    return render(request, 'index.html')
```

## URLs
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_index, name='home_index'),
]
```

## Templates

### index.html
The main template that extends the base template and displays the dashboard.

Location: `templates/index.html`

```html
{% extends "base.html" %}
{% block content %}
    <!-- Dashboard content -->
{% endblock %}
```

## Testing
Tests are located in `tests.py` and `tests_hello.py`. They verify the basic functionality of the home views and responses.

## Usage
The Home app is automatically included in the main URL configuration and serves as the entry point for users accessing the root URL of the application.