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

## Features

- User registration and authentication (JWT)
- Owners can create, update and delete parking spots
- Filter parkings by city, type and distance from center
- Drivers can make reservations (hourly, daily, monthly)
- Automatic price calculation based on duration
- Conflict detection — no double bookings

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/` | Register |
| POST | `/api/token/` | Get JWT token |
| GET | `/api/users/me/` | Get current user |

### Parkings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/parkings/` | List all parkings |
| POST | `/api/parkings/` | Create parking (owner only) |
| GET | `/api/parkings/{id}/` | Parking detail |
| PUT | `/api/parkings/{id}/` | Update (owner only) |
| DELETE | `/api/parkings/{id}/` | Delete (owner only) |

### Reservations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reservations/` | My reservations |
| POST | `/api/reservations/` | Create reservation |

## ⚙️ Installation

1. Clone the repository
   \`\`\`bash
   git clone https://github.com/your-username/parkeasy.git
   cd parkeasy
   \`\`\`

2. Create and activate virtual environment
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. Install dependencies
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Apply migrations
   \`\`\`bash
   python manage.py migrate
   \`\`\`

5. Run the server
   \`\`\`bash
   python manage.py runserver
   \`\`\`
