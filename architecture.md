# Legal Document Verification Agent - Architecture

## 🎯 System Overview

An AI-powered agent for legal operations clerks to verify documents for compliance, renewal dates, obligations, and risks using LangChain + CopilotKit (LangGraph).

---

## 🏗️ Technology Stack

### Frontend
- **Framework**: Next.js 15 + React + TypeScript
- **UI Library**: CopilotKit (AG-UI Protocol)
- **Document Viewer**: react-pdf
- **Charts**: recharts (for risk dashboards)
- **Timeline**: react-calendar-timeline (deadline tracking)
- **Styling**: Tailwind CSS

### Backend
- **Framework**: FastAPI (Python)
- **Agent Orchestration**: LangGraph
- **LLM Integration**: LangChain
- **Document Processing**:
  - PyPDF2 / pdfplumber (PDF extraction)
  - python-docx (Word documents)
  - Tesseract OCR / AWS Textract (image-based PDFs)
- **NLP**: spaCy (Named Entity Recognition)
- **Date Parsing**: python-dateutil
- **Data Validation**: Pydantic

### LLM Provider
- **Primary**: OpenAI GPT-4 / Anthropic Claude
- **Fallback**: OpenAI GPT-3.5-turbo (cost optimization)

### Database
- **Primary**: PostgreSQL (structured data)
- **Vector Store**: Chroma/Pinecone (compliance embeddings)
- **Cache**: Redis (LLM response caching)

### Protocol
- **AG-UI**: Agent-User Interaction Protocol (CopilotKit)
- **Streaming**: Server-Sent Events (SSE)

---

## 🧠 Agent Architecture (LangGraph State Machine)

### State Schema

```python
from typing import TypedDict, List, Optional, Dict
from datetime import datetime

class DocumentVerificationState(TypedDict):
    # Input
    document_file: str
    document_type: str
    user_id: str
    
    # Document Processing
    raw_text: str
    parsed_sections: List[Dict[str, str]]
    document_metadata: Dict[str, any]
    
    # Extraction Results
    renewal_dates: List[Dict]  
    # [{date: datetime, description: str, days_until: int, urgency: str}]
    
    obligations: List[Dict]
    # [{clause_id: str, requirement: str, party: str, status: str, deadline: Optional[datetime]}]
    
    compliance_items: List[Dict]
    # [{regulation: str, requirement: str, status: str, gap: Optional[str], severity: str}]
    
    # Risk Assessment
    risks: List[Dict]
    # [{id: str, category: str, severity: str, description: str, mitigation: str, score: float}]
    
    overall_risk_score: float  # 0-100
    risk_level: str  # "Critical" | "High" | "Medium" | "Low"
    
    # Human-in-the-Loop
    human_feedback: Optional[Dict]
    requires_review: bool
    review_items: List[str]
    
    # Output
    verification_report: Dict
    recommendations: List[str]
    status: str  # "processing" | "review_required" | "completed" | "error"
    error_message: Optional[str]
```

---

## 🔄 Agent Nodes (LangGraph)

### 1. Document Ingestion Node
**Purpose**: Accept and prepare document for processing

**Tasks**:
- Validate file format (PDF, DOCX, images)
- Extract raw text content
- Detect document encoding
- Handle OCR for scanned documents
- Extract embedded metadata

**Output**: `raw_text`, `document_metadata`

---

### 2. Document Classification Node
**Purpose**: Identify document type and structure

**Tasks**:
- Classify document type (contract, license, permit, agreement, policy, etc.)
- Identify parties involved
- Extract document ID/reference numbers
- Detect document sections (terms, obligations, exhibits)
- Parse document structure

**LLM Prompt Example**:
```
Analyze this legal document and classify:
1. Document Type: [contract/license/permit/agreement/other]
2. Parties: [list all parties]
3. Effective Date: [date]
4. Expiration Date: [date]
5. Document Sections: [list key sections]
```

**Output**: `document_type`, `parsed_sections`, `document_metadata`

---

### 3. Requirement Extraction Node
**Purpose**: Extract key dates, obligations, and requirements

**Tasks**:
- **Renewal Dates**: Find expiration, renewal deadlines, notice periods
- **Obligations**: Extract contractual commitments, deliverables, milestones
- **Compliance Requirements**: Identify regulatory requirements, certifications, reporting obligations

**Extraction Strategy**:
- Regex patterns for dates
- NER (Named Entity Recognition) for obligations
- LLM-based semantic extraction for implicit requirements

**Output**: `renewal_dates`, `obligations`, `compliance_items`

---

### 4. Compliance Verification Node
**Purpose**: Check requirements against compliance database

**Tasks**:
- Match extracted requirements to regulatory rules
- Identify missing compliance items
- Check for expired certifications
- Verify regulatory alignment
- Calculate days until deadlines

**Compliance Database**:
```python
# Example compliance rules structure
compliance_rules = {
    "GDPR": {
        "requirements": ["Data Processing Agreement", "Privacy Policy", "DPO Designation"],
        "renewal": "Annual",
        "penalty": "High"
    },
    "ISO27001": {
        "requirements": ["Security Policy", "Risk Assessment", "Audit Log"],
        "renewal": "Every 3 years",
        "penalty": "Medium"
    }
}
```

**Output**: Updated `compliance_items` with verification status

---

### 5. Risk Assessment Node
**Purpose**: Analyze compliance gaps and calculate risk scores

**Risk Scoring Formula**:
```python
risk_score = (
    (urgency_weight * time_criticality) +      # 0-40 points
    (severity_weight * obligation_impact) +     # 0-30 points
    (penalty_weight * regulatory_consequence)   # 0-30 points
)

# Risk Levels
# 0-25: Low
# 26-50: Medium
# 51-75: High
# 76-100: Critical
```

**Risk Categories**:
- **Deadline Risk**: Approaching or missed renewal dates
- **Compliance Risk**: Regulatory non-compliance
- **Contractual Risk**: Unmet obligations
- **Financial Risk**: Penalty exposure
- **Reputational Risk**: Public disclosure issues

**Output**: `risks`, `overall_risk_score`, `risk_level`

---

### 6. Human-in-the-Loop (HITL) Node
**Purpose**: Present findings to clerk for validation

**Review Triggers**:
- Critical risk detected (score > 75)
- Ambiguous clauses requiring interpretation
- Missing critical information
- Conflicting requirements
- User-requested review

**HITL Actions**:
- Display extracted data with document references
- Allow manual corrections
- Request clarification via chat
- Enable annotation and notes
- Provide approval/rejection workflow

**Output**: `human_feedback`, `requires_review` = False

---

### 7. Report Generation Node
**Purpose**: Create comprehensive verification report

**Report Sections**:
1. **Executive Summary**: Overall risk level, key findings
2. **Document Information**: Metadata, parties, dates
3. **Renewal Dates**: Calendar view with urgency indicators
4. **Obligations**: Checklist with status
5. **Compliance Analysis**: Requirements vs. actual status
6. **Risk Assessment**: Detailed risk breakdown with mitigation
7. **Recommendations**: Actionable next steps
8. **Appendix**: Supporting evidence, document excerpts

**Export Formats**: PDF, Excel, JSON

**Output**: `verification_report`, `recommendations`

---

## 🔄 Workflow Design

```mermaid
graph TD
    A[Document Upload UI] --> B[Ingestion Node]
    B --> C[Classification Node]
    C --> D[Extraction Node]
    D --> E[Compliance Verification Node]
    E --> F[Risk Assessment Node]
    F --> G{Risk Level?}
    G -->|Critical/High| H[HITL Review Node]
    G -->|Medium/Low| I[Report Generation Node]
    H --> J{User Action}
    J -->|Approved| I
    J -->|Revise| D
    J -->|Reject| K[Error Handling]
    I --> L[Display Report UI]
    K --> L
```

---

## 🎨 Frontend Features (CopilotKit)

### 1. Agentic Chat UI
**Components**:
- `<CopilotChat />` - Main chat interface
- Streaming responses with agent status
- Context-aware suggestions

**Use Cases**:
- "What are the renewal dates in this contract?"
- "Highlight all compliance requirements"
- "What's the risk level for this document?"

---

### 2. Generative UI Components

#### Document Viewer
```tsx
<DocumentViewer 
  file={documentFile}
  highlights={extractedClauses}
  annotations={userNotes}
/>
```

#### Risk Dashboard
```tsx
<RiskDashboard 
  riskScore={overallRiskScore}
  riskBreakdown={risks}
  complianceStatus={complianceItems}
/>
```

#### Timeline View
```tsx
<DeadlineTimeline 
  renewalDates={renewalDates}
  currentDate={new Date()}
  highlightUrgent={true}
/>
```

#### Compliance Checklist
```tsx
<ComplianceChecklist 
  items={complianceItems}
  onItemCheck={handleItemCheck}
  editable={true}
/>
```

---

### 3. Human-in-the-Loop Integration

**HITL Checkpoint UI**:
```tsx
<CopilotSidebar>
  <HITLReviewPanel
    findings={agentFindings}
    onApprove={handleApprove}
    onRevise={handleRevise}
    onReject={handleReject}
  />
</CopilotSidebar>
```

**Features**:
- Pause agent at review checkpoints
- Inline editing of extracted data
- Annotation tools for document sections
- Approval workflow with comments

---

### 4. Shared State Management

**Frontend State**:
```tsx
const { state, updateState } = useCopilotReadable({
  description: "Document verification state",
  value: {
    currentDocument: documentFile,
    extractedData: {
      renewalDates,
      obligations,
      complianceItems
    },
    riskAssessment: {
      score: overallRiskScore,
      level: riskLevel,
      risks
    },
    userAnnotations: annotations
  }
});
```

**Real-time Sync**:
- Agent updates → UI reflects changes instantly
- User edits → Agent state updated via shared state
- Progress indicators during processing

---

### 5. Frontend Actions

```tsx
useCopilotAction({
  name: "highlightClause",
  description: "Highlight a specific clause in the document",
  parameters: [{
    name: "clauseId",
    type: "string",
    required: true
  }],
  handler: async ({ clauseId }) => {
    // Highlight logic
  }
});

useCopilotAction({
  name: "updateRiskLevel",
  description: "Update risk level for a specific item",
  parameters: [{
    name: "riskId",
    type: "string"
  }, {
    name: "newLevel",
    type: "string",
    enum: ["Critical", "High", "Medium", "Low"]
  }],
  handler: async ({ riskId, newLevel }) => {
    // Update logic
  }
});

useCopilotAction({
  name: "exportReport",
  description: "Export verification report",
  parameters: [{
    name: "format",
    type: "string",
    enum: ["PDF", "Excel", "JSON"]
  }],
  handler: async ({ format }) => {
    // Export logic
  }
});
```

---

## 📁 Project Structure

```
legal-doc-verification-agent/
├── frontend/                  # Next.js application
│   ├── app/
│   │   ├── page.tsx          # Main page
│   │   ├── layout.tsx
│   │   └── api/
│   │       └── copilotkit/   # CopilotKit API routes
│   ├── components/
│   │   ├── DocumentViewer.tsx
│   │   ├── RiskDashboard.tsx
│   │   ├── DeadlineTimeline.tsx
│   │   ├── ComplianceChecklist.tsx
│   │   └── HITLReviewPanel.tsx
│   ├── hooks/
│   │   ├── useCopilotActions.ts
│   │   └── useDocumentState.ts
│   ├── lib/
│   │   └── copilotkit-config.ts
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Configuration
│   │   └── api/
│   │       └── routes/
│   │           └── agent.py  # Agent API endpoints
│   ├── agent/
│   │   ├── graph.py          # LangGraph definition
│   │   ├── state.py          # State schema
│   │   └── nodes/
│   │       ├── ingestion.py
│   │       ├── classification.py
│   │       ├── extraction.py
│   │       ├── compliance.py
│   │       ├── risk_assessment.py
│   │       ├── hitl.py
│   │       └── report.py
│   ├── services/
│   │   ├── document_processor.py
│   │   ├── llm_service.py
│   │   └── compliance_db.py
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   ├── utils/
│   │   ├── date_parser.py
│   │   └── risk_calculator.py
│   ├── requirements.txt
│   └── pyproject.toml
│
├── shared/
│   └── types/                # Shared TypeScript types
│
├── docs/
│   └── architecture.md       # This file
│
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml        # Optional: containerization
```

---

## 🔧 Environment Variables

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_COPILOTKIT_PUBLIC_KEY=your_public_key
```

### Backend (.env)
```bash
# LLM
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/legal_docs
REDIS_URL=redis://localhost:6379

# OCR (optional)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1

# App
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## 🛠️ Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [x] Setup Next.js project with CopilotKit
- [ ] Setup FastAPI backend with LangGraph
- [ ] Create basic document upload UI
- [ ] Implement document text extraction (PDF)
- [ ] Setup LangGraph state schema

### Phase 2: Core Agent (Week 2-3)
- [ ] Build document classification node
- [ ] Implement extraction logic (dates, obligations)
- [ ] Create compliance verification node
- [ ] Setup compliance rules database
- [ ] Test agent workflow end-to-end

### Phase 3: Risk Assessment (Week 4)
- [ ] Design risk scoring algorithm
- [ ] Implement risk categorization
- [ ] Create risk mitigation recommendations
- [ ] Build risk dashboard UI

### Phase 4: UI Integration (Week 5)
- [ ] Integrate AG-UI protocol
- [ ] Build generative UI components
- [ ] Implement HITL checkpoints
- [ ] Add frontend actions
- [ ] Setup shared state sync

### Phase 5: Testing & Polish (Week 6)
- [ ] Test with sample legal documents
- [ ] Tune LLM prompts for accuracy
- [ ] Optimize performance (caching, async)
- [ ] Add error handling & logging
- [ ] Create user documentation

---

## 🎯 Success Metrics

### Accuracy
- **Date Extraction**: >95% accuracy
- **Obligation Detection**: >90% recall
- **Risk Assessment**: <10% false positives

### Performance
- **Processing Speed**: <2 minutes for 20-page document
- **Review Time**: Clerk can validate in <5 minutes
- **Uptime**: 99.5% availability

### User Experience
- **HITL Efficiency**: <3 review checkpoints per document
- **Report Clarity**: 4.5/5 user satisfaction
- **Error Rate**: <5% documents requiring re-processing

---

## 🔒 Security Considerations

1. **Document Storage**: Encrypt at rest (AES-256)
2. **Data Transmission**: TLS 1.3 for all API calls
3. **Access Control**: Role-based authentication (clerk/admin)
4. **PII Protection**: Redact sensitive information before LLM processing
5. **Audit Logging**: Track all document access and modifications
6. **Compliance**: GDPR, SOC 2 compliance for document handling

---

## 🚀 Future Enhancements

### Phase 2 Features
- **Multi-document Analysis**: Compare related contracts
- **Version Tracking**: Track document amendments
- **Alert System**: Automated deadline reminders
- **Workflow Integration**: Jira/ServiceNow ticketing
- **Mobile App**: On-the-go document verification

### Advanced Capabilities
- **Learning from Feedback**: Fine-tune model on clerk corrections
- **Template Library**: Pre-built compliance templates
- **Collaboration**: Multi-user review workflows
- **API Integrations**: DocuSign, ContractWorks, legal databases
- **Analytics Dashboard**: Trend analysis, compliance metrics

---

## 📚 References

- [CopilotKit Documentation](https://docs.copilotkit.ai/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AG-UI Protocol Specification](https://www.copilotkit.ai/blog/introducing-ag-ui-the-protocol-where-agents-meet-users)
- [LangChain Documentation](https://python.langchain.com/)

---

**Last Updated**: 2025-11-02  
**Version**: 1.0  
**Status**: Initial Design - Subject to Change
