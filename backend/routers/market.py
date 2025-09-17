from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ai.chroma_service import get_chroma_service
import logging

logger = logging.getLogger(__name__)

class APIResponse(BaseModel):
    """Базовый API response model"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class MineralSearchResult(BaseModel):
    """Результат поиска минерала"""
    document: str
    metadata: dict
    relevance_score: float
    commodity_type: str
    current_price: str

class DealSearchResult(BaseModel):
    """Результат поиска сделки"""
    deal_id: Optional[str]
    commodity: Optional[str]
    counterparty: Optional[str]
    quantity: Optional[float]
    value_usd: Optional[str]
    status: Optional[str]
    risk: Optional[str]
    region: Optional[str]
    relevance_score: float
    document_preview: str

router = APIRouter(prefix="/market", tags=["Market Intelligence"])

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/market", tags=["Market Intelligence"])

class MineralSearchRequest(BaseModel):
    """Запрос поиска минералов"""
    query: str
    n_results: int = Query(5, ge=1, le=10)
    commodity_type: Optional[str] = None
    market: Optional[str] = None

class DealSearchRequest(BaseModel):
    """Запрос поиска сделок"""
    query: str
    n_results: int = Query(5, ge=1, le=20)
    status: Optional[str] = None
    risk_level: Optional[str] = None
    region: Optional[str] = None

@router.get("/search/minerals")
async def search_minerals(
    query: str = Query(..., description="Поисковый запрос по минералам"),
    n_results: int = Query(5, ge=1, le=10),
    commodity_type: Optional[str] = Query(None, description="Тип минерала"),
    market: Optional[str] = Query(None, description="Биржа/рынок")
):
    """
    Семантический поиск по каталогу минералов
    Использует Chroma для поиска по описаниям, характеристикам, ценам
    """
    try:
        service = get_chroma_service()
        
        # Формирование фильтров
        filters = {}
        if commodity_type:
            filters["type"] = commodity_type  # match metadata key
        if market:
            filters["market"] = market
        
        # Поиск в Chroma
        results = service.search_minerals(
            query=query,
            n_results=n_results,
            filters=filters
        )
        
        if not results["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка поиска минералов: {results.get('error', 'Unknown error')}"
            )
        
        # Форматирование результатов
        enriched_results = []
        for item in results["results"]:
            enriched = MineralSearchResult(
                document=item["document"],
                metadata=item["metadata"],
                relevance_score=item["relevance_score"],
                commodity_type=item["commodity_type"],
                current_price=item["current_price"]
            )
            enriched_results.append(enriched)
        
        # Mock AI insights for MVP
        ai_insights = {
            "summary": f"Найдено {len(enriched_results)} релевантных минералов для запроса '{query}'. Рекомендуем проверить текущие цены и риски.",
            "confidence": "medium"
        }
        
        return APIResponse(
            success=True,
            data={
                "query": query,
                "filters": filters,
                "results_count": results["results_count"],
                "processing_time_ms": results.get("processing_time_ms", 0),
                "results": enriched_results,
                "ai_analysis": ai_insights
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка API поиска минералов: {e}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@router.get("/search/deals")
async def search_deals(
    query: str = Query(..., description="Поисковый запрос по сделкам"),
    n_results: int = Query(5, ge=1, le=20),
    status: Optional[str] = Query(None, description="Статус сделки"),
    risk_level: Optional[str] = Query(None, description="Уровень риска"),
    region: Optional[str] = Query(None, description="Регион")
):
    """
    Поиск по торговым сделкам с фильтрами
    Возвращает релевантные сделки + общую статистику
    """
    try:
        service = get_chroma_service()
        
        # Поиск в Chroma
        results = service.search_deals(
            query=query,
            n_results=n_results,
            status_filter=status,
            risk_filter=risk_level
        )
        
        if not results["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка поиска сделок: {results.get('error', 'Unknown error')}"
            )
        
        # Форматирование для ответа
        formatted_results = []
        for item in results["results"]:
            formatted = DealSearchResult(
                deal_id=item["metadata"].get("deal_id"),
                commodity=item["metadata"].get("commodity"),
                counterparty=item["metadata"].get("counterparty"),
                quantity=item["metadata"].get("quantity_tons"),
                value_usd=item["metadata"].get("total_amount_usd"),
                status=item["metadata"].get("status"),
                risk=item["metadata"].get("risk_level"),
                region=item["metadata"].get("region"),
                relevance_score=item["relevance_score"],
                document_preview=item["document"][:200] + "..."
            )
            formatted_results.append(formatted)
        
        return APIResponse(
            success=True,
            data={
                "query": query,
                "filters": {
                    "status": status,
                    "risk_level": risk_level,
                    "region": region
                },
                "results_count": results["results_count"],
                "total_deal_value_usd": results["total_deal_value_usd"],
                "results": formatted_results
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка API поиска сделок: {e}")
        raise HTTPException(status_code=500, detail=f"Search deals error: {str(e)}")

@router.get("/stats")
async def market_stats():
    """
    Статистика рынка и Chroma коллекций
    """
    try:
        service = get_chroma_service()
        stats = service.get_collection_stats()
        
        if not stats["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка получения статистики: {stats.get('error')}"
            )
        
        # Дополнительная аналитика
        stats_data = stats["data"]
        total_value = stats_data.get("deals_value_usd", 0)
        confirmed_deals = stats_data.get("confirmed_deals", 0)
        total_vectors = stats_data.get("total_vectors", 0)
        
        analysis = {
            "total_market_value_usd": f"${total_value:,.0f}",
            "confirmed_deals_count": confirmed_deals,
            "total_knowledge_vectors": total_vectors,
            "data_freshness": stats_data.get("last_updated", "unknown"),
            "system_status": stats_data.get("status", "unknown")
        }
        
        return APIResponse(
            success=True,
            data={
                "chroma_stats": stats_data["stats"],
                "market_analysis": analysis
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения статистики рынка: {e}")
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

@router.get("/search/kyc")
async def search_kyc(
    query: str = Query(..., description="Поисковый запрос по KYC"),
    n_results: int = Query(3, ge=1, le=10),
    aml_filter: Optional[str] = Query("clean", description="AML фильтр"),
    test_mode: bool = Query(False, description="Использовать тестовую БД")
):
    """
    Поиск KYC документов с compliance фильтрами
    """
    try:
        service = get_chroma_service(is_test_mode=test_mode)
        
        results = service.search_kyc(
            query=query,
            n_results=n_results,
            aml_filter=aml_filter
        )
        
        if not results["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка поиска KYC: {results.get('error', 'Unknown error')}"
            )
        
        return APIResponse(
            success=True,
            data={
                "query": query,
                "test_mode": test_mode,
                "environment": results.get("environment", "unknown"),
                "aml_filter": aml_filter,
                "results_count": results["results_count"],
                "clean_entities": results["clean_entities"],
                "average_risk_score": results["average_risk_score"],
                "results": results["results"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка API поиска KYC: {e}")
        raise HTTPException(status_code=500, detail=f"KYC search error: {str(e)}")

@router.get("/rag")
async def rag_search(
    query: str = Query(..., description="RAG запрос (Chroma + LLM)"),
    n_results: int = Query(3, ge=1, le=5),
    commodity_type: Optional[str] = Query(None, description="Тип минерала для фильтра"),
    test_mode: bool = Query(False, description="Тестовый режим (mock LLM)")
):
    """
    RAG endpoint: Семантический поиск + AI summary через OpenAI
    """
    try:
        service = get_chroma_service(is_test_mode=test_mode)
        
        # Фильтры
        filters = {}
        if commodity_type:
            filters["type"] = commodity_type
        
        # RAG query
        rag_results = service.rag_query(
            query=query,
            n_results=n_results,
            filters=filters
        )
        
        if not rag_results["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка RAG поиска: {rag_results.get('error', 'Unknown error')}"
            )
        
        return APIResponse(
            success=True,
            data={
                "query": query,
                "test_mode": test_mode,
                "rag_enabled": rag_results["rag_enabled"],
                "llm_model": rag_results["llm_model"],
                "chroma_results_count": rag_results["chroma_results_count"],
                "ai_response": rag_results["response"],
                "sources": rag_results["sources"],
                "environment": rag_results["environment"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка RAG API: {e}")
        raise HTTPException(status_code=500, detail=f"RAG error: {str(e)}")
