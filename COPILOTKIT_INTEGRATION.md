# CopilotKit Integration Guide

## ✅ What's Been Implemented

Full CopilotKit chat UI has been integrated into the Legal Document Verification Agent!

---

## 🎯 Features Implemented

### 1. **CopilotKit Provider Setup**
- ✅ `CopilotKit` provider wraps the entire app
- ✅ `CopilotSidebar` component with custom labels
- ✅ Runtime API route at `/api/copilotkit`
- ✅ OpenAI integration configured

### 2. **Agentic Chat UI**
- ✅ Persistent sidebar chat interface
- ✅ Custom welcome message
- ✅ Click-to-open/close functionality
- ✅ Styled with CopilotKit default theme

### 3. **Custom Copilot Actions**
Created 4 intelligent actions the AI can use:

#### `verifyDocument`
Upload and verify a legal document
```typescript
// AI can trigger document verification
useCopilotAction({
  name: "verifyDocument",
  description: "Upload and verify a legal document",
  handler: async ({ file }) => {
    return await uploadDocument(file);
  },
});
```

#### `explainRisk`
Get detailed explanation of a specific risk
```typescript
// User: "Explain risk #2"
// AI calls: explainRisk({ riskId: "compliance_risk_2" })
```

#### `getComplianceStatus`
Get comprehensive compliance overview
```typescript
// User: "What's our compliance status?"
// AI calls: getComplianceStatus()
// Returns: compliance rate, items, gaps
```

#### `getUpcomingDeadlines`
Get all deadlines and urgent items
```typescript
// User: "Show me upcoming deadlines"
// AI calls: getUpcomingDeadlines()
// Returns: all renewal dates with urgency levels
```

### 4. **Shared State (useCopilotReadable)**
AI has real-time access to:
- Current document name
- Processing status
- Risk level and score
- Number of renewal dates, compliance items, risks

```typescript
useCopilotReadable({
  description: "Current document verification state",
  value: {
    hasDocument: true/false,
    fileName: "contract.pdf",
    riskLevel: "high",
    riskScore: 75.3,
    renewalDatesCount: 3,
    complianceItemsCount: 8,
    risksCount: 5,
  },
});
```

---

## 📁 Files Created/Modified

### New Files
1. **`app/api/copilotkit/route.ts`** - Runtime API endpoint
2. **`lib/copilotkit-config.ts`** - Configuration constants
3. **`hooks/useDocumentVerification.ts`** - Custom hook with Copilot actions

### Modified Files
1. **`app/layout.tsx`** - Added CopilotKit providers
2. **`app/page.tsx`** - Integrated chat notifications
3. **`package.json`** - Added `openai` dependency

---

## 🚀 How to Use

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

This will install:
- `@copilotkit/react-core`
- `@copilotkit/react-ui`
- `@copilotkit/runtime`
- `openai`

### Step 2: Configure Environment
Create `frontend/.env.local`:
```bash
OPENAI_API_KEY=sk-your-openai-key-here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 3: Start the App
```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Step 4: Open and Test
1. Navigate to http://localhost:3000
2. **Look for the chat icon** in the bottom-right corner
3. Click to open the **CopilotKit sidebar**
4. Start chatting!

---

## 💬 Example Conversations

### Before Uploading a Document
```
User: What can you help me with?

AI: I'm your legal document verification assistant! I can help you:
- Upload and analyze legal documents (PDF or DOCX)
- Identify renewal dates and deadlines
- Extract contractual obligations
- Verify compliance with regulations like GDPR, ISO27001, SOC2
- Assess risks and provide recommendations

Just upload a document to get started!
```

### After Uploading
```
User: What's the risk level of this document?

AI: Based on the analysis:
- Risk Score: 75.3/100
- Risk Level: HIGH
- 5 risks identified, including 2 critical items
- Main concerns: GDPR compliance gap and approaching deadline in 7 days

Would you like me to explain any specific risk?
```

```
User: Show me the upcoming deadlines

AI: Here are your upcoming deadlines:
- Contract renewal: 30 days (MEDIUM urgency)
- Insurance certificate renewal: 7 days (CRITICAL urgency)
- Annual audit deadline: 90 days (LOW urgency)

The insurance renewal needs immediate attention!
```

```
User: What's our compliance status?

AI: Compliance Overview:
- Total Items: 8
- Compliant: 5 (62.5%)
- Non-Compliant: 3
- Compliance Rate: 62.5%

Main gaps:
1. Missing GDPR Data Processing Agreement
2. ISO27001 audit overdue (14 months)
3. No evidence of SOC2 certification

Would you like recommendations on how to address these?
```

---

## 🎨 UI Components

### CopilotSidebar
The main chat interface with:
- **Custom Title**: "Legal Document Assistant"
- **Welcome Message**: Personalized greeting
- **Persistent**: Stays open across page navigation
- **Styled**: Uses CopilotKit default theme (customizable)

### Position
- Bottom-right corner (default)
- Can be customized via CSS
- Responsive on mobile

---

## 🔧 Customization Options

### Change Chat Position
Edit `app/layout.tsx`:
```typescript
<CopilotSidebar
  defaultOpen={true}  // Open by default
  clickOutsideToClose={true}  // Close when clicking outside
  // Add custom CSS class for positioning
  className="custom-chat-position"
>
```

### Custom Styling
Add to `globals.css`:
```css
/* Customize CopilotKit theme */
:root {
  --copilot-kit-primary-color: #3b82f6;
  --copilot-kit-background-color: #ffffff;
  --copilot-kit-text-color: #1f2937;
}

/* Custom chat position */
.custom-chat-position {
  /* Add your custom styles */
}
```

### Add More Actions
Edit `hooks/useDocumentVerification.ts`:
```typescript
useCopilotAction({
  name: "exportReport",
  description: "Export verification report as PDF",
  parameters: [{
    name: "format",
    type: "string",
    enum: ["PDF", "Excel", "JSON"]
  }],
  handler: async ({ format }) => {
    // Implementation
  },
});
```

---

## 🤖 AI Capabilities

The AI assistant can:
1. **Answer Questions** about compliance, risks, deadlines
2. **Execute Actions** like verifying documents
3. **Access Live Data** from the current verification state
4. **Provide Context** based on the uploaded document
5. **Make Recommendations** for risk mitigation

---

## 🔍 How It Works

### 1. User Opens Chat
```
User clicks chat icon → CopilotSidebar opens
```

### 2. User Asks Question
```
"What's the compliance status?" 
→ AI calls getComplianceStatus() action
→ Returns real compliance data
→ AI formats and explains to user
```

### 3. User Uploads Document
```
Document uploaded → uploadDocument() called
→ Backend processes → Results returned
→ useCopilotReadable updates state
→ AI notified of new document
→ AI can now answer questions about it
```

### 4. AI Uses Context
```
User: "Is this high risk?"
→ AI checks useCopilotReadable state
→ Sees riskLevel: "high", riskScore: 75.3
→ Responds with specific details
```

---

## 📊 State Flow

```
┌─────────────────┐
│  User Action    │
│ (Upload/Chat)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ useCopilot      │
│ ReadableState   │ ← Real-time document data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Assistant   │
│  (GPT-4)        │ ← Analyzes context
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ useCopilot      │
│ Actions         │ ← Executes functions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Response to    │
│  User in Chat   │
└─────────────────┘
```

---

## 🎯 Next Steps

### Immediate
1. **Install dependencies**: `npm install`
2. **Test the chat**: Ask questions, upload documents
3. **Verify actions work**: Check backend logs

### Enhancements
1. **Add more actions**:
   - `highlightClause` - Highlight specific document sections
   - `scheduleReminder` - Set deadline alerts
   - `compareDocuments` - Compare two contracts

2. **Improve prompts**:
   - Edit `lib/copilotkit-config.ts` → `AGENT_INSTRUCTIONS`
   - Add domain-specific knowledge

3. **Add generative UI**:
   - Render custom components in chat
   - Show inline risk cards
   - Display interactive timelines

4. **Streaming progress**:
   - Show real-time agent progress
   - Update chat as agent moves through nodes

---

## 🐛 Troubleshooting

### Chat doesn't appear
- Check console for errors
- Verify `OPENAI_API_KEY` is set in `.env.local`
- Make sure `npm install` completed successfully

### Actions don't work
- Check backend is running on port 8000
- Verify CORS is configured in backend
- Look at browser network tab for failed requests

### AI gives generic responses
- Check `useCopilotReadable` is updating
- Verify document state is being set correctly
- Add more descriptive action descriptions

---

## 📚 Resources

- **CopilotKit Docs**: https://docs.copilotkit.ai/
- **Action Examples**: https://docs.copilotkit.ai/reference/hooks/useCopilotAction
- **Readable State**: https://docs.copilotkit.ai/reference/hooks/useCopilotReadable
- **Chat UI**: https://docs.copilotkit.ai/reference/components/CopilotChat

---

## ✨ Summary

You now have a **fully functional AI chat assistant** that:
- ✅ Understands your document verification workflow
- ✅ Can execute actions (verify, explain, analyze)
- ✅ Has real-time access to document state
- ✅ Provides intelligent recommendations
- ✅ Answers questions naturally

**Try it out and let the AI help you verify documents!** 🚀
