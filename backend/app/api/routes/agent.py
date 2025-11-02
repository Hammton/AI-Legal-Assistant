"""
Agent API Routes
Endpoints for document verification agent
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import logging
from datetime import datetime
import uuid
import os

from app.agent.graph import verification_graph
from app.services.document_processor import document_processor
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/verify-document")
async def verify_document(
    file: UploadFile = File(...),
    user_id: str = "default_user"
):
    """
    Verify a legal document
    
    Processes the document through the verification agent and returns
    risk assessment, compliance analysis, and recommendations.
    
    Args:
        file: Uploaded document (PDF or DOCX)
        user_id: User identifier
        
    Returns:
        Verification results with risk score and recommendations
    """
    try:
        # Validate file type
        if not file.filename.endswith(tuple(settings.ALLOWED_FILE_TYPES)):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {settings.ALLOWED_FILE_TYPES}"
            )
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Save uploaded file temporarily
        upload_dir = settings.UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, f"{session_id}_{file.filename}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Document uploaded: {file.filename} (session: {session_id})")
        
        # Extract text from document
        raw_text = await document_processor.extract_text(file_path)
        
        if not raw_text or len(raw_text) < 100:
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from document or document is too short"
            )
        
        # Initialize state
        initial_state = {
            "document_file": file_path,
            "document_type": "unknown",
            "user_id": user_id,
            "session_id": session_id,
            "raw_text": raw_text,
            "parsed_sections": [],
            "document_metadata": None,
            "renewal_dates": [],
            "obligations": [],
            "compliance_items": [],
            "risks": [],
            "overall_risk_score": 0.0,
            "risk_level": "unknown",
            "human_feedback": None,
            "requires_review": False,
            "review_items": [],
            "current_step": "initialized",
            "progress_percentage": 0,
            "messages": ["Document uploaded successfully"],
            "verification_report": None,
            "recommendations": [],
            "status": "processing",
            "error_message": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Run the agent
        config = {"configurable": {"thread_id": session_id}}
        
        result = await verification_graph.ainvoke(initial_state, config)
        
        logger.info(f"Verification complete for session {session_id}")
        
        # Clean up uploaded file (optional)
        # os.remove(file_path)
        
        # Get the raw text from result or fallback to the original extracted text
        final_raw_text = result.get("raw_text", raw_text)
        
        logger.info(f"Raw text length: {len(final_raw_text) if final_raw_text else 0}")
        
        # Return results
        return JSONResponse(content={
            "session_id": session_id,
            "status": result.get("status", "completed"),
            "risk_level": result.get("risk_level", "unknown"),
            "overall_risk_score": result.get("overall_risk_score", 0),
            "renewal_dates": result.get("renewal_dates", []),
            "obligations": result.get("obligations", []),
            "compliance_items": result.get("compliance_items", []),
            "risks": result.get("risks", []),
            "recommendations": result.get("recommendations", []),
            "requires_review": result.get("requires_review", False),
            "report": result.get("verification_report"),
            "messages": result.get("messages", []),
            "raw_text": final_raw_text  # Include extracted document text
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/status/{session_id}")
async def get_status(session_id: str):
    """
    Get status of a verification session
    
    Args:
        session_id: Session identifier
        
    Returns:
        Current status and progress
    """
    try:
        # In production, this would query the database or checkpointer
        # For now, return basic status
        return {
            "session_id": session_id,
            "status": "completed",
            "message": "Status endpoint - to be implemented with checkpointer"
        }
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hitl-feedback/{session_id}")
async def submit_hitl_feedback(
    session_id: str,
    feedback: dict
):
    """
    Submit human-in-the-loop feedback
    
    Args:
        session_id: Session identifier
        feedback: User feedback (action, comments, modifications)
        
    Returns:
        Updated verification results
    """
    try:
        # TODO: Implement HITL feedback handling
        # This would resume the agent with user feedback
        
        return {
            "session_id": session_id,
            "status": "feedback_received",
            "message": "HITL feedback endpoint - to be implemented"
        }
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
