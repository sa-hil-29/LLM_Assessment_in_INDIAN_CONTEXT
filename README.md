# LLM Assessment (Indian Context)

A Django-based web application scaffold for building an LLM assessment platform tailored to the Indian context.

## Setup

1. Create and activate a Python virtual environment
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations
   ```bash
   python manage.py migrate
   ```
4. Start the development server
   ```bash
   python manage.py runserver
   ```

## Project structure

- `llm_assessment/` — Django project settings and URLs
- `assessment/` — core app for assessment workflows

## Notes

This scaffold includes a simple homepage and ready-to-expand assessment app.
