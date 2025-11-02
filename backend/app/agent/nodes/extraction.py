"""
Requirement Extraction Node
Extracts renewal dates, obligations, and compliance requirements from documents
"""
from typing import Dict, List
import logging
from datetime import datetime, timedelta
import re

from app.agent.state import DocumentVerificationState, RenewalDate, Obligation, ComplianceItem

logger = logging.getLogger(__name__)


async def extraction_node(state: DocumentVerificationState) -> Dict:
    """
    Extract key information from document
    
    Tasks:
    1. Extract renewal dates and deadlines
    2. Identify contractual obligations
    3. Find compliance requirements
    4. Parse dates and calculate urgency
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with extracted data
    """
    logger.info("Starting requirement extraction")
    
    try:
        raw_text = state["raw_text"]
        document_type = state["document_type"]
        
        # TODO: Use LLM for semantic extraction
        # For now, using placeholder logic
        
        # Extract renewal dates
        renewal_dates = await extract_renewal_dates(raw_text)
        
        # Extract obligations
        obligations = await extract_obligations(raw_text, document_type)
        
        # Extract compliance items
        compliance_items = await extract_compliance_requirements(raw_text, document_type)
        
        logger.info(f"Extracted {len(renewal_dates)} renewal dates, "
                   f"{len(obligations)} obligations, "
                   f"{len(compliance_items)} compliance items")
        
        return {
            "renewal_dates": renewal_dates,
            "obligations": obligations,
            "compliance_items": compliance_items,
            "current_step": "extraction",
            "progress_percentage": 45,
            "messages": [
                f"Extracted {len(renewal_dates)} renewal dates",
                f"Found {len(obligations)} contractual obligations",
                f"Identified {len(compliance_items)} compliance requirements"
            ],
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in extraction node: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Extraction failed: {str(e)}",
            "current_step": "extraction",
            "updated_at": datetime.utcnow().isoformat()
        }


async def extract_renewal_dates(text: str) -> List[RenewalDate]:
    """
    Extract renewal dates and deadlines from text
    
    Uses:
    1. Regex patterns for common date formats
    2. Keywords: renewal, expiration, deadline, termination
    3. LLM for context understanding (TODO)
    """
    renewal_dates = []
    
    # Date patterns
    date_patterns = [
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',  # MM/DD/YYYY or DD-MM-YYYY
        r'\b([A-Z][a-z]+ \d{1,2},? \d{4})\b',     # Month DD, YYYY
        r'\b(\d{4}-\d{2}-\d{2})\b'                 # YYYY-MM-DD
    ]
    
    # Keywords for renewal context
    renewal_keywords = [
        'renewal date', 'expiration date', 'deadline', 'termination date',
        'expires on', 'renews on', 'due date', 'notice period'
    ]
    
    # TODO: Replace with actual LLM extraction
    # Placeholder: Create sample renewal dates
    sample_date = datetime.utcnow() + timedelta(days=90)
    days_until = (sample_date - datetime.utcnow()).days
    
    renewal_dates.append({
        "date": sample_date.isoformat(),
        "description": "Contract renewal deadline",
        "days_until": days_until,
        "urgency": calculate_urgency(days_until),
        "clause_reference": "Section 5.2"
    })
    
    # Add another sample
    sample_date_2 = datetime.utcnow() + timedelta(days=30)
    days_until_2 = (sample_date_2 - datetime.utcnow()).days
    
    renewal_dates.append({
        "date": sample_date_2.isoformat(),
        "description": "Insurance certificate renewal",
        "days_until": days_until_2,
        "urgency": calculate_urgency(days_until_2),
        "clause_reference": "Exhibit B"
    })
    
    return renewal_dates


async def extract_obligations(text: str, document_type: str) -> List[Obligation]:
    """
    Extract contractual obligations and commitments
    
    Looks for:
    - "Party shall/must/will..."
    - Deliverables and milestones
    - Performance requirements
    """
    obligations = []
    
    # TODO: Use LLM to extract obligations with context
    # Placeholder: Create sample obligations
    
    obligations_data = [
        {
            "clause_id": "3.1",
            "requirement": "Provide monthly status reports",
            "party": "Party A",
            "status": "pending",
            "deadline": (datetime.utcnow() + timedelta(days=15)).isoformat(),
            "description": "Submit detailed monthly reports by the 15th of each month"
        },
        {
            "clause_id": "4.2",
            "requirement": "Maintain insurance coverage",
            "party": "Party B",
            "status": "pending",
            "deadline": None,
            "description": "Maintain general liability insurance of $1M minimum"
        },
        {
            "clause_id": "6.1",
            "requirement": "Compliance with data protection regulations",
            "party": "Both Parties",
            "status": "unclear",
            "deadline": None,
            "description": "Comply with GDPR and applicable data protection laws"
        }
    ]
    
    for data in obligations_data:
        obligations.append(data)
    
    return obligations


async def extract_compliance_requirements(text: str, document_type: str) -> List[ComplianceItem]:
    """
    Extract regulatory and compliance requirements
    
    Identifies:
    - Regulatory references (GDPR, HIPAA, SOX, etc.)
    - Certifications required (ISO, SOC 2, etc.)
    - Industry-specific compliance
    """
    compliance_items = []
    
    # Common compliance regulations
    compliance_keywords = {
        'GDPR': ['gdpr', 'data protection', 'privacy regulation'],
        'HIPAA': ['hipaa', 'health insurance portability'],
        'SOX': ['sarbanes-oxley', 'sox'],
        'ISO27001': ['iso 27001', 'information security management'],
        'SOC2': ['soc 2', 'service organization control']
    }
    
    # TODO: Use LLM for comprehensive compliance extraction
    # Placeholder: Create sample compliance items
    
    compliance_data = [
        {
            "regulation": "GDPR",
            "requirement": "Data Processing Agreement required",
            "status": "non_compliant",
            "gap": "No DPA found in contract documents",
            "severity": "high"
        },
        {
            "regulation": "ISO27001",
            "requirement": "Annual security audit",
            "status": "partially_compliant",
            "gap": "Last audit was 14 months ago (exceeds 12-month requirement)",
            "severity": "medium"
        },
        {
            "regulation": "SOC2 Type II",
            "requirement": "Current SOC2 certification",
            "status": "compliant",
            "gap": None,
            "severity": "low"
        }
    ]
    
    for data in compliance_data:
        compliance_items.append(data)
    
    return compliance_items


def calculate_urgency(days_until: int) -> str:
    """
    Calculate urgency level based on days until deadline
    
    Returns: "critical" | "high" | "medium" | "low"
    """
    if days_until < 0:
        return "critical"  # Overdue
    elif days_until <= 7:
        return "critical"  # Within a week
    elif days_until <= 30:
        return "high"      # Within a month
    elif days_until <= 90:
        return "medium"    # Within 3 months
    else:
        return "low"       # More than 3 months
