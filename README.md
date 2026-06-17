# KONECTA H0: Sparring Marketplace MVP

## 🎯 Overview

KONECTA is a **smart sparring marketplace** for boxers, MMA fighters and Muay Thai practitioners. Connect compatible athletes, record sparring partners, and maintain a real-time ELO ranking system.

> **Key Feature:** Instead of manually searching for partners on WhatsApp, users find sparring partners with a smart algorithm that considers: sport, weight, experience, and statistics.

### 🎬 Demo Video

[H0 Hackathon Submission Video - YouTube Link](https://youtube.com)

---

## ✨ Features

### MVP (Sprint 1-3, June 1-30)

* ✅ **User Authentication** - Signup/login with JWT + AWS Cognito
* ✅ **User Profiles** - Profile with an "octagon" (8 attributes: speed, defense, technique, power, cardio, adaptability, aggression, precision)
* ✅ **Smart Matching** - Algorithm that finds compatible partners based on: sport, weight (±5kg), experience, gym
* ✅ **Sparring Recording** - Record sparring sessions, date, and details
* ✅ **Voting System** - Both users vote for the winner. If they match → final result
* ✅ **ELO Ranking** - Automatic ranking update based on a chess formula
* ✅ **Leaderboard** - Top 100 users per gym, filterable by sport
* ✅ **Admin Dashboard** - Next.js dashboard with users, analytics, and leaderboard

### Roadmap (Post-MVP)

* 🔄 **Mobile App** (React Native) - iOS + Android
* 🔄 **Real-time Notifications** - WebSockets
* 🔄 **Challenges with Betting** - Points system
* 🔄 **Wallet & Monetization** - Konecta 20% commission

---

## 🛠️ Technology Stack

| Category | Components & Technologies |
| --- | --- |
| **Backend** | **Language:** Python 3.11 <br>

<br> **Framework:** FastAPI 0.104 <br>

<br> **ORM:** SQLAlchemy 2.0 (async) <br>

<br> **Database:** PostgreSQL 15 (Aurora RDS) <br>

<br> **Auth:** AWS Cognito + JWT (PyJWT) <br>

<br> **Compute:** AWS Lambda <br>

<br> **Gateway:** AWS API Gateway <br>

<br> **Testing:** pytest |
| **Frontend** | **Framework:** Next.js 14 <br>

<br> **Library:** React 18 <br>

<br> **Language:** TypeScript <br>

<br> **Styling:** Tailwind CSS 3 <br>

<br> **Deployment:** Vercel |
| **Infrastructure** | **Compute:** AWS Lambda (serverless) <br>

<br> **Database:** AWS Aurora PostgreSQL <br>

<br> **Auth:** AWS Cognito <br>

<br> **CDN:** Vercel Edge Network <br>

<br> **Monitoring:** CloudWatch + Sentry (future) |

---

## 📦 Architecture

### System Design

```text
┌─────────────────────────────────────────────────────────┐
│                      User (Browser)                     │
└──────────────────────────┬──────────────────────────────┘
                           │
                 ┌─────────┴────────┐
                 │                  │
         ┌───────▼────────┐ ┌───────▼─────────┐
         │   Vercel CDN   │ │   API Gateway   │
         │   (Next.js)    │ │      (AWS)      │
         │ - Dashboard    │ │                 │
         │ - Pages        │ └────────┬────────┘
         │ - Components   │          │
         └────────────────┘ ┌────────▼────────┐
                            │   AWS Lambda    │
                            │   (FastAPI)     │
                            │ - /auth/...     │
                            │ - /api/users    │
                            │ - /api/matching │
                            │ - /api/sparrings│
                            │ - /api/ranking  │
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │   Aurora RDS    │
                            │  (PostgreSQL)   │
                            │ - users         │
                            │ - sparring      │
                            │ - vote          │
                            │ - rankings      │
                            └─────────────────┘

```

### Data Flow (Example: User Search for Sparring Partner)

1. User opens dashboard (Vercel)
2. Click "Find Partners" button
3. Frontend calls: `GET /api/matching?sport=BOXING&weight=75`
4. API Gateway routes to Lambda
5. Lambda executes FastAPI:
* Validates JWT token
* Queries PostgreSQL for compatible users
* Returns JSON list


6. Frontend renders list of candidates
7. User clicks "Request Sparring"
8. Frontend calls: `POST /api/sparrings` (with opponent_id)
9. Lambda persists in database
10. Both users notified (future: WebSockets)

---

## 🚀 Getting Started

### Prerequisites

* Node.js 18+
* Python 3.11+
* Docker (for local PostgreSQL)
* AWS Account (for deployment)

### Backend Setup

```bash
# Clone repo
git clone https://github.com/yourusername/konecta-h0.git
cd konecta-h0

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Local PostgreSQL setup
docker-compose up -d

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
# Server runs on http://localhost:8000
# Swagger UI: http://localhost:8000/docs

```

### Frontend Setup

```bash
# Frontend (in new terminal)
cd frontend
npm install
npm run dev
# App runs on http://localhost:3000

```

---

## 📋 API Documentation

All endpoints are documented with **Swagger UI** (OpenAPI):

* **Endpoint:** `http://localhost:8000/docs`
* **Alternative:** `http://localhost:8000/redoc`

### Authentication Endpoints

* `POST /auth/signup` - Register new user
* `POST /auth/login` - Login & get JWT token

### User Endpoints

* `GET /api/users/me` - Get current user profile (requires JWT)
* `GET /api/users/{id}` - Get user by ID (public)
* `POST /api/users` - Create user (admin)

### Matching & Sparring

* `GET /api/matching` - Find compatible partners
* `POST /api/sparrings` - Create sparring event
* `POST /api/sparrings/{id}/vote` - Vote on sparring result
* `GET /api/ranking` - Get leaderboard (top 100)

---

## 🧪 Testing

### Unit Tests

```bash
cd backend
pytest -v                  # Run all tests
pytest --cov               # With coverage report
pytest tests/test_auth.py  # Specific test file

```

### Manual Testing (Postman)

* **Import:** `backend/postman_collection.json`
* **Use environment:** `backend/postman_environment.json`
* Run requests in order

---

## 🔐 Security

### Password Security

* Passwords are hashed with bcrypt (passlib)
* Never stored in plain text
* Minimum 8 characters required

### JWT Tokens

* Issued by backend with HS256 algorithm
* Expire after 30 minutes
* Signature prevents tampering
* Validated on every protected endpoint

### Database

* Aurora uses encryption at rest
* VPC for private access
* No public internet exposure

---

## 📊 Performance Metrics

* **Cold Start:** 200-400ms (Python Lambda)
* **API Response:** <100ms (p95) with indexed queries
* **Page Load:** <2s (Next.js + Vercel CDN)
* **Uptime:** 99.9% (AWS managed)
* **Concurrent Users:** Auto-scales to 10,000+

---

## 🗂️ Project Structure

```text
konecta-h0/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app instance
│   │   ├── config.py            # Settings (Pydantic)
│   │   ├── api/                 # Route handlers
│   │   │   ├── auth.py          # Auth endpoints
│   │   │   ├── users.py         # User endpoints
│   │   │   ├── sparrings.py     # Sparring endpoints
│   │   │   ├── matching.py      # Matching algorithm
│   │   │   └── ranking.py       # Leaderboard
│   │   ├── services/            # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── matching_service.py
│   │   │   └── ranking_engine.py
│   │   ├── models/              # Data models
│   │   │   ├── db_models.py     # SQLAlchemy ORM
│   │   │   └── schemas.py       # Pydantic validation
│   │   ├── db/                  # Database
│   │   │   ├── database.py      # SQLAlchemy engine
│   │   │   └── migrations/      # Alembic versions
│   │   ├── middleware/          # Auth, error handling
│   │   └── utils/               # Helpers (JWT, password)
│   ├── tests/                   # Unit tests
│   ├── requirements.txt
│   ├── docker-compose.yml       # Local PostgreSQL
│   ├── .env.example
│   └── zappa_settings.json      # AWS Lambda config
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Home page
│   │   ├── dashboard/           # Dashboard pages
│   │   ├── layout.tsx           # Root layout
│   │   └── api/                 # API calls (lib)
│   ├── components/              # React components
│   ├── public/                  # Static assets
│   └── package.json
├── docs/
│   ├── 01_MVP_Definition.md
│   ├── 02_TechStack.md
│   └── API.md
└── README.md

```

---

## 📖 Documentation in process

* **[MVP Definition](https://www.google.com/search?q=./docs/01_MVP_Definition.md)** - Scope & requirements
* **[Tech Stack](https://www.google.com/search?q=./docs/TechStack_Architecture_KONECTA_H0.md)** - Architecture decisions
* **[API Reference](https://www.google.com/search?q=./docs/API.md)** - Detailed endpoint docs
* **[Deployment Guide](https://www.google.com/search?q=./docs/DEPLOYMENT.md)** - AWS Lambda + Vercel setup

---

## 👨‍💻 Development Workflow

### Branches

* `main` → Production (H0 Submission)
* `develop` → Integration branch
* `feature/KO-*` → Feature branches (KO-101, KO-104, etc)
* `bugfix/KO-*` → Bug fixes

### Feature Development (Example)

```bash
# Create feature branches
git checkout -b feature/KO-104-auth-system

# Develop & test locally
# ... code changes ...
# pytest -v

# Commit with clear message
git commit -m "KO-104: Implement auth system (signup/login + JWT)"

# Push to GitHub
git push origin feature/KO-104-auth-system

# Create PR to develop
# Code review → merge

```

---

## 🚀 Deployment

### Frontend (Vercel)

```bash
cd frontend
git push origin main
# Automatically deploys on push
# URL: https://konecta-h0.vercel.app

```

### Backend (AWS Lambda)

```bash
cd backend
zappa deploy dev  # First deployment
zappa update dev  # Subsequent updates
zappa logs -t dev # View logs

```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

## 👤 Author

**[Javier L]**

* **GitHub:** [@javtl](https://www.github.com/javtl)
* **LinkedIn:** [Your LinkedIn](https://www.linkedin.com/in/javierlsw/)

---

## 🙏 Acknowledgments

* H0 Hackathon organizers for the opportunity
* FastAPI documentation & community
* Next.js team
