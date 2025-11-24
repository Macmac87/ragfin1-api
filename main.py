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
from crypto_rates_scraper import CryptoRatesScraper

load_dotenv()

app = FastAPI(title="RAGFIN1 API", version="2.0.0")

# Inicializar RAG Engine
# Inicializar Crypto Scraper
crypto_scraper = CryptoRatesScraper()
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
    print("🚀 RAGFIN1 API v2.0 Starting...")
    print("✅ RAG Engine initialized with Claude API")
    records = rag_engine.load_all_data()
    print(f"✅ {len(records)} exchange records loaded")
    print("✅ Crypto rates scraper initialized")
    
    try:
        summary = crypto_scraper.get_crypto_summary()
        print(f"✅ Crypto coverage: USDT {summary['rates_by_coin']['USDT']['coverage_pct']}%, USDC {summary['rates_by_coin']['USDC']['coverage_pct']}%")
    except Exception as e:
        print(f"⚠️  Crypto scraper warning: {e}")

# ==================== CRYPTO ENDPOINTS ====================

@app.get("/api/v1/crypto-rates")
async def get_crypto_rates(currencies: Optional[str] = None):
    """Obtiene tasas actuales de USDT/USDC a monedas locales"""
    try:
        currency_list = None
        if currencies:
            currency_list = [c.strip().upper() for c in currencies.split(",")]
        
        rates = crypto_scraper.get_all_rates(currency_list)
        
        return {
            "success": True,
            "data": rates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/crypto-summary")
async def get_crypto_summary():
    """Resumen de cobertura de stablecoins"""
    try:
        summary = crypto_scraper.get_crypto_summary()
        return {
            "success": True,
            "data": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/compare-traditional-vs-crypto/{destination}")
async def compare_traditional_vs_crypto(destination: str, amount: float = 1000):
    """Compara costo de remesa tradicional vs crypto para un país"""
    try:
        from collections import defaultdict
        
        traditional_records = rag_engine.filter_data(destination=destination.upper(), limit=50)
        
        if not traditional_records:
            raise HTTPException(status_code=404, detail=f"No traditional rates found for {destination}")
        
        by_provider = defaultdict(list)
        for rec in traditional_records:
            by_provider[rec.provider].append(rec)
        
        traditional_rates = {}
        for provider, recs in by_provider.items():
            avg_rate = sum(r.exchange_rate for r in recs) / len(recs)
            avg_fee = sum(r.fee for r in recs) / len(recs)
            
            traditional_rates[provider] = {
                "rate": avg_rate,
                "fee": avg_fee,
                "total_cost": avg_rate + avg_fee
            }

        currency_map = {
            "MX": "MXN", "CO": "COP", "VE": "VES", "BR": "BRL", 
            "CL": "CLP", "AR": "ARS", "PE": "PEN", "BO": "BOB"
        }

        currency = currency_map.get(destination, destination)
        crypto_rates = crypto_scraper.get_all_rates([currency])




        comparison = crypto_scraper.compare_with_traditional(currency, traditional_rates, crypto_rates, amount)
        
        return {
            "success": True,
            "destination": destination,
            "amount_usd": amount,
            "data": comparison
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)