"""
Report Generation Node
Creates comprehensive verification report
"""
from typing import Dict, List
import logging
from datetime import datetime

from app.agent.state import DocumentVerificationState, VerificationReport

logger = logging.getLogger(__name__)


async def report_generation_node(state: DocumentVerificationState) -> Dict:
    """
    Generate comprehensive verification report
    
    Report includes:
    1. Executive summary
    2. Document information
    3. Renewal dates calendar
    4. Obligations checklist
    5. Compliance analysis
    6. Risk assessment
    7. Recommendations
    8. Supporting evidence
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with verification report
    """
    logger.info("Generating verification report")
    
    try:
        # Gather all data
        document_metadata = state.get("document_metadata", {})
        renewal_dates = state.get("renewal_dates", [])
        obligations = state.get("obligations", [])
        compliance_items = state.get("compliance_items", [])
        risks = state.get("risks", [])
        overall_risk_score = state.get("overall_risk_score", 0)
        risk_level = state.get("risk_level", "unknown")
        
        # Generate report sections
        report = {
            "document_id": state.get("session_id", "unknown"),
            "generated_at": datetime.utcnow().isoformat(),
            "summary": generate_executive_summary(
                risk_level, overall_risk_score, risks, compliance_items
            ),
            "risk_level": risk_level,
            "overall_risk_score": overall_risk_score,
            "sections": {
                "document_info": generate_document_info_section(
                    document_metadata, state.get("document_file", "")
                ),
                "renewal_dates": generate_renewal_dates_section(renewal_dates),
                "obligations": generate_obligations_section(obligations),
                "compliance": generate_compliance_section(compliance_items),
                "risk_assessment": generate_risk_assessment_section(risks, risk_level),
                "recommendations": generate_recommendations_section(
                    risks, compliance_items, renewal_dates
                )
            }
        }
        
        # Generate actionable recommendations
        recommendations = extract_top_recommendations(report["sections"]["recommendations"])
        
        logger.info("Verification report generated successfully")
        
        return {
            "verification_report": report,
            "recommendations": recommendations,
            "status": "completed",
            "current_step": "report_generation",
            "progress_percentage": 100,
            "messages": ["Verification report generated successfully"],
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in report generation node: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Report generation failed: {str(e)}",
            "current_step": "report_generation",
            "updated_at": datetime.utcnow().isoformat()
        }


def generate_executive_summary(
    risk_level: str,
    overall_risk_score: float,
    risks: List[Dict],
    compliance_items: List[Dict]
) -> str:
    """Generate executive summary of findings"""
    
    critical_risks = len([r for r in risks if r["severity"] == "critical"])
    high_risks = len([r for r in risks if r["severity"] == "high"])
    non_compliant = len([c for c in compliance_items if c["status"] == "non_compliant"])
    
    summary = f"""
EXECUTIVE SUMMARY

Overall Risk Level: {risk_level.upper()}
Risk Score: {overall_risk_score:.1f}/100

Key Findings:
- {len(risks)} total risk items identified
- {critical_risks} critical risks requiring immediate attention
- {high_risks} high-priority risks
- {non_compliant} compliance gaps detected

Recommendation: """
    
    if risk_level == "critical":
        summary += "IMMEDIATE ACTION REQUIRED. Address critical risks before proceeding."
    elif risk_level == "high":
        summary += "Prompt action recommended. Address high-priority items within 7 days."
    elif risk_level == "medium":
        summary += "Monitor identified risks. Address within 30 days."
    else:
        summary += "Document is low risk. Continue normal monitoring."
    
    return summary.strip()


def generate_document_info_section(metadata: Dict, filename: str) -> Dict:
    """Generate document information section"""
    return {
        "filename": filename,
        "document_type": metadata.get("document_type", "Unknown"),
        "parties": metadata.get("parties", []),
        "effective_date": metadata.get("effective_date"),
        "expiration_date": metadata.get("expiration_date"),
        "document_id": metadata.get("document_id"),
        "jurisdiction": metadata.get("jurisdiction")
    }


def generate_renewal_dates_section(renewal_dates: List[Dict]) -> Dict:
    """Generate renewal dates section"""
    # Sort by urgency
    sorted_dates = sorted(renewal_dates, key=lambda x: x.get("days_until", 999))
    
    urgent_dates = [d for d in sorted_dates if d.get("urgency") in ["critical", "high"]]
    upcoming_dates = [d for d in sorted_dates if d.get("urgency") in ["medium", "low"]]
    
    return {
        "total_count": len(renewal_dates),
        "urgent": urgent_dates,
        "upcoming": upcoming_dates,
        "calendar_view": [
            {
                "date": d.get("date"),
                "description": d.get("description"),
                "urgency": d.get("urgency"),
                "days_until": d.get("days_until")
            }
            for d in sorted_dates
        ]
    }


def generate_obligations_section(obligations: List[Dict]) -> Dict:
    """Generate obligations section"""
    pending = [o for o in obligations if o["status"] == "pending"]
    unclear = [o for o in obligations if o["status"] == "unclear"]
    overdue = [o for o in obligations if o["status"] == "overdue"]
    met = [o for o in obligations if o["status"] == "met"]
    
    return {
        "total_count": len(obligations),
        "pending": pending,
        "unclear": unclear,
        "overdue": overdue,
        "met": met,
        "checklist": [
            {
                "clause_id": o.get("clause_id"),
                "requirement": o.get("requirement"),
                "party": o.get("party"),
                "status": o.get("status"),
                "deadline": o.get("deadline")
            }
            for o in obligations
        ]
    }


def generate_compliance_section(compliance_items: List[Dict]) -> Dict:
    """Generate compliance analysis section"""
    compliant = [c for c in compliance_items if c["status"] == "compliant"]
    non_compliant = [c for c in compliance_items if c["status"] == "non_compliant"]
    partially_compliant = [c for c in compliance_items if c["status"] == "partially_compliant"]
    unclear = [c for c in compliance_items if c["status"] == "unclear"]
    
    # Group by regulation
    by_regulation = {}
    for item in compliance_items:
        regulation = item.get("regulation", "Other")
        if regulation not in by_regulation:
            by_regulation[regulation] = []
        by_regulation[regulation].append(item)
    
    return {
        "total_count": len(compliance_items),
        "compliant_count": len(compliant),
        "non_compliant_count": len(non_compliant),
        "partially_compliant_count": len(partially_compliant),
        "unclear_count": len(unclear),
        "compliance_rate": len(compliant) / len(compliance_items) * 100 if compliance_items else 0,
        "by_regulation": by_regulation,
        "gaps": non_compliant + partially_compliant
    }


def generate_risk_assessment_section(risks: List[Dict], risk_level: str) -> Dict:
    """Generate risk assessment section"""
    # Group by category
    by_category = {}
    for risk in risks:
        category = risk.get("category", "other")
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(risk)
    
    # Group by severity
    by_severity = {}
    for risk in risks:
        severity = risk.get("severity", "low")
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(risk)
    
    return {
        "overall_level": risk_level,
        "total_risks": len(risks),
        "by_category": by_category,
        "by_severity": by_severity,
        "critical_risks": by_severity.get("critical", []),
        "high_risks": by_severity.get("high", []),
        "risk_matrix": generate_risk_matrix(risks)
    }


def generate_risk_matrix(risks: List[Dict]) -> List[Dict]:
    """Generate risk matrix for visualization"""
    matrix = []
    for risk in risks:
        matrix.append({
            "id": risk.get("id"),
            "category": risk.get("category"),
            "severity": risk.get("severity"),
            "score": risk.get("score"),
            "description": risk.get("description")
        })
    return matrix


def generate_recommendations_section(
    risks: List[Dict],
    compliance_items: List[Dict],
    renewal_dates: List[Dict]
) -> List[Dict]:
    """Generate actionable recommendations"""
    recommendations = []
    
    # Recommendations for critical risks
    critical_risks = [r for r in risks if r["severity"] == "critical"]
    for risk in critical_risks:
        recommendations.append({
            "priority": "critical",
            "category": risk["category"],
            "issue": risk["description"],
            "action": risk["mitigation"],
            "timeline": "Immediate (within 24 hours)"
        })
    
    # Recommendations for high risks
    high_risks = [r for r in risks if r["severity"] == "high"]
    for risk in high_risks[:3]:  # Top 3
        recommendations.append({
            "priority": "high",
            "category": risk["category"],
            "issue": risk["description"],
            "action": risk["mitigation"],
            "timeline": "Within 7 days"
        })
    
    # Recommendations for compliance gaps
    non_compliant = [c for c in compliance_items if c["status"] == "non_compliant"]
    for item in non_compliant[:3]:  # Top 3
        recommendations.append({
            "priority": "high",
            "category": "compliance",
            "issue": item["gap"],
            "action": f"Address {item['regulation']} compliance requirement",
            "timeline": "Within 14 days"
        })
    
    # Recommendations for approaching deadlines
    urgent_deadlines = [d for d in renewal_dates if d.get("urgency") == "critical"]
    for deadline in urgent_deadlines:
        recommendations.append({
            "priority": "critical",
            "category": "deadline",
            "issue": f"Deadline approaching: {deadline['description']}",
            "action": f"Complete renewal process immediately",
            "timeline": f"{deadline['days_until']} days remaining"
        })
    
    return recommendations


def extract_top_recommendations(recommendations: List[Dict]) -> List[str]:
    """Extract top recommendations as simple strings"""
    # Sort by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    sorted_recs = sorted(recommendations, key=lambda r: priority_order.get(r.get("priority", "low"), 3))
    
    # Format as strings
    top_recs = []
    for rec in sorted_recs[:5]:  # Top 5
        priority = rec.get("priority", "").upper()
        action = rec.get("action", "")
        timeline = rec.get("timeline", "")
        top_recs.append(f"[{priority}] {action} - {timeline}")
    
    return top_recs
