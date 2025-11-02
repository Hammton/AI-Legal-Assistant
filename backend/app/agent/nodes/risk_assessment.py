"""
Risk Assessment Node
Analyzes compliance gaps and calculates risk scores
"""
from typing import Dict, List
import logging
from datetime import datetime

from app.agent.state import DocumentVerificationState, Risk

logger = logging.getLogger(__name__)


# Risk scoring weights
URGENCY_WEIGHT = 0.4  # 40% based on time criticality
SEVERITY_WEIGHT = 0.3  # 30% based on obligation impact
PENALTY_WEIGHT = 0.3   # 30% based on regulatory consequences


async def risk_assessment_node(state: DocumentVerificationState) -> Dict:
    """
    Assess risks based on compliance gaps and obligations
    
    Tasks:
    1. Analyze each compliance gap
    2. Calculate risk scores
    3. Categorize risks
    4. Generate mitigation recommendations
    5. Calculate overall risk score
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with risk assessment results
    """
    logger.info("Starting risk assessment")
    
    try:
        compliance_items = state.get("compliance_items", [])
        obligations = state.get("obligations", [])
        renewal_dates = state.get("renewal_dates", [])
        
        # Assess risks from different sources
        compliance_risks = await assess_compliance_risks(compliance_items)
        deadline_risks = await assess_deadline_risks(renewal_dates)
        obligation_risks = await assess_obligation_risks(obligations)
        
        # Combine all risks
        all_risks = compliance_risks + deadline_risks + obligation_risks
        
        # Calculate overall risk score
        overall_risk_score = calculate_overall_risk_score(all_risks)
        risk_level = determine_risk_level(overall_risk_score)
        
        # Determine if human review is required
        requires_review = overall_risk_score > 75 or any(
            risk["severity"] == "critical" for risk in all_risks
        )
        
        review_items = []
        if requires_review:
            review_items = [
                risk["description"] 
                for risk in all_risks 
                if risk["severity"] in ["critical", "high"]
            ]
        
        logger.info(f"Risk assessment complete: {risk_level} risk "
                   f"(score: {overall_risk_score:.1f}/100)")
        
        return {
            "risks": all_risks,
            "overall_risk_score": overall_risk_score,
            "risk_level": risk_level,
            "requires_review": requires_review,
            "review_items": review_items,
            "current_step": "risk_assessment",
            "progress_percentage": 75,
            "messages": [
                f"Identified {len(all_risks)} risk items",
                f"Overall risk level: {risk_level.upper()}",
                f"Risk score: {overall_risk_score:.1f}/100"
            ],
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in risk assessment node: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Risk assessment failed: {str(e)}",
            "current_step": "risk_assessment",
            "updated_at": datetime.utcnow().isoformat()
        }


async def assess_compliance_risks(compliance_items: List[Dict]) -> List[Risk]:
    """
    Assess risks from compliance gaps
    """
    risks = []
    
    for idx, item in enumerate(compliance_items):
        if item["status"] in ["non_compliant", "partially_compliant"]:
            severity = item.get("severity", "medium")
            regulation = item.get("regulation", "Unknown")
            requirement = item.get("requirement", "Unknown")
            gap = item.get("gap", "Compliance gap identified")
            
            # Calculate risk score for this item
            risk_score = calculate_compliance_risk_score(severity, item["status"])
            
            # Generate mitigation recommendation
            mitigation = generate_compliance_mitigation(regulation, requirement, severity)
            
            risks.append({
                "id": f"compliance_risk_{idx}",
                "category": "compliance",
                "severity": severity,
                "description": f"{regulation}: {gap}",
                "mitigation": mitigation,
                "score": risk_score
            })
    
    return risks


async def assess_deadline_risks(renewal_dates: List[Dict]) -> List[Risk]:
    """
    Assess risks from approaching or missed deadlines
    """
    risks = []
    
    for idx, renewal in enumerate(renewal_dates):
        days_until = renewal.get("days_until", 999)
        urgency = renewal.get("urgency", "low")
        description = renewal.get("description", "Unknown deadline")
        
        if days_until <= 30:  # Only flag deadlines within 30 days
            risk_score = calculate_deadline_risk_score(days_until)
            severity = map_urgency_to_severity(urgency)
            
            mitigation = generate_deadline_mitigation(days_until, description)
            
            risks.append({
                "id": f"deadline_risk_{idx}",
                "category": "deadline",
                "severity": severity,
                "description": f"Deadline approaching: {description} in {days_until} days",
                "mitigation": mitigation,
                "score": risk_score
            })
    
    return risks


async def assess_obligation_risks(obligations: List[Dict]) -> List[Risk]:
    """
    Assess risks from unmet or unclear obligations
    """
    risks = []
    
    for idx, obligation in enumerate(obligations):
        status = obligation.get("status", "pending")
        
        if status in ["overdue", "unclear"]:
            requirement = obligation.get("requirement", "Unknown")
            party = obligation.get("party", "Unknown party")
            
            severity = "high" if status == "overdue" else "medium"
            risk_score = 70 if status == "overdue" else 50
            
            mitigation = generate_obligation_mitigation(requirement, party, status)
            
            risks.append({
                "id": f"obligation_risk_{idx}",
                "category": "contractual",
                "severity": severity,
                "description": f"Obligation {status}: {requirement} ({party})",
                "mitigation": mitigation,
                "score": risk_score
            })
    
    return risks


def calculate_compliance_risk_score(severity: str, status: str) -> float:
    """Calculate risk score for compliance items"""
    severity_scores = {
        "critical": 90,
        "high": 70,
        "medium": 50,
        "low": 30
    }
    
    base_score = severity_scores.get(severity, 50)
    
    # Adjust based on status
    if status == "non_compliant":
        return base_score
    elif status == "partially_compliant":
        return base_score * 0.7
    else:
        return base_score * 0.3


def calculate_deadline_risk_score(days_until: int) -> float:
    """Calculate risk score based on days until deadline"""
    if days_until < 0:
        return 100  # Overdue
    elif days_until <= 7:
        return 90   # Critical
    elif days_until <= 14:
        return 75   # High
    elif days_until <= 30:
        return 60   # Medium
    else:
        return 40   # Low


def calculate_overall_risk_score(risks: List[Risk]) -> float:
    """
    Calculate overall risk score using weighted average
    
    Uses the highest risk scores with diminishing weight
    """
    if not risks:
        return 0.0
    
    # Sort risks by score (descending)
    sorted_risks = sorted(risks, key=lambda r: r["score"], reverse=True)
    
    # Weight the top risks more heavily
    weights = [1.0, 0.7, 0.5, 0.3, 0.2]  # First 5 risks have the most impact
    
    weighted_sum = 0
    weight_total = 0
    
    for idx, risk in enumerate(sorted_risks[:5]):
        weight = weights[idx] if idx < len(weights) else 0.1
        weighted_sum += risk["score"] * weight
        weight_total += weight
    
    overall_score = weighted_sum / weight_total if weight_total > 0 else 0
    
    return round(overall_score, 1)


def determine_risk_level(score: float) -> str:
    """Determine risk level from score"""
    if score >= 76:
        return "critical"
    elif score >= 51:
        return "high"
    elif score >= 26:
        return "medium"
    else:
        return "low"


def map_urgency_to_severity(urgency: str) -> str:
    """Map urgency level to severity"""
    mapping = {
        "critical": "critical",
        "high": "high",
        "medium": "medium",
        "low": "low"
    }
    return mapping.get(urgency, "medium")


def generate_compliance_mitigation(regulation: str, requirement: str, severity: str) -> str:
    """Generate mitigation recommendation for compliance risks"""
    mitigations = {
        "GDPR": "Engage data protection officer to ensure GDPR compliance. Review and update data processing agreements.",
        "ISO27001": "Schedule audit with certified ISO27001 auditor. Review information security management system.",
        "SOC2": "Contact SOC2 auditor to schedule Type II assessment. Review security controls.",
        "default": f"Review {regulation} requirements and develop compliance plan. Consult with legal team if needed."
    }
    
    return mitigations.get(regulation, mitigations["default"])


def generate_deadline_mitigation(days_until: int, description: str) -> str:
    """Generate mitigation for deadline risks"""
    if days_until < 0:
        return f"URGENT: Deadline overdue. Contact relevant parties immediately to address {description}."
    elif days_until <= 7:
        return f"CRITICAL: Take immediate action. Prioritize completion of {description} within the next week."
    elif days_until <= 30:
        return f"HIGH PRIORITY: Schedule completion of {description} within {days_until} days. Set reminders."
    else:
        return f"PLANNED: Schedule {description} completion. Set reminder for {days_until - 7} days."


def generate_obligation_mitigation(requirement: str, party: str, status: str) -> str:
    """Generate mitigation for obligation risks"""
    if status == "overdue":
        return f"Contact {party} immediately regarding overdue obligation: {requirement}. Escalate to management if needed."
    elif status == "unclear":
        return f"Seek clarification from legal team regarding: {requirement}. Document interpretation for {party}."
    else:
        return f"Monitor {requirement} obligation for {party}. Ensure timely completion."
