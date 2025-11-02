"""
Human-in-the-Loop (HITL) Node
Presents findings to user for review and approval
"""
from typing import Dict
import logging
from datetime import datetime

from app.agent.state import DocumentVerificationState

logger = logging.getLogger(__name__)


async def hitl_node(state: DocumentVerificationState) -> Dict:
    """
    Present findings to user for review
    
    This node pauses the agent workflow and waits for human feedback.
    The actual user interaction happens in the frontend UI.
    
    Tasks:
    1. Prepare review summary
    2. Wait for user feedback (handled by LangGraph interrupt)
    3. Process user feedback
    4. Update state based on feedback
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with human feedback incorporated
    """
    logger.info("Entering human-in-the-loop review checkpoint")
    
    try:
        # Check if we already have feedback
        human_feedback = state.get("human_feedback")
        
        if human_feedback:
            # Feedback received, process it
            action = human_feedback.get("action", "approved")
            comments = human_feedback.get("comments")
            modifications = human_feedback.get("modifications", {})
            
            logger.info(f"Human feedback received: {action}")
            
            if action == "approved":
                return {
                    "requires_review": False,
                    "current_step": "hitl_approved",
                    "progress_percentage": 85,
                    "messages": ["Review approved by user"],
                    "updated_at": datetime.utcnow().isoformat()
                }
            
            elif action == "revised":
                # Apply user modifications
                updated_state = apply_user_modifications(state, modifications)
                updated_state.update({
                    "requires_review": False,
                    "current_step": "hitl_revised",
                    "progress_percentage": 85,
                    "messages": [f"Review revised with user feedback: {comments}"],
                    "updated_at": datetime.utcnow().isoformat()
                })
                return updated_state
            
            elif action == "rejected":
                return {
                    "status": "error",
                    "error_message": f"User rejected findings: {comments}",
                    "current_step": "hitl_rejected",
                    "updated_at": datetime.utcnow().isoformat()
                }
        
        else:
            # No feedback yet, prepare review data
            review_summary = prepare_review_summary(state)
            
            logger.info("Waiting for human review...")
            
            # In LangGraph, this would use interrupt/resume
            # For now, we'll mark as requiring review
            return {
                "requires_review": True,
                "current_step": "hitl_pending",
                "progress_percentage": 80,
                "messages": ["Awaiting human review and approval"],
                "review_items": review_summary["items"],
                "updated_at": datetime.utcnow().isoformat()
            }
        
    except Exception as e:
        logger.error(f"Error in HITL node: {str(e)}")
        return {
            "status": "error",
            "error_message": f"HITL review failed: {str(e)}",
            "current_step": "hitl",
            "updated_at": datetime.utcnow().isoformat()
        }


def prepare_review_summary(state: DocumentVerificationState) -> Dict:
    """
    Prepare summary of findings for human review
    
    Includes:
    - Critical risks requiring attention
    - Compliance gaps
    - Unclear obligations
    - Overall risk assessment
    """
    risks = state.get("risks", [])
    compliance_items = state.get("compliance_items", [])
    obligations = state.get("obligations", [])
    overall_risk_score = state.get("overall_risk_score", 0)
    risk_level = state.get("risk_level", "unknown")
    
    # Extract items requiring review
    review_items = []
    
    # Critical and high severity risks
    critical_risks = [r for r in risks if r["severity"] in ["critical", "high"]]
    if critical_risks:
        review_items.append({
            "type": "risks",
            "priority": "critical",
            "count": len(critical_risks),
            "description": f"{len(critical_risks)} critical/high risks identified",
            "items": critical_risks[:5]  # Top 5
        })
    
    # Non-compliant items
    non_compliant = [c for c in compliance_items if c["status"] == "non_compliant"]
    if non_compliant:
        review_items.append({
            "type": "compliance",
            "priority": "high",
            "count": len(non_compliant),
            "description": f"{len(non_compliant)} compliance gaps found",
            "items": non_compliant[:5]
        })
    
    # Unclear obligations
    unclear_obligations = [o for o in obligations if o["status"] == "unclear"]
    if unclear_obligations:
        review_items.append({
            "type": "obligations",
            "priority": "medium",
            "count": len(unclear_obligations),
            "description": f"{len(unclear_obligations)} obligations need clarification",
            "items": unclear_obligations[:5]
        })
    
    return {
        "overall_risk_score": overall_risk_score,
        "risk_level": risk_level,
        "items": review_items,
        "requires_attention": len(critical_risks) > 0 or len(non_compliant) > 0
    }


def apply_user_modifications(state: DocumentVerificationState, modifications: Dict) -> Dict:
    """
    Apply user modifications to the state
    
    User can modify:
    - Risk severity levels
    - Compliance status
    - Obligation interpretations
    - Add notes and annotations
    """
    updated = {}
    
    # Apply risk modifications
    if "risks" in modifications:
        risks = state.get("risks", [])
        for mod in modifications["risks"]:
            risk_id = mod.get("id")
            for risk in risks:
                if risk["id"] == risk_id:
                    if "severity" in mod:
                        risk["severity"] = mod["severity"]
                    if "description" in mod:
                        risk["description"] = mod["description"]
                    if "mitigation" in mod:
                        risk["mitigation"] = mod["mitigation"]
        updated["risks"] = risks
    
    # Apply compliance modifications
    if "compliance_items" in modifications:
        compliance_items = state.get("compliance_items", [])
        for mod in modifications["compliance_items"]:
            idx = mod.get("index")
            if 0 <= idx < len(compliance_items):
                if "status" in mod:
                    compliance_items[idx]["status"] = mod["status"]
                if "gap" in mod:
                    compliance_items[idx]["gap"] = mod["gap"]
        updated["compliance_items"] = compliance_items
    
    # Apply obligation modifications
    if "obligations" in modifications:
        obligations = state.get("obligations", [])
        for mod in modifications["obligations"]:
            clause_id = mod.get("clause_id")
            for obligation in obligations:
                if obligation["clause_id"] == clause_id:
                    if "status" in mod:
                        obligation["status"] = mod["status"]
                    if "description" in mod:
                        obligation["description"] = mod["description"]
        updated["obligations"] = obligations
    
    # Add user notes
    if "notes" in modifications:
        updated["messages"] = [f"User note: {modifications['notes']}"]
    
    return updated
