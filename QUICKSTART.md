# Quick Start Guide

Get the Legal Document Verification Agent running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key (or Anthropic)

---

## Step 1: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

---

## Step 2: Setup Frontend

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
copy .env.example .env.local  # Windows
# cp .env.example .env.local  # Mac/Linux

# No need to edit if backend runs on localhost:8000
```

---

## Step 3: Start the Application

### Terminal 1 - Backend

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

uvicorn app.main:app --reload
```

✅ Backend running at http://localhost:8000  
📚 API docs at http://localhost:8000/docs

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend running at http://localhost:3000

---

## Step 4: Test It!

1. Open browser to http://localhost:3000
2. Click "Click to upload" and select a PDF or DOCX file
3. Click "Verify Document"
4. View the risk assessment and recommendations!

---

## What's Happening?

When you upload a document, the system:

1. **Ingests** - Extracts text from PDF/DOCX
2. **Classifies** - Identifies document type
3. **Extracts** - Finds renewal dates, obligations, compliance requirements
4. **Verifies** - Checks against compliance rules
5. **Assesses** - Calculates risk scores
6. **Reviews** - (Optional) Human-in-the-loop checkpoint
7. **Reports** - Generates comprehensive verification report

---

## Sample Test Document

Don't have a legal document handy? Create a simple test:

**test-contract.txt**
```
SERVICE AGREEMENT

This agreement is between Party A and Party B.

Effective Date: January 1, 2024
Expiration Date: December 31, 2024

OBLIGATIONS:
- Party A shall provide monthly status reports
- Party B shall maintain insurance coverage
- Both parties must comply with GDPR regulations

RENEWAL:
Contract renews automatically unless notice given 30 days prior to expiration.

ISO27001 certification required.
Annual security audit mandatory.
```

Save as PDF and upload!

---

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.11+)
- Verify virtual environment is activated
- Check .env file has OPENAI_API_KEY

### Frontend won't start
- Check Node version: `node --version` (should be 18+)
- Delete node_modules and run `npm install` again
- Check port 3000 isn't already in use

### Upload fails
- Check backend is running on port 8000
- Check file is PDF or DOCX
- Check file size < 50MB
- Look at backend logs for errors

### No results returned
- Verify OpenAI API key is valid and has credits
- Check backend logs: `uvicorn app.main:app --reload --log-level debug`

---

## Next Steps

Once it's running:

1. **Try different documents** - Contracts, licenses, agreements
2. **Check the API docs** - http://localhost:8000/docs
3. **Review the code** - See how the LangGraph agent works
4. **Customize** - Modify compliance rules in `backend/app/agent/nodes/compliance.py`
5. **Extend** - Add new risk categories or compliance checks

---

## Development Tips

### Backend Hot Reload
The `--reload` flag auto-restarts when you modify Python files

### Frontend Hot Reload
Next.js auto-updates when you save changes to React components

### View Logs
- Backend: Terminal where uvicorn is running
- Frontend: Browser console + terminal

### API Testing
Use the Swagger UI at http://localhost:8000/docs to test endpoints directly

---

## Architecture Quick Reference

```
┌─────────────┐
│   Frontend  │ Next.js + React
│  (Port 3000)│
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │ FastAPI
│  (Port 8000)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  LangGraph  │ Agent with 7 nodes:
│   Agent     │ 1. Ingestion
└─────────────┘ 2. Classification
       │        3. Extraction
       │        4. Compliance
       │        5. Risk Assessment
       ▼        6. HITL (optional)
┌─────────────┐ 7. Report Generation
│  OpenAI/    │
│  Anthropic  │
└─────────────┘
```

---

## Need Help?

- Check the `architecture.md` for detailed system design
- Review `PROJECT_STATUS.md` for implementation status
- Look at code comments in agent nodes for logic details

Happy document verifying! ⚖️
