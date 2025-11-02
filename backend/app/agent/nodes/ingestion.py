"""
Document Ingestion Node
Extracts text from uploaded documents (PDF, DOCX)
"""
from typing import Dict
import logging
from datetime import datetime

from app.agent.state import DocumentVerificationState

logger = logging.getLogger(__name__)


async def ingestion_node(state: DocumentVerificationState) -> Dict:
    """
    Extract text and metadata from document
    
    Tasks:
    1. Validate file format
    2. Extract raw text
    3. Handle OCR if needed
    4. Extract embedded metadata
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with raw_text and document_metadata
    """
    logger.info(f"Starting document ingestion for: {state['document_file']}")
    
    try:
        document_file = state["document_file"]
        
        # The raw_text is already extracted before the agent runs
        # Just pass it through and add metadata
        raw_text = state.get("raw_text", "")
        
        if not raw_text:
            raise ValueError("No text content found in document")
        
        # Extract metadata
        document_metadata = {
            "document_type": "unknown",
            "parties": [],
            "effective_date": None,
            "expiration_date": None,
            "document_id": None,
            "jurisdiction": None
        }
        
        logger.info(f"Document ingestion completed successfully. Text length: {len(raw_text)}")
        
        return {
            "raw_text": raw_text,  # Pass through the already extracted text
            "document_metadata": document_metadata,
            "current_step": "ingestion",
            "progress_percentage": 15,
            "messages": ["Document ingested successfully"],
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in ingestion node: {str(e)}")
        return {
            "status": "error",
            "error_message": f"Document ingestion failed: {str(e)}",
            "current_step": "ingestion",
            "updated_at": datetime.utcnow().isoformat()
        }
