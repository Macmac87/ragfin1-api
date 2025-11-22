"""
RAGFIN1 FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAGFIN1 API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"service": "RAGFIN1", "version": "2.0.0", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/direct")
async def direct_query(origin: str, destination: str, amount: float = 500.0):
    try:
        from ragfin1_db import RAGFIN1Database
        db = RAGFIN1Database()
        providers = ["Western Union", "Remitly", "Wise", "Xoom"]
        results = []
        
        for provider in providers:
            data = db.get_latest_corridor(provider, origin, destination, amount)
            if data:
                results.append({
                    "provider": data["provider"],
                    "fee": data["fee"],
                    "exchange_rate": data["exchange_rate"],
                    "recipient_receives": data["recipient_receives"]
                })
        
        db.close()
        return {"success": True, "corridor": f"{origin} → {destination}", "providers": results}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)