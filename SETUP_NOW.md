# 🚀 Setup NOW - Fix Your Issues

## Quick Fix for Your Two Problems

### ❌ Problem 1: Upload Returns "Failed to Fetch"
### ❌ Problem 2: CopilotKit Chat Not Working

Both are **missing API key** issues! Here's the fix:

---

## ⚡ 5-Minute Fix

### Step 1: Add OpenAI Key to Backend
1. Open file: `backend/.env`
2. Find line: `OPENAI_API_KEY=sk-your-openai-key-here`
3. Replace with your **actual** OpenAI API key:
```bash
OPENAI_API_KEY=sk-proj-AbCd1234YourActualKeyHere
```
4. Save file

### Step 2: Add OpenAI Key to Frontend
1. File should already exist: `frontend/.env.local`
2. Open it and add:
```bash
OPENAI_API_KEY=sk-proj-AbCd1234YourActualKeyHere
NEXT_PUBLIC_API_URL=http://localhost:8000
```
3. **Use the SAME key as backend!**
4. Save file

### Step 3: Install Frontend Dependencies
```bash
cd frontend
npm install
```

Wait for it to complete...

### Step 4: Restart Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 5: Test It!
1. Open http://localhost:3000
2. Upload a document
3. Click "Verify Document"
4. Should work now! ✅
5. Look for chat icon bottom-right ↘️

---

## 🔑 Where is YOUR OpenAI API Key?

If you don't have one:
1. Go to https://platform.openai.com/api-keys
2. Log in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)
5. Paste it in **both** `.env` files

---

## ✅ Verification Steps

After setup, verify:

### Backend Check:
```bash
# Open browser to:
http://localhost:8000/health
```
Should show: `{"status":"healthy",...}`

### Frontend Check:
```bash
# Open browser to:
http://localhost:3000
```
Should show the upload interface

### Upload Check:
1. Select a PDF or DOCX file
2. Click "Verify Document"
3. Should see processing, then results (not "failed to fetch")

### Chat Check:
1. Look for chat bubble icon in bottom-right corner
2. Click it to open sidebar
3. Type: "Hello"
4. Should get a response from AI

---

## 🐛 Still Not Working?

### If Upload Still Fails:

**Check backend terminal** - Do you see errors?

Common errors:
```
ValueError: OPENAI_API_KEY not configured
```
→ Fix: Add key to `backend/.env`

```
Traceback... connection refused
```
→ Fix: Backend not running, restart it

### If Chat Still Doesn't Work:

**Check browser console** (Press F12):

Common errors:
```
OPENAI_API_KEY is not defined
```
→ Fix: Add key to `frontend/.env.local` and **restart frontend**

```
Failed to fetch /api/copilotkit
```
→ Fix: Run `npm install` again

---

## 📋 File Locations Summary

```
legal-doc-verification-agent/
├── backend/
│   └── .env                    ← PUT OPENAI KEY HERE (line 2)
└── frontend/
    └── .env.local              ← PUT OPENAI KEY HERE (create this file)
```

---

## 🎯 Exact Commands to Run

Copy and paste these in order:

```bash
# 1. Go to frontend
cd C:\Users\user\legal-doc-verification-agent\frontend

# 2. Install dependencies
npm install

# 3. Open .env.local in notepad
notepad .env.local

# Add these two lines (replace with your key):
#   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY
#   NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. Save and close notepad

# 5. Start frontend (keep this terminal open)
npm run dev
```

```bash
# In NEW TERMINAL:

# 1. Go to backend
cd C:\Users\user\legal-doc-verification-agent\backend

# 2. Open .env in notepad
notepad .env

# Edit line 2 to have your real API key:
#   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY

# 3. Save and close notepad

# 4. Activate venv and start backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

---

## 🎉 You're Done!

Open http://localhost:3000 and try:
1. Upload a document ✅
2. Click chat icon ✅
3. Ask AI a question ✅

Everything should work now!

---

## 💡 Pro Tip

Keep both terminal windows open side-by-side so you can see logs from both frontend and backend. This helps debug any issues.

---

**Need more help?** Check `TROUBLESHOOTING_GUIDE.md` for detailed diagnostics!
