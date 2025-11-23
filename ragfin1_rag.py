"""
RAGFIN1 RAG Engine - Production Ready
Integración real con Claude API para inteligencia competitiva
Mario @ MGA - No mocks, no bullshit
"""

import sqlite3
import anthropic
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from dataclasses import dataclass
import numpy as np
from collections import defaultdict

# Cargar variables de entorno
load_dotenv()

@dataclass
class ExchangeRecord:
    """Estructura de un registro de tasa de cambio"""
    provider: str
    destination: str
    exchange_rate: float
    fee: float
    timestamp: str
    corridor: str = ""
    
    def __post_init__(self):
        self.corridor = f"USA-{self.destination}"
    
    def to_dict(self) -> Dict:
        return {
            "provider": self.provider,
            "destination": self.destination,
            "exchange_rate": self.exchange_rate,
            "fee": self.fee,
            "timestamp": self.timestamp,
            "corridor": self.corridor
        }

class RAGEngine:
    """
    Motor RAG para RAGFIN1 - Análisis de inteligencia competitiva
    Usa Claude API para generar insights sobre tasas y fees
    """
    
    def __init__(self, db_path: str = "ragfin1_data.db", api_key: Optional[str] = None):
        self.db_path = db_path
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY no encontrada en environment")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
        
        # Stats para tracking
        self.total_queries = 0
        self.total_tokens = 0
        
    def get_connection(self) -> sqlite3.Connection:
        """Conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def load_all_data(self) -> List[ExchangeRecord]:
        """Carga todos los registros de la DB"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT provider, destination, exchange_rate, fee, timestamp 
            FROM corridors 
            ORDER BY timestamp DESC
        """)
        
        records = []
        for row in cursor.fetchall():
            records.append(ExchangeRecord(
                provider=row['provider'],
                destination=row['destination'],
                exchange_rate=float(row['exchange_rate']),
                fee=float(row['fee']),
                timestamp=row['timestamp']
            ))
        
        conn.close()
        return records
    
    def filter_data(self, 
                    destination: Optional[str] = None,
                    provider: Optional[str] = None,
                    limit: Optional[int] = None) -> List[ExchangeRecord]:
        """Filtra datos según criterios"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT provider, destination, exchange_rate, fee, timestamp FROM corridors WHERE 1=1"
        params = []
        
        if destination:
            query += " AND destination = ?"
            params.append(destination)
        
        if provider:
            query += " AND provider = ?"
            params.append(provider)
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        
        records = []
        for row in cursor.fetchall():
            records.append(ExchangeRecord(
                provider=row['provider'],
                destination=row['destination'],
                exchange_rate=float(row['exchange_rate']),
                fee=float(row['fee']),
                timestamp=row['timestamp']
            ))
        
        conn.close()
        return records
    
    def get_competitive_analysis(self, destination: str) -> Dict:
        """Análisis competitivo para un país específico"""
        records = self.filter_data(destination=destination, limit=100)
        
        if not records:
            return {"error": f"No hay datos para {destination}"}
        
        # Agrupar por provider
        by_provider = defaultdict(list)
        for rec in records:
            by_provider[rec.provider].append(rec)
        
        # Stats por provider
        provider_stats = {}
        for provider, recs in by_provider.items():
            rates = [r.exchange_rate for r in recs]
            fees = [r.fee for r in recs]
            
            provider_stats[provider] = {
                "avg_rate": np.mean(rates),
                "min_rate": np.min(rates),
                "max_rate": np.max(rates),
                "avg_fee": np.mean(fees),
                "total_cost": np.mean(rates) + np.mean(fees),
                "sample_size": len(recs)
            }
        
        # Encontrar el más competitivo (menor total_cost)
        best_provider = min(provider_stats.items(), 
                           key=lambda x: x[1]['total_cost'])
        
        return {
            "destination": destination,
            "providers_analyzed": list(provider_stats.keys()),
            "stats_by_provider": provider_stats,
            "most_competitive": {
                "provider": best_provider[0],
                "total_cost": best_provider[1]['total_cost']
            },
            "data_points": len(records)
        }
    
    def build_context_for_query(self, 
                                query_type: str,
                                destination: Optional[str] = None,
                                provider: Optional[str] = None,
                                limit: int = 50) -> str:
        """
        Construye el contexto relevante para una query
        Optimizado para Claude's context window
        """
        records = self.filter_data(destination=destination, provider=provider, limit=limit)
        
        if not records:
            return "No hay datos disponibles para los criterios especificados."
        
        # Construir contexto estructurado
        context_parts = []
        
        # Header con metadata
        context_parts.append(f"# RAGFIN1 - Datos de Tasas de Cambio")
        context_parts.append(f"Total registros: {len(records)}")
        context_parts.append(f"Última actualización: {records[0].timestamp}")
        context_parts.append("")
        
        # Agrupar por corredor
        by_corridor = defaultdict(list)
        for rec in records:
            by_corridor[rec.corridor].append(rec)
        
        for corridor, corridor_recs in by_corridor.items():
            context_parts.append(f"## {corridor}")
            
            # Agrupar por provider dentro del corredor
            by_provider = defaultdict(list)
            for rec in corridor_recs:
                by_provider[rec.provider].append(rec)
            
            for provider, provider_recs in by_provider.items():
                rates = [r.exchange_rate for r in provider_recs]
                fees = [r.fee for r in provider_recs]
                
                context_parts.append(f"### {provider}")
                context_parts.append(f"- Exchange rate promedio: {np.mean(rates):.4f}")
                context_parts.append(f"- Fee promedio: ${np.mean(fees):.2f}")
                context_parts.append(f"- Costo total: {np.mean(rates) + np.mean(fees):.2f}")
                context_parts.append(f"- Registros: {len(provider_recs)}")
                context_parts.append("")
        
        return "\n".join(context_parts)
    
    def query(self, 
              user_query: str,
              destination: Optional[str] = None,
              provider: Optional[str] = None,
              max_tokens: int = 4096) -> Dict[str, Any]:
        """
        Query principal del RAG Engine
        Usa Claude para analizar los datos y responder
        """
        
        # Construir contexto
        context = self.build_context_for_query(
            query_type="general",
            destination=destination,
            provider=provider,
            limit=100
        )
        
        # System prompt especializado en remesas
        system_prompt = """Eres un analista experto en remesas internacionales y competencia de mercado.

Tu trabajo es analizar datos de tasas de cambio y fees de diferentes providers (Wise, Western Union, Intermex) 
en corredores USA-LatAm.

INSTRUCCIONES:
1. Analiza los datos proporcionados cuidadosamente
2. Identifica patrones, tendencias y oportunidades competitivas
3. Proporciona respuestas precisas con números concretos
4. Compara providers cuando sea relevante
5. Calcula costos totales (exchange_rate + fee) para comparaciones justas
6. Sé directo y conciso - esto es para decisiones de negocio

FORMATO:
- Usa markdown para estructura
- Incluye números específicos
- Destaca insights clave
- No inventes datos que no estén en el contexto"""

        # User prompt con contexto
        user_prompt = f"""Datos disponibles:

{context}

---

Query del usuario: {user_query}

Analiza los datos y responde la pregunta con precisión."""

        try:
            # Llamada a Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extraer respuesta
            answer = response.content[0].text
            
            # Stats
            self.total_queries += 1
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            self.total_tokens += (input_tokens + output_tokens)
            
            return {
                "success": True,
                "answer": answer,
                "metadata": {
                    "model": self.model,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "query_number": self.total_queries
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": None
            }
    
    def competitive_insight(self, destination: str) -> Dict[str, Any]:
        """
        Genera un reporte de inteligencia competitiva para un país
        Usa Claude para análisis profundo
        """
        
        # Primero obtener análisis numérico
        stats = self.get_competitive_analysis(destination)
        
        if "error" in stats:
            return stats
        
        # Construir prompt para análisis estratégico
        query = f"""Analiza la competencia en el corredor USA-{destination}.

Datos estadísticos:
{json.dumps(stats, indent=2)}

Proporciona:
1. Quién es el líder del mercado y por qué
2. Oportunidades de arbitraje o gaps competitivos
3. Recomendaciones estratégicas para un nuevo entrante
4. Tendencias de pricing que observas

Sé específico con números y estrategias accionables."""

        result = self.query(query, destination=destination)
        
        if result["success"]:
            return {
                "success": True,
                "destination": destination,
                "numerical_analysis": stats,
                "strategic_analysis": result["answer"],
                "metadata": result["metadata"]
            }
        else:
            return result
    
    def compare_providers(self, destination: str, providers: List[str]) -> Dict[str, Any]:
        """Comparación directa entre providers para un país"""
        
        query = f"""Compara estos providers en el corredor USA-{destination}: {', '.join(providers)}

Proporciona:
1. Tabla comparativa de costos totales (exchange_rate + fee)
2. Análisis de ventajas/desventajas de cada uno
3. Recomendación según perfil de usuario (volumen alto vs bajo)
4. Gaps de precio entre ellos

Usa los datos reales disponibles."""

        return self.query(query, destination=destination)
    
    def get_stats(self) -> Dict:
        """Stats del RAG Engine"""
        return {
            "total_queries": self.total_queries,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": (self.total_tokens / 1_000_000) * 3.0  # Aproximado para Sonnet
        }


def test_rag_engine():
    """Test básico del RAG Engine"""
    print("🚀 Testing RAGFIN1 RAG Engine...")
    
    try:
        # Inicializar
        rag = RAGEngine()
        print("✅ RAG Engine inicializado")
        
        # Test 1: Cargar datos
        print("\n📊 Cargando datos...")
        records = rag.load_all_data()
        print(f"✅ {len(records)} registros cargados")
        
        # Mostrar primeros 3 registros
        print("\n📋 Primeros 3 registros:")
        for i, rec in enumerate(records[:3]):
            print(f"   {i+1}. {rec.provider} → {rec.destination}: Rate={rec.exchange_rate}, Fee=${rec.fee}")
        
        # Test 2: Análisis competitivo
        print("\n🔍 Análisis competitivo para México (MX)...")
        analysis = rag.get_competitive_analysis("MX")
        
        if "error" not in analysis:
            print(f"✅ Análisis completado: {analysis['providers_analyzed']}")
            print(f"   Más competitivo: {analysis['most_competitive']['provider']}")
        else:
            print(f"⚠️  {analysis['error']}")
        
        # Test 3: Query con Claude
        print("\n🤖 Query con Claude API...")
        result = rag.query("¿Cuál es el provider más barato para enviar a México?", destination="MX")
        
        if result["success"]:
            print("✅ Query exitosa")
            print(f"   Tokens usados: {result['metadata']['total_tokens']}")
            print(f"\n📝 Respuesta:\n{result['answer'][:300]}...")
        else:
            print(f"❌ Error: {result['error']}")
        
        # Stats finales
        print("\n📈 Stats:")
        stats = rag.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n✅ TEST COMPLETADO")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_rag_engine()