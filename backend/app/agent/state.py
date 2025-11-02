from typing import TypedDict, List, Optional, Dict, Annotated
from datetime import datetime
import operator


class RenewalDate(TypedDict):
    """Structure for renewal date information"""
    date: datetime
    description: str
    days_until: int
    urgency: str  # "critical" | "high" | "medium" | "low"
    clause_reference: Optional[str]


class Obligation(TypedDict):
    """Structure for contractual obligations"""
    clause_id: str
    requirement: str
    party: str
    status: str  # "pending" | "met" | "overdue" | "unclear"
    deadline: Optional[datetime]
    description: str


class ComplianceItem(TypedDict):
    """Structure for compliance requirements"""
    regulation: str
    requirement: str
    status: str  # "compliant" | "non_compliant" | "partially_compliant" | "unclear"
    gap: Optional[str]
    severity: str  # "critical" | "high" | "medium" | "low"


class Risk(TypedDict):
    """Structure for identified risks"""
    id: str
    category: str  # "deadline" | "compliance" | "contractual" | "financial" | "reputational"
    severity: str  # "critical" | "high" | "medium" | "low"
    description: str
    mitigation: str
    score: float  # 0-100


class DocumentMetadata(TypedDict):
    """Document metadata"""
    document_type: str
    parties: List[str]
    effective_date: Optional[datetime]
    expiration_date: Optional[datetime]
    document_id: Optional[str]
    jurisdiction: Optional[str]


class HumanFeedback(TypedDict):
    """Human-in-the-loop feedback"""
    timestamp: datetime
    action: str  # "approved" | "revised" | "rejected"
    comments: Optional[str]
    modifications: Optional[Dict]


class VerificationReport(TypedDict):
    """Final verification report structure"""
    document_id: str
    generated_at: datetime
    summary: str
    risk_level: str
    overall_risk_score: float
    sections: Dict[str, any]


class DocumentVerificationState(TypedDict):
    """Main state schema for the document verification agent"""
    
    # Input
    document_file: str
    document_type: str
    user_id: str
    session_id: str
    
    # Document Processing
    raw_text: str
    parsed_sections: Annotated[List[Dict[str, str]], operator.add]
    document_metadata: Optional[DocumentMetadata]
    
    # Extraction Results
    renewal_dates: Annotated[List[RenewalDate], operator.add]
    obligations: Annotated[List[Obligation], operator.add]
    compliance_items: Annotated[List[ComplianceItem], operator.add]
    
    # Risk Assessment
    risks: Annotated[List[Risk], operator.add]
    overall_risk_score: float
    risk_level: str  # "critical" | "high" | "medium" | "low"
    
    # Human-in-the-Loop
    human_feedback: Optional[HumanFeedback]
    requires_review: bool
    review_items: Annotated[List[str], operator.add]
    
    # Agent Progress
    current_step: str
    progress_percentage: int
    messages: Annotated[List[str], operator.add]
    
    # Output
    verification_report: Optional[VerificationReport]
    recommendations: Annotated[List[str], operator.add]
    
    # Status & Error Handling
    status: str  # "processing" | "review_required" | "completed" | "error"
    error_message: Optional[str]
    
    # Metadata
    created_at: datetime
    updated_at: datetime
