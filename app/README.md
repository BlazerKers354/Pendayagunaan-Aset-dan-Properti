# App Directory

This directory contains the main Flask application code.

## Structure:
- `__init__.py` - Flask application factory and configuration
- `routes.py` - All application routes and view functions
- `models.py` - Database models and data access objects
- `database.py` - Database initialization and utilities
- `data_processor.py` - Data processing utilities for CSV data
- `prediction_models.py` - ML prediction models and related functions
- `static/` - Static assets (CSS, JS, images)
- `templates/` - Jinja2 HTML templates

## Usage:
This is the core application package. Import the `create_app` function from here to initialize the Flask application.
