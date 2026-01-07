"""
RAGFIN1 FastAPI Application v3.1.0
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional, List
from collections import defaultdict
from ragfin1_rag import RAGEngine
from crypto_rates_scraper import CryptoRatesScraper
from functools import lru_cache
from datetime import datetime, timedelta

cache_data = {}
CACHE_DURATION = 300

load_dotenv()

app = FastAPI(title="RAGFIN1 API", version="3.1.0")

# Inicializar componentes
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

# ==================== CACHE-BUSTING MIDDLEWARE ====================
@app.middleware("http")
async def add_cache_control_headers(request: Request, call_next):
    response = await call_next(request)
    # No-cache para frontend y static files
    if request.url.path.startswith("/static/") or request.url.path == "/" or not request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# ==================== MODELOS ====================

class QueryRequest(BaseModel):
    query: str
    destination: Optional[str] = None
    provider: Optional[str] = None
    max_tokens: int = 4096

class CompareRequest(BaseModel):
    destination: str
    providers: List[str]

# ==================== ENDPOINTS BÁSICOS ====================


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ==================== RAG ENDPOINTS ====================

@app.post("/api/v1/rag/query")
async def rag_query(request: QueryRequest):
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
    try:
        # Check cache
        cache_key = f"insight_{destination}"
        if cache_key in cache_data:
            cached_time, cached_result = cache_data[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=CACHE_DURATION):
                return cached_result

        # Fetch fresh data
        result = rag_engine.competitive_insight(destination)

        # Store in cache
        cache_data[cache_key] = (datetime.now(), result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/api/v1/rag/compare")
async def compare_providers(request: CompareRequest):
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
    return rag_engine.get_stats()

@app.get("/api/v1/competitive-analysis/{destination}")
async def competitive_analysis(destination: str):
    try:
        # Check cache
        cache_key = f"competitive_{destination}"
        if cache_key in cache_data:
            cached_time, cached_result = cache_data[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=CACHE_DURATION):
                return cached_result

        # Fetch fresh data
        result = rag_engine.get_competitive_analysis(destination)

        # Store in cache
        cache_data[cache_key] = (datetime.now(), result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/crypto-rates")
async def get_crypto_rates(currencies: Optional[str] = None):
    try:
        currency_list = None
        if currencies:
            currency_list = [c.strip().upper() for c in currencies.split(",")]

        rates = crypto_scraper.get_all_rates(currency_list)

        return {"success": True, "data": rates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/crypto-summary")
async def get_crypto_summary():
    try:
        summary = crypto_scraper.get_crypto_summary()
        return {"success": True, "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/compare-traditional-vs-crypto/{destination}")
async def compare_traditional_vs_crypto(destination: str, amount: float = 1000):
    try:
        traditional_records = rag_engine.filter_data(
            destination=destination.upper(),
            limit=50
        )

        if not traditional_records:
            raise HTTPException(
                status_code=404,
                detail=f"No traditional rates found for {destination}"
            )

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

        comparison = crypto_scraper.compare_with_traditional(
            currency,
            traditional_rates,
            crypto_rates,
            amount
        )

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

@app.get("/api/v1/binance-p2p/{destination}")
async def get_binance_p2p_rate(destination: str, amount: float = 1000):
    """Obtiene tasa P2P de Binance para un país"""
    from binance_p2p_scraper import BinanceP2PScraper

    try:
        scraper = BinanceP2PScraper()
        result = scraper.compare_with_traditional(destination.upper(), amount)

        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== CARD PREMIUMS ENDPOINT ====================
from card_scrapers import get_all_card_premiums

@app.get("/api/v1/card-premiums/{country}")
async def get_card_premiums(country: str, amount: int = 500):
    """
    Get card payment premiums for all 11 LATAM countries
    Shows cost comparison: Bank Transfer vs Debit Card vs Credit Card
    Supported: BR, MX, CO, PE, CL, AR, VE, BO, SV, DO, GT
    """
    try:
        country_upper = country.upper()
        data = get_all_card_premiums(country_upper, amount)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== STATIC FILES & FRONTEND ====================

# Montar archivos estáticos del frontend
static_path = os.path.join(os.path.dirname(__file__), "frontend", "build")

if os.path.exists(static_path):
    # Servir archivos estáticos (CSS, JS, imágenes)
    app.mount("/static", StaticFiles(directory=os.path.join(static_path, "static")), name="static")
    
    # Servir el index.html para todas las rutas no-API (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Si la ruta empieza con /api/, dejar que FastAPI la maneje
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Para cualquier otra ruta, servir el index.html del frontend
        index_file = os.path.join(static_path, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        else:
            raise HTTPException(status_code=404, detail="Frontend not found")
else:
    print(f"⚠️  Frontend build not found at {static_path}")
    print("   Run 'npm run build' in frontend directory")

# ==================== STARTUP ====================

@app.on_event("startup")
async def startup_event():
    print("🚀 RAGFIN1 API v3.1.0 Starting...")
    print("✅ RAG Engine initialized")

    records = rag_engine.load_all_data()
    print(f"✅ {len(records)} exchange records loaded")

    print("✅ Crypto rates scraper initialized")

    try:
        summary = crypto_scraper.get_crypto_summary()
        usdt_cov = summary['rates_by_coin']['USDT']['coverage_pct']
        usdc_cov = summary['rates_by_coin']['USDC']['coverage_pct']
        print(f"✅ Crypto coverage: USDT {usdt_cov}%, USDC {usdc_cov}%")
    except Exception as e:
        print(f"⚠️ Crypto scraper warning: {e}")
    
    print("✅ Card premiums available for 11 countries")
    
    # Check if frontend is available
    if os.path.exists(static_path):
        print(f"✅ Frontend build found and mounted")
    else:
        print(f"⚠️  Frontend build not found - API only mode")

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)