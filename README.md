# kpop-universe

# Team - K-Pop Universe – Fan Community Platform

| Partner 1 | Partner 2 | Partner 3 | Project |
|---|---|---|---|
| Aryan | Harsita | Kaif | K-Pop Universe – Fan Community Platform |

## 1. Who is doing what

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | | | | | |
| Day 1 | | | | | |
| Day 1 | | | | | |
| Day 2 | | | | | |
| Day 2 | | | | | |
| Day 2 | | | | | |
| Day 3 | | | | | |
| Day 3 | | | | | |
| Day 3 | | | | | |

## 2. User roles 

| Role | Responsibilities |
|---|---|
| Admin | Manage organizers, users and platform moderation |
| Organizer | Manage artists, fan events and community activities |
| Fan | Create fan clubs, publish posts, vote and participate in events |

New registrations receive the **fan** role by default. Only admins can create organizer accounts.

## 3. API contract 

Backend runs on **port 8001**. Methods, paths and bodies below are our team's decisions.

### Authentication APIs (3)

| # | What it does | Method | Path | Request body | Success code |
|---|---|---|---|---|---|
| A1 | Register a new account (role = fan) | POST | `/auth/register` | `{ username, email, password }` | 200 |
| A2 | Login and generate access and refresh tokens | POST | `/auth/login` | `{ email, password }` | 200 |
| A3 | Generate a new access token | POST | `/auth/refresh` | `{ refresh_token }` | 200 |

### Project-specific APIs (15)

| # | What it does | Method | Path | Request body | Access | Success code |
|---|---|---|---|---|---|---|
| E1 | Create an organizer account | POST | `/admin/organizers` | `{ username, email, password }` | Admin | 200 |
| E2 | Add an artist or group | POST | `/artists` | `{ name, description, category }` | Organizer | 200 |
| E3 | Get all artists and groups | GET | `/artists` | — | All | 200 |
| E4 | Get details of one artist or group | GET | `/artists/{artist_id}` | — | All | 200 |
| E5 | Create a fan club | POST | `/fanclubs` | `{ name, artist_id }` | Fan | 200 |
| E6 | Get all available fan clubs | GET | `/fanclubs` | — | All | 200 |
| E7 | Join a fan club | POST | `/fanclubs/{club_id}/join` | — | Fan | 200 |
| E8 | Create a community post | POST | `/posts` | `{ text, image_url (optional) }` | Fan | 200 |
| E9 | Get posts from the community feed | GET | `/posts` | — | All | 200 |
| E10 | Like or unlike a post | POST | `/posts/{post_id}/like` | — | Fan | 200 |
| E11 | Create a poll for an artist or group | POST | `/polls` | `{ artist_id, question, options[], opens_at, closes_at }` | Organizer | 200 |
| E12 | Vote in a poll | POST | `/polls/{poll_id}/vote` | `{ option_id }` | Fan | 200 |
| E13 | Get poll results | GET | `/polls/{poll_id}/results` | — | All | 200 |
| E14 | Create a fan event | POST | `/events` | `{ name, date, venue, participant_limit }` | Organizer | 200 |
| E15 | Register for a fan event | POST | `/events/{event_id}/register` | — | Fan | 200 |

All protected endpoints take the JWT access token in the `Authorization: Bearer` header.

## 4. Business rules the API must check 

| Rule | Proposed status |
|---|---|
| Non-admin trying to create an organizer | 403 |
| Wrong role for a protected endpoint | 403 |
| Invalid or expired access / refresh token | 401 |
| A fan joining the same fan club twice | 409 |
| A fan liking the same post twice | 409 |
| A fan voting more than once in a poll | 409 |
| Voting outside the poll's opening/closing dates | 400 |
| The same fan registering for the same event twice | 409 |
| Registering for an event that is full | 400 |
| Missing or empty required fields | 422 |

Every error returns a meaningful message. Admins must be able to manage inappropriate users and community content.

## 5. Endpoint tracker

Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Who |
|---|---|---|---|---|
| A1 | POST /auth/register | ⬜ | ⬜ | |
| A2 | POST /auth/login | ⬜ | ⬜ | |
| A3 | POST /auth/refresh | ⬜ | ⬜ | |
| E1 | POST /admin/organizers | ⬜ | ⬜ | |
| E2 | POST /artists | ⬜ | ⬜ | |
| E3 | GET /artists | ⬜ | ⬜ | |
| E4 | GET /artists/{artist_id} | ⬜ | ⬜ | |
| E5 | POST /fanclubs | ⬜ | ⬜ | |
| E6 | GET /fanclubs | ⬜ | ⬜ | |
| E7 | POST /fanclubs/{club_id}/join | ⬜ | ⬜ | |
| E8 | POST /posts | ⬜ | ⬜ | |
| E9 | GET /posts | ⬜ | ⬜ | |
| E10 | POST /posts/{post_id}/like | ⬜ | ⬜ | |
| E11 | POST /polls | ⬜ | ⬜ | |
| E12 | POST /polls/{poll_id}/vote | ⬜ | ⬜ | |
| E13 | GET /polls/{poll_id}/results | ⬜ | ⬜ | |
| E14 | POST /events | ⬜ | ⬜ | |
| E15 | POST /events/{event_id}/register | ⬜ | ⬜ | |

## 6. Setup & deployment tracker

| Item | Status | Who |
|---|---|---|
| GitHub repo + collaborators + README | ⬜ | |
| Database schema design (tables, fields, relationships) | ⬜ | |
| Dockerfile | ⬜ | |
| Docker image built & verified locally | ⬜ | |
| Image pushed to Docker Hub | ⬜ | |
| GitHub Actions workflow (build → Docker Hub → EC2) | ⬜ | |
| EC2 instance + Docker installed + security group | ⬜ | |
| Persistent SQLite directory mounted on EC2 | ⬜ | |
| Public API URL working after auto-deploy | ⬜ | |

Credentials (Docker Hub, EC2 SSH) live in **GitHub Actions Secrets** — never in the repo.

## 7. Tech Stack & Deployment

- **Backend:** Python, FastAPI, Pydantic, SQLite, SQLAlchemy, PyJWT, argon2-cffi
- **Auth:** JWT access + refresh tokens, role-based access control (Admin / Organizer / Fan)
- **Deployment:** Docker (no Compose), GitHub Actions CI/CD, AWS EC2
- **Database:** SQLite file, persisted outside the container via a mounted directory on EC2

## 8. How to Run Locally

### Backend (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Swagger UI: http://127.0.0.1:8001/docs

### Docker

```powershell
docker build -t kpop-universe .
docker run -p 8001:8001 kpop-universe
```

Verify the API works through the container at http://127.0.0.1:8001/docs
