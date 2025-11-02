"""
Compliance Verification Node
Verifies extracted requirements against compliance rules and regulations
"""
from typing import Dict, List
import logging
from datetime import datetime

from app.agent.state import DocumentVerificationState, ComplianceItem

logger = logging.getLogger(__name__)


# Compliance rules database (in production, this would be in a database or vector store)
COMPLIANCE_RULES = {
    "contract": {
        "required_clauses": [
            "Termination clause",
            "Confidentiality agreement",
            "Indemnification clause",
            "Dispute resolution"
        ],
        "required_certifications": [],
        "regulatory_requirements": []
    },
    "license": {
        "required_clauses": [
            "License scope",
            "Usage restrictions",
            "Renewal terms"
        ],
        "required_certifications": ["Business license"],
        "regulatory_requirements": ["State licensing requirements"]
    },
    "service_agreement": {
        "required_clauses": [
            "Service Level Agreement (SLA)",
            "Data protection clause",
            "Liability limitations"
        ],
        "required_certifications": ["ISO27001", "SOC2"],
        "regulatory_requirements": ["GDPR compliance", "Data Processing Agreement"]
    }
}


async def compliance_node(state: DocumentVerificationState) -> Dict:
    """
    Verify compliance against rules and regulations
    
    Tasks:
    1. Load applicable compliance rules
    2. Check extracted items against rules
    3. Identify gaps and missing requirements
    4. Verify deadline compliance
    5. Update compliance status
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with compliance verification results
    """
    logger.info("Starting compliance verification")
    
    try:
        document_type = state["document_type"]
        compliance_items = state.get("compliance_items", [])
        obligations = state.get("obligations", [])
        renewal_dates = state.get("renewal_dates", [])
        
        # Get applicable rules for document type
        rules = COMPLIANCE_RULES.get(document_type, COMPLIANCE_RULES["contract"])
        
        # Verify compliance
        updated_compliance_items = await verify_compliance(
            compliance_items,
            obligations,
            rules
        )
        
        # Check deadline compliance
        deadline_issues = await check_deadline_compliance(renewal_dates)
        
        # Add deadline compliance items
        if deadline_issues:
            updated_compliance_items.extend(deadline_issues)
        
        # Calculate compliance statistics
        total_items = len(updated_compliance_items)
        compliant_count = sum(1 for item in updated_compliance_items 
                             if item["status"] == "compliant")
        non_compliant_count = sum(1 for item in updated_compliance_items 
                                  if item["status"] == "non_compliant")
        
        logger.info(f"Compliance check complete: {compliant_count}/{total_items} compliant")
        
        return {
            "compliance_items": updated_compliance_items,
            "current_step": "compliance",
            "progress_percentage": 60,
            "messages": [
                f"Verified {total_items} compliance requirements",
                f"{compliant_count} items compliant, {non_compliant_count} items need attention"
            ],
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in compliance node: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Compliance verification failed: {str(e)}",
            "current_step": "compliance",
            "updated_at": datetime.utcnow().isoformat()
        }


async def verify_compliance(
    compliance_items: List[ComplianceItem],
    obligations: List[Dict],
    rules: Dict
) -> List[ComplianceItem]:
    """
    Verify compliance items against rules
    
    Checks:
    1. Required clauses present
    2. Required certifications valid
    3. Regulatory requirements met
    """
    verified_items = list(compliance_items)
    
    # Check required clauses
    for clause in rules.get("required_clauses", []):
        # TODO: Use LLM to check if clause exists in document
        # Placeholder: Check if any obligation mentions this clause
        found = any(clause.lower() in oblig.get("description", "").lower() 
                   for oblig in obligations)
        
        if not found:
            verified_items.append({
                "regulation": "Contract Standards",
                "requirement": f"Required clause: {clause}",
                "status": "non_compliant",
                "gap": f"Missing required clause: {clause}",
                "severity": "high"
            })
    
    # Check required certifications
    for cert in rules.get("required_certifications", []):
        # Check if certification is mentioned in compliance items
        found = any(cert.lower() in item.get("regulation", "").lower() 
                   for item in compliance_items)
        
        if not found:
            verified_items.append({
                "regulation": cert,
                "requirement": f"{cert} certification required",
                "status": "unclear",
                "gap": f"No evidence of {cert} certification found",
                "severity": "medium"
            })
    
    # Check regulatory requirements
    for regulation in rules.get("regulatory_requirements", []):
        found = any(regulation.lower() in item.get("requirement", "").lower() 
                   for item in compliance_items)
        
        if not found:
            verified_items.append({
                "regulation": regulation,
                "requirement": f"Compliance with {regulation}",
                "status": "non_compliant",
                "gap": f"No {regulation} compliance documented",
                "severity": "high"
            })
    
    return verified_items


async def check_deadline_compliance(renewal_dates: List[Dict]) -> List[ComplianceItem]:
    """
    Check if deadlines are being met or at risk
    
    Creates compliance items for:
    - Overdue deadlines (critical)
    - Approaching deadlines (warning)
    """
    deadline_items = []
    
    for renewal in renewal_dates:
        days_until = renewal.get("days_until", 0)
        description = renewal.get("description", "Unknown")
        
        if days_until < 0:
            # Overdue
            deadline_items.append({
                "regulation": "Deadline Compliance",
                "requirement": f"Meet deadline: {description}",
                "status": "non_compliant",
                "gap": f"Deadline overdue by {abs(days_until)} days",
                "severity": "critical"
            })
        elif days_until <= 7:
            # Critical - less than a week
            deadline_items.append({
                "regulation": "Deadline Compliance",
                "requirement": f"Meet deadline: {description}",
                "status": "partially_compliant",
                "gap": f"Deadline in {days_until} days - immediate action required",
                "severity": "critical"
            })
        elif days_until <= 30:
            # High - less than a month
            deadline_items.append({
                "regulation": "Deadline Compliance",
                "requirement": f"Meet deadline: {description}",
                "status": "partially_compliant",
                "gap": f"Deadline approaching in {days_until} days",
                "severity": "high"
            })
    
    return deadline_items
