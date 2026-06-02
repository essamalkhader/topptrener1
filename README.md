# ToppTrener

A web-based sports training booking platform built with Django.

## About
ToppTrener connects professional sports trainers with athletes and fitness enthusiasts in Oslo, Norway. Trainers can create and manage training sessions, while trainees can browse, filter, and book sessions using membership credits or direct payment.

## Features
- Role-based system (Trainers and Trainees)
- Session browsing with search and filter
- Credit-based booking with membership plans
- Simulated payment for non-members
- Trainer dashboard with session management
- Review and star rating system
- Trainer public profiles

## Setup Instructions
1. Clone the repository
2. Create a virtual environment: `python -m venv env`
3. Activate it: `env\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Load sample data: `python manage.py loaddata data.json`
7. Run the server: `python manage.py runserver`

## Sample Credentials
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| erik | trainer123 | Trainer |
| sarah | trainer123 | Trainer |
| alex | trainee123 | Trainee (Plus membership) |
| mia | trainee123 | Trainee (Basic membership) |
| lucas | trainee123 | Trainee (No membership) |

## Technology Stack
- Python 3.12
- Django 6.0.3
- SQLite
- Tailwind CSS
- Pillow
- pytz
- JavaScript

## Course
ELE 3921 Web Applications Development — BI Norwegian Business School, Spring 2026
Student: ESAM ALBAADANI (s2418660)