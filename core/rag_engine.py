"""
RAGFIN1 Core RAG Engine
"""
import os
from typing import Dict, Optional, Any
from datetime import datetime

class RAGFin1Engine:
    def __init__(self, anthropic_api_key: Optional[str] = None, test_mode: bool = False, **kwargs):
        self.test_mode = test_mode
        print("✅ RAGFIN1 Engine initialized")
    
    def process_query(self, query: str, context: Optional[Dict] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        return {
            "answer": "RAGFIN1 is running in test mode",
            "intent": "test",
            "sources": ["test_mode"],
            "context_used": False,
            "confidence": 0.5,
            "timestamp": datetime.now().isoformat()
        }
    
    def close(self):
        pass