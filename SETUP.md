# Setup Guide

## Quick Start

### 1. Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- OpenAI API key or Anthropic API key

### 2. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
```

Edit `.env.local` and add your API keys:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
OPENAI_API_KEY=sk-your-key-here
```

Run the frontend:
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

### 3. Backend Setup

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your configuration:
```
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://user:pass@localhost:5432/legal_docs
```

Run the backend:
```bash
uvicorn app.main:app --reload
```

Backend API will be available at http://localhost:8000

API docs at http://localhost:8000/docs

## Project Structure

```
legal-doc-verification-agent/
├── frontend/          # Next.js + CopilotKit UI
├── backend/           # FastAPI + LangGraph agent
├── shared/            # Shared types
├── docs/              # Documentation
├── architecture.md    # System architecture
└── README.md          # Project overview
```

## Next Steps

1. Install dependencies: `npm install` (frontend) and `pip install -r requirements.txt` (backend)
2. Configure environment variables
3. Start both servers
4. Open http://localhost:3000 and test document upload

## Development Commands

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run linter

### Backend
- `uvicorn app.main:app --reload` - Start with auto-reload
- `pytest` - Run tests (when added)
- `python -m app.main` - Run directly

## Troubleshooting

### Frontend issues
- Clear `.next` folder: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

### Backend issues
- Recreate virtual environment
- Check Python version: `python --version` (should be 3.11+)
- Verify API keys in `.env`

## Database Setup (Optional)

If using PostgreSQL:
```bash
# Install PostgreSQL
# Create database
createdb legal_docs

# Run migrations (when added)
# alembic upgrade head
```

## Optional: Docker Setup

Coming soon - docker-compose.yml for easy deployment
