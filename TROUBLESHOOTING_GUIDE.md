# Troubleshooting Guide

## 🔴 Issue 1: "Failed to Fetch" When Uploading Document

### Problem
When you click "Verify Document", you get a "Failed to fetch" error.

### Root Causes
1. **Backend not running** on port 8000
2. **CORS blocking** the request
3. **Missing OpenAI API key** in backend
4. **Wrong API URL** in frontend

### Solution Steps

#### Step 1: Check Backend is Running
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test**: Open http://localhost:8000 in browser - should show:
```json
{
  "status": "healthy",
  "service": "Legal Document Verification Agent",
  "version": "0.1.0"
}
```

#### Step 2: Add OpenAI API Key to Backend
Edit `backend/.env`:
```bash
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```

Replace `sk-proj-YOUR_ACTUAL_KEY_HERE` with your real OpenAI key.

#### Step 3: Check Backend Logs
When you try to upload, look at the backend terminal. You should see:
```
INFO:     127.0.0.1:xxxxx - "POST /api/v1/agent/verify-document HTTP/1.1" 200 OK
```

If you see errors, they'll appear here.

#### Step 4: Test Backend Directly
Open a new terminal and test with curl:

**Windows PowerShell:**
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET
$response.Content
```

**Should return:**
```json
{"status":"healthy","checks":{"api":"ok"}}
```

---

## 🔴 Issue 2: CopilotKit Chat Not Working

### Problem
Chat icon doesn't appear or chat doesn't respond.

### Root Causes
1. **Missing `.env.local`** file in frontend
2. **Missing OpenAI API key** for chat
3. **Dependencies not installed**
4. **Layout.tsx issues**

### Solution Steps

#### Step 1: Create `.env.local` File
Create file at: `frontend/.env.local`

```bash
# YOUR OPENAI API KEY (REQUIRED!)
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**⚠️ CRITICAL**: Replace `sk-proj-YOUR_ACTUAL_KEY_HERE` with your actual OpenAI API key!

#### Step 2: Install Missing Dependencies
```bash
cd frontend
npm install
```

This installs:
- `@copilotkit/react-core`
- `@copilotkit/react-ui`
- `@copilotkit/runtime`
- `openai` package

#### Step 3: Verify Layout.tsx
The file should have CopilotKit providers. Check `frontend/app/layout.tsx` contains:

```typescript
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
```

#### Step 4: Restart Frontend
After creating `.env.local`:
```bash
cd frontend
npm run dev
```

**⚠️ Important**: You MUST restart the dev server after creating/editing `.env.local`

#### Step 5: Check Browser Console
1. Open http://localhost:3000
2. Press F12 (Developer Tools)
3. Go to "Console" tab
4. Look for errors related to CopilotKit

Common errors:
- `OPENAI_API_KEY is not defined` → Check `.env.local` exists
- `Failed to fetch /api/copilotkit` → Check API route exists
- CORS errors → Backend CORS issue

---

## 🔧 Quick Fix Checklist

### Backend Issues
- [ ] Backend running on port 8000
- [ ] `backend/.env` file exists
- [ ] `OPENAI_API_KEY` in `backend/.env` is valid
- [ ] Backend shows no errors in terminal
- [ ] Can access http://localhost:8000/health

### Frontend Issues
- [ ] `frontend/.env.local` file exists
- [ ] `OPENAI_API_KEY` in `frontend/.env.local` is valid
- [ ] Ran `npm install` in frontend directory
- [ ] Frontend restarted after creating `.env.local`
- [ ] Can access http://localhost:3000
- [ ] No errors in browser console

---

## 📝 Step-by-Step Setup (Fresh Start)

### 1. Backend Setup
```bash
cd backend

# Create/edit .env file
# Add: OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE

# Install dependencies (if not done)
pip install -r requirements.txt

# Start server
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
# Add these lines:
#   OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
#   NEXT_PUBLIC_API_URL=http://localhost:8000

# Start server
npm run dev
```

### 3. Verify Setup
Open these in browser:
- http://localhost:8000/health → Should work
- http://localhost:3000 → Should show UI
- Look for chat icon in bottom-right corner

---

## 🔍 Detailed Diagnostics

### Check 1: Backend is Accessible
```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status":"healthy","checks":{"api":"ok"}}
```

### Check 2: CopilotKit API Route Works
```bash
curl http://localhost:3000/api/copilotkit
```

Expected: Should NOT return 404

### Check 3: OpenAI Key is Valid
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-proj-YOUR_KEY_HERE"
```

Expected: List of models (not error)

### Check 4: Dependencies Installed
```bash
cd frontend
npm list @copilotkit/react-core
```

Expected: Shows version number (not "missing")

---

## 🐛 Common Error Messages

### Error: "Failed to fetch"
**Cause**: Backend not running or CORS issue  
**Fix**: Start backend, check CORS in `app/config.py`

### Error: "OPENAI_API_KEY is not defined"
**Cause**: Missing `.env.local` or wrong variable name  
**Fix**: Create `frontend/.env.local` with correct key

### Error: "Network request failed"
**Cause**: Wrong API URL  
**Fix**: Check `NEXT_PUBLIC_API_URL` in `.env.local`

### Error: "Module not found: @copilotkit/react-core"
**Cause**: Dependencies not installed  
**Fix**: Run `npm install` in frontend directory

### Error: "Cannot read property 'handleRequest' of undefined"
**Cause**: CopilotKit runtime not initialized  
**Fix**: Check `app/api/copilotkit/route.ts` exists

---

## 📊 Verification Commands

Run these to verify everything is working:

```bash
# Check backend running
curl http://localhost:8000

# Check frontend running
curl http://localhost:3000

# Check environment files exist
ls backend\.env
ls frontend\.env.local

# Check dependencies
cd frontend && npm list @copilotkit/react-core
cd backend && pip list | findstr langchain
```

---

## 🎯 Still Not Working?

### Get Backend Logs
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --log-level debug
```

Try uploading document and copy the error message.

### Get Frontend Logs
1. Open http://localhost:3000
2. Open Developer Tools (F12)
3. Go to Console tab
4. Try uploading document
5. Copy any red error messages

### Check File Locations
```bash
# Should all exist:
backend/.env
backend/app/main.py
frontend/.env.local
frontend/app/api/copilotkit/route.ts
frontend/lib/copilotkit-config.ts
```

---

## ✅ Success Indicators

You'll know it's working when:

1. **Backend**: Terminal shows "Application startup complete"
2. **Frontend**: Terminal shows "Ready in X ms"
3. **Browser**: http://localhost:3000 loads without errors
4. **Chat Icon**: Visible in bottom-right corner
5. **Upload**: Document processes without "failed to fetch"
6. **Chat**: AI responds to messages

---

## 🔑 Where to Put API Keys (Summary)

### OpenAI API Key Goes in TWO Places:

**1. Backend** (`backend/.env`):
```bash
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```
→ Used for: Document analysis, classification, extraction

**2. Frontend** (`frontend/.env.local`):
```bash
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```
→ Used for: CopilotKit chat, AI responses

**⚠️ Both need the SAME key! Use your real OpenAI API key in both files.**

---

## 📞 Quick Reference

| Issue | File to Check | What to Add |
|-------|--------------|-------------|
| Upload fails | `backend/.env` | `OPENAI_API_KEY=sk-...` |
| Chat not working | `frontend/.env.local` | `OPENAI_API_KEY=sk-...` |
| CORS error | `backend/app/config.py` | Check ALLOWED_ORIGINS |
| Dependencies missing | `frontend/` | Run `npm install` |
| Backend not starting | `backend/` | Check Python version 3.11+ |

---

**Remember**: After creating or editing `.env` or `.env.local` files, you MUST restart the servers!
