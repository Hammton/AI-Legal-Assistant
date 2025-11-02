from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal
import logging

from app.agent.state import DocumentVerificationState
from app.agent.nodes.ingestion import ingestion_node
from app.agent.nodes.classification import classification_node
from app.agent.nodes.extraction import extraction_node
from app.agent.nodes.compliance import compliance_node
from app.agent.nodes.risk_assessment import risk_assessment_node
from app.agent.nodes.hitl import hitl_node
from app.agent.nodes.report import report_generation_node

logger = logging.getLogger(__name__)


def create_verification_graph():
    """
    Create the LangGraph state machine for document verification
    
    Workflow:
    1. Ingestion: Extract text from document
    2. Classification: Identify document type and structure
    3. Extraction: Extract dates, obligations, compliance items
    4. Compliance: Verify against rules
    5. Risk Assessment: Calculate risk scores
    6. HITL (conditional): Human review if needed
    7. Report Generation: Create final report
    """
    
    # Initialize the graph
    workflow = StateGraph(DocumentVerificationState)
    
    # Add nodes
    workflow.add_node("ingestion", ingestion_node)
    workflow.add_node("classification", classification_node)
    workflow.add_node("extraction", extraction_node)
    workflow.add_node("compliance", compliance_node)
    workflow.add_node("risk_assessment", risk_assessment_node)
    workflow.add_node("hitl", hitl_node)
    workflow.add_node("report_generation", report_generation_node)
    
    # Define edges
    workflow.set_entry_point("ingestion")
    workflow.add_edge("ingestion", "classification")
    workflow.add_edge("classification", "extraction")
    workflow.add_edge("extraction", "compliance")
    workflow.add_edge("compliance", "risk_assessment")
    
    # Conditional edge: go to HITL if review required
    workflow.add_conditional_edges(
        "risk_assessment",
        should_review,
        {
            "review": "hitl",
            "skip": "report_generation"
        }
    )
    
    workflow.add_edge("hitl", "report_generation")
    workflow.add_edge("report_generation", END)
    
    # Add memory for checkpointing
    memory = MemorySaver()
    
    # Compile the graph
    app = workflow.compile(checkpointer=memory)
    
    logger.info("Document verification graph created successfully")
    return app


def should_review(state: DocumentVerificationState) -> Literal["review", "skip"]:
    """
    Determine if human review is required
    
    Review is triggered if:
    - Risk score is critical (>75)
    - Ambiguous findings detected
    - Missing critical information
    - User explicitly requested review
    """
    if state.get("requires_review", False):
        return "review"
    
    risk_score = state.get("overall_risk_score", 0)
    if risk_score > 75:
        return "review"
    
    return "skip"


# Create the graph instance
verification_graph = create_verification_graph()
