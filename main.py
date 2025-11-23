"""
RAGFIN1 FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional, List
from ragfin1_rag import RAGEngine

load_dotenv()

app = FastAPI(title="RAGFIN1 API", version="2.0.0")

# Inicializar RAG Engine
rag_engine = RAGEngine()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELOS PYDANTIC ====================

class QueryRequest(BaseModel):
    query: str
    destination: Optional[str] = None
    provider: Optional[str] = None
    max_tokens: int = 4096

class CompareRequest(BaseModel):
    destination: str
    providers: List[str]

# ==================== ENDPOINTS BÁSICOS ====================

@app.get("/")
async def root():
    return {
        "name": "RAGFIN1 API",
        "version": "2.0.0",
        "status": "operational",
        "features": ["RAG Engine", "Competitive Analysis", "Claude AI Integration"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ==================== RAG ENDPOINTS ====================

@app.post("/api/v1/rag/query")
async def rag_query(request: QueryRequest):
    """Query general al RAG Engine con Claude AI"""
    try:
        result = rag_engine.query(
            user_query=request.query,
            destination=request.destination,
            provider=request.provider,
            max_tokens=request.max_tokens
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/rag/competitive-insight/{destination}")
async def competitive_insight(destination: str):
    """Análisis competitivo profundo para un país usando Claude AI"""
    try:
        result = rag_engine.competitive_insight(destination)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/rag/compare")
async def compare_providers(request: CompareRequest):
    """Comparación directa entre providers usando Claude AI"""
    try:
        result = rag_engine.compare_providers(
            destination=request.destination,
            providers=request.providers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/rag/stats")
async def rag_stats():
    """Stats del RAG Engine (queries, tokens, costos)"""
    return rag_engine.get_stats()

@app.get("/api/v1/competitive-analysis/{destination}")
async def competitive_analysis(destination: str):
    """Análisis competitivo numérico (sin IA) para un país"""
    try:
        result = rag_engine.get_competitive_analysis(destination)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== STARTUP EVENT ====================

@app.on_event("startup")
async def startup_event():
    print("🚀 RAGFIN1 API Starting...")
    print("✅ RAG Engine initialized with Claude API")
    records = rag_engine.load_all_data()
    print(f"✅ {len(records)} exchange records loaded")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)