# CloseZap AI - WhatsApp Sales Assistant Backend

An AI-powered backend service for managing WhatsApp leads with automated follow-ups.

## Features

- **Webhook Integration**: Receives WhatsApp messages via Twilio
- **AI Responses**: Generates human-like sales responses using OpenAI
- **Lead Management**: Full CRUD operations for leads
- **Automated Follow-ups**: Sends follow-up messages to inactive leads
- **PostgreSQL/SQLite**: Database support with automatic fallback

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuration and settings
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py          # SQLAlchemy base model
│   │   └── session.py       # Database session management
│   ├── models/
│   │   ├── __init__.py
│   │   └── lead.py          # Lead model and schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── leads.py         # Lead management endpoints
│   │   └── webhook.py       # WhatsApp webhook endpoint
│   └── services/
│       ├── __init__.py
│       ├── ai_service.py    # OpenAI integration
│       ├── lead_service.py  # Lead business logic
│       └── followup_service.py  # Automated follow-ups
├── requirements.txt
├── .env.example
├── run.py
└── README.md
```

## Requirements

- Python 3.10+
- PostgreSQL (optional, SQLite used by default)

## Installation

1. **Clone the repository and navigate to the backend directory:**

```bash
cd C:\Users\fehao\Documents\Workspace\closezap-ai\backend
```

2. **Create a virtual environment:**

```bash
python -m venv venv
```

3. **Activate the virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

5. **Configure environment variables:**

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-openai-api-key
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

## Running the Application

### Development mode:

```bash
python run.py
```

### Or with uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Webhook

- `POST /api/webhook` - Receive WhatsApp messages (Twilio webhook)

### Leads

- `GET /api/leads` - List all leads (with optional status filter)
- `GET /api/leads/{id}` - Get a specific lead
- `PATCH /api/leads/{id}` - Update a lead
- `DELETE /api/leads/{id}` - Delete a lead

### Health

- `GET /` - API information
- `GET /health` - Health check

## API Documentation

Once the server is running, access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Models

### Lead

| Field | Type | Description |
|-------|------|-------------|
| id | int | Auto-increment ID |
| name | string | Lead name (optional) |
| phone | string | Phone number (unique) |
| interest | text | Lead's interest area |
| status | enum | new, engaged, closed |
| last_message | text | Last conversation snippet |
| created_at | datetime | Creation timestamp |
| last_contact_at | datetime | Last contact timestamp |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| APP_NAME | Application name | CloseZap AI |
| DEBUG | Debug mode | true |
| DATABASE_URL | Database connection string | sqlite:///./closezap.db |
| OPENAI_API_KEY | OpenAI API key | - |
| TWILIO_ACCOUNT_SID | Twilio account SID | - |
| TWILIO_AUTH_TOKEN | Twilio auth token | - |
| TWILIO_PHONE_NUMBER | Twilio WhatsApp number | - |
| FOLLOWUP_ENABLED | Enable auto follow-ups | true |
| FOLLOWUP_INACTIVITY_HOURS | Hours before follow-up | 24 |
| FOLLOWUP_CHECK_INTERVAL_MINUTES | Check interval | 30 |

## Twilio Setup

1. Create a Twilio account at https://www.twilio.com
2. Purchase a phone number with WhatsApp capability
3. Configure the webhook URL in Twilio console:
   - URL: `https://your-domain.com/api/webhook`
   - Method: POST

## Testing with cURL

### Send a webhook message:

```bash
curl -X POST http://localhost:8000/api/webhook \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "From=whatsapp:+1234567890&Body=Hello, I'm interested in your services"
```

### Get leads:

```bash
curl http://localhost:8000/api/leads
```

### Update a lead:

```bash
curl -X PATCH http://localhost:8000/api/leads/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "status": "closed"}'
```

## License

MIT License