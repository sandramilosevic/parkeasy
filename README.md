# ParkEasy

A parking reservation platform built with Django REST Framework.  
Owners can list their parking spots, drivers can search and reserve them.

## Tech Stack

- **Python** / **Django 5.2**
- **Django REST Framework** — API
- **Simple JWT** — Authentication
- **PostgreSQL** — Database
- **django-filters** — Filtering, search and ordering
- **drf-yasg** — Auto-generated Swagger/ReDoc API docs
- **django-cors-headers** — CORS support
- **python-decouple** — Environment variables

- ## User Roles

| Role | Description |
|------|-------------|
| `owner` | Can list and manage parking spots |
| `driver` | Can search and reserve parking spots |
