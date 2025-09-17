"""
Chroma RAG Service для OpenMineralHub
Интеграция векторной БД для семантического поиска и AI анализа
"""

import chromadb
import json
import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from pydantic import BaseModel
from fastapi import HTTPException
from config.chroma_config import chroma_config

# New imports for RAG
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser

logger = logging.getLogger(__name__)

class MineralDocument(BaseModel):
    """Модель документа минерала"""
    commodity: str
    name_ru: str
    name_en: str
    symbol: str
    commodity_type: str
    current_price_usd: float
    unit: str
    market: str
    annual_production: float
    top_producers: List[str]
    main_uses: List[str]
    description: str
    document: str
    metadata: Dict[str, Any]

class DealDocument(BaseModel):
    """Модель торговой сделки"""
    deal_id: str
    commodity: str
    counterparty: str
    quantity: float
    price_usd: float
    total_amount_usd: float
    date: str
    status: str
    risk_level: str
    region: str
    document: str
    metadata: Dict[str, Any]

class KYCDocument(BaseModel):
    """Модель KYC документа"""
    company_name: str
    lei: str
    jurisdiction: str
    industry: str
    aml_status: str
    risk_score: int
    verification_sources: List[str]
    document: str
    metadata: Dict[str, Any]

class ChromaService:
    """
    Chroma RAG Service для OpenMineralHub
    Поддержка локального и Cloud ChromaDB для production и тестов
    """
    
    COLLECTIONS = {
        "minerals": "openmineral_minerals",
        "deals": "openmineral_deals", 
        "kyc": "openmineral_kyc"
    }
    
    def __init__(self, is_test_mode: bool = False):
        """Инициализация клиента Chroma (Cloud для prod, локальный для тестов)"""
        self.is_test_mode = is_test_mode
        self.test_db_path = "./chroma_test_db"
        
        try:
            if is_test_mode:
                # Локальный ChromaDB для тестов (persistent)
                self.client = chromadb.PersistentClient(path=self.test_db_path)
                logger.info(f"Локальный ChromaDB для тестов инициализирован: {self.test_db_path}")
            else:
                # Cloud ChromaDB для production
                self.client = chromadb.CloudClient(
                    api_key=chroma_config.API_KEY,
                    tenant=chroma_config.TENANT,
                    database=chroma_config.DATABASE
                )
                logger.info(f"Chroma Cloud клиент инициализирован: {chroma_config.get_connection_string()}")
            
            self._setup_collections()
        except Exception as e:
            logger.error(f"Ошибка инициализации Chroma: {e}")
            raise HTTPException(status_code=500, detail=f"Chroma init error: {str(e)}")
    
    def _setup_collections(self):
        """Создание/получение коллекций"""
        # Коллекция минералов
        self.minerals_collection = self.client.get_or_create_collection(
            name=self.COLLECTIONS["minerals"],
            metadata={
                "description": "Каталог минералов OpenMineralHub",
                "version": "1.0",
                "project": "OpenMineralHub",
                "environment": "test" if self.is_test_mode else "production"
            }
        )
        
        # Коллекция сделок
        self.deals_collection = self.client.get_or_create_collection(
            name=self.COLLECTIONS["deals"],
            metadata={
                "description": "Торговые сделки OpenMineralHub",
                "version": "1.0", 
                "project": "OpenMineralHub",
                "environment": "test" if self.is_test_mode else "production"
            }
        )
        
        # Коллекция KYC/Compliance
        self.kyc_collection = self.client.get_or_create_collection(
            name=self.COLLECTIONS["kyc"],
            metadata={
                "description": "KYC и compliance документы",
                "version": "1.0",
                "project": "OpenMineralHub",
                "compliance_standard": "AML_KYC",
                "environment": "test" if self.is_test_mode else "production"
            }
        )
        
        logger.info("Коллекции Chroma инициализированы")
    
    def load_initial_data(self) -> bool:
        """Загрузка начальных тестовых данных"""
        if self.is_test_mode:
            print("📊 Загрузка тестовых данных в локальную ChromaDB...")
        else:
            print("📊 Загрузка начальных данных OpenMineralHub...")
        
        # 1. Минералы (5 ключевых)
        minerals = [
            {
                "id": "cu_base_metal",
                "document": "Медь (Cu) - основной промышленный металл для электропроводки, строительства, электроники, возобновляемой энергетики. Крупнейшие производители: Чили (28%), Перу (10%), Китай (8%). Цена LME: $9,500/тонна. Спрос растет из-за зеленой энергетики и электромобилей. Годовая добыча: 21 млн тонн.",
                "metadata": {
                    "commodity": "copper",
                    "name_ru": "Медь",
                    "name_en": "Copper",
                    "type": "base_metal",
                    "symbol": "Cu",
                    "current_price": 9500,
                    "unit": "USD/ton",
                    "market": "LME",
                    "annual_production": 21000000,
                    "top_producers": ["Chile", "Peru", "China"],
                    "main_uses": ["wiring", "construction", "electronics", "renewables"],
                    "risk_factors": ["china_demand", "green_energy"],
                    "source": "openmineral_catalog",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "li_battery_material",
                "document": "Литий (Li) - щелочной металл, ключевой компонент литий-ионных аккумуляторов для электромобилей и возобновляемой энергии. Спрос вырос на 300% за 5 лет. Основные источники: соляные озера Австралии (50%), Чили (30%). Цена карбоната лития: $15,000/тонна. Прогноз дефицита до 2030 года из-за EV boom.",
                "metadata": {
                    "commodity": "lithium",
                    "name_ru": "Литий",
                    "name_en": "Lithium", 
                    "type": "battery_material",
                    "symbol": "Li",
                    "current_price": 15000,
                    "unit": "USD/ton",
                    "market": "battery_index",
                    "annual_production": 130000,
                    "top_producers": ["Australia", "Chile", "Argentina"],
                    "main_uses": ["EV_batteries", "energy_storage", "renewables"],
                    "risk_factors": ["supply_chain", "environmental", "price_volatility"],
                    "source": "openmineral_catalog",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "au_precious_metal",
                "document": "Золото (Au) - благородный металл, используется в ювелирных изделиях (50%), инвестициях (40%), электронике (10%). Текущая спот цена: $2,650/унция. Крупнейшие производители: Китай (11%), Австралия (10%), Россия (9%). Золото служит защитным активом во время экономических кризисов и инфляции.",
                "metadata": {
                    "commodity": "gold",
                    "name_ru": "Золото",
                    "name_en": "Gold",
                    "type": "precious_metal",
                    "symbol": "Au",
                    "current_price": 2650,
                    "unit": "USD/oz",
                    "market": "COMEX",
                    "annual_production": 3300,
                    "top_producers": ["China", "Australia", "Russia"],
                    "main_uses": ["jewelry", "investment", "electronics"],
                    "risk_factors": ["inflation", "geopolitics", "central_banks"],
                    "source": "openmineral_catalog",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "ni_base_metal",
                "document": "Никель (Ni) - переходный металл, используется в производстве нержавеющей стали (65%), электромобильных аккумуляторов (20%), специальных сплавов (10%). Крупнейший производитель: Индонезия (50% мировой добычи). Месторождения: Соровия (Индонезия), Норильск (Россия). Цена LME: $18,000/тонна.",
                "metadata": {
                    "commodity": "nickel",
                    "name_ru": "Никель",
                    "name_en": "Nickel",
                    "type": "base_metal",
                    "symbol": "Ni",
                    "current_price": 18000,
                    "unit": "USD/ton",
                    "market": "LME",
                    "annual_production": 2500000,
                    "top_producers": ["Indonesia", "Philippines", "Russia"],
                    "main_uses": ["stainless_steel", "EV_batteries", "alloys"],
                    "risk_factors": ["export_bans", "supply_concentration", "environmental"],
                    "source": "openmineral_catalog",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "fe_industrial_metal",
                "document": "Железная руда (Fe) - основной сырье для производства стали (98% мировой добычи). Крупнейшие экспортеры: Австралия (55%), Бразилия (20%), Китай (импорт). Месторождения: Хэмэрсли (Австралия), Карихара (Бразилия). Цена железной руды 62% Fe: $110/тонна на DCE. Глобальное производство: 2.6 млрд тонн/год.",
                "metadata": {
                    "commodity": "iron_ore",
                    "name_ru": "Железная руда",
                    "name_en": "Iron Ore",
                    "type": "industrial_metal",
                    "symbol": "Fe",
                    "current_price": 110,
                    "unit": "USD/ton",
                    "market": "DCE",
                    "annual_production": 2600000000,
                    "top_producers": ["Australia", "Brazil", "China"],
                    "main_uses": ["steel_production", "construction", "infrastructure"],
                    "risk_factors": ["china_economy", "global_infrastructure", "environmental"],
                    "source": "openmineral_catalog",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            }
        ]
        
        # Добавление минералов
        mineral_docs = [m["document"] for m in minerals]
        mineral_meta = [m["metadata"] for m in minerals]
        mineral_ids = [m["id"] for m in minerals]
        
        self.minerals_collection.add(
            documents=mineral_docs,
            metadatas=mineral_meta,
            ids=mineral_ids
        )
        print(f"✅ Загружено {len(minerals)} минералов в коллекцию '{self.COLLECTIONS['minerals']}'")
        
        # 2. Сделки (5 примеров)
        deals = [
            {
                "id": "deal_omh_001_cu_glencore",
                "document": "Торговая сделка OMH-001: Продажа 500 тонн меди международному трейдеру Glencore International AG. Цена реализации: $9,500 за тонну. Общая контрактная сумма: $4,750,000 USD. Дата заключения: 15 января 2025 года. Срок поставки: первый квартал 2025 года. Порт отгрузки: Вальпараисо, Чили. Условия поставки: FOB. Валюта расчетов: USD. Статус сделки: подтверждена. Оценка рисков: средний уровень (логистические риски Латинской Америки, валютные колебания). Контрагент: Glencore (Швейцария, LEI: 213800E2AWGCG8J3CS80).",
                "metadata": {
                    "deal_id": "OMH-001",
                    "type": "spot_sale",
                    "commodity": "copper",
                    "quantity_tons": 500,
                    "price_usd_per_ton": 9500,
                    "total_amount_usd": 4750000,
                    "date": "2025-01-15",
                    "delivery_period": "Q1_2025",
                    "counterparty": "Glencore International AG",
                    "port": "Valparaiso",
                    "incoterms": "FOB",
                    "currency": "USD",
                    "status": "confirmed",
                    "risk_level": "medium",
                    "risk_factors": ["latin_america_logistics", "currency_fluctuation"],
                    "region": "South_America",
                    "compliance_status": "verified",
                    "source": "trading_system",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "deal_omh_002_li_sqm",
                "document": "Торговая сделка OMH-002: Закупка 200 тонн карбоната лития у Sociedad Química y Minera de Chile S.A. (SQM). Цена закупки: $15,000 за тонну. Общая сумма контракта: $3,000,000 USD. Дата заключения: 1 февраля 2025 года. Срок поставки: второй квартал 2025 года. Пункт отгрузки: Антофагаста, Чили. Условия поставки: CIF порт Роттердам, Нидерланды. Валюта расчетов: USD. Статус сделки: находится в стадии переговоров. Оценка рисков: высокий уровень (политическая нестабильность в Чили, волатильность цен на литий). Контрагент: SQM S.A. (Чили, LEI: 549300J7U7O5Z4K6U171).",
                "metadata": {
                    "deal_id": "OMH-002",
                    "type": "spot_purchase",
                    "commodity": "lithium",
                    "quantity_tons": 200,
                    "price_usd_per_ton": 15000,
                    "total_amount_usd": 3000000,
                    "date": "2025-02-01",
                    "delivery_period": "Q2_2025",
                    "counterparty": "SQM S.A.",
                    "port_origin": "Antofagasta",
                    "port_destination": "Rotterdam",
                    "incoterms": "CIF",
                    "currency": "USD",
                    "status": "negotiation",
                    "risk_level": "high",
                    "risk_factors": ["chile_politics", "lithium_price_volatility", "supply_chain"],
                    "region": "South_America",
                    "compliance_status": "pending",
                    "source": "trading_system",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "deal_omh_003_fe_dce_futures",
                "document": "Фьючерсная сделка OMH-003: Хеджирование 1,000 тонн железной руды на Даляньской товарной бирже (DCE). Фиксированная цена: $110 за тонну (62% Fe CFR Китай). Общая номинальная сумма: $110,000 USD. Дата заключения: 10 марта 2025 года. Месяц поставки: май 2025 года. Тип контракта: фьючерс на поставку. Валюта расчетов: USD. Статус: исполнена. Маржа по сделке: 10% от номинала ($11,000). Цель хеджирования: защита от роста цен на сталь из-за инфраструктурных проектов в Китае. Контрагент: DCE Clearing House.",
                "metadata": {
                    "deal_id": "OMH-003",
                    "type": "futures_hedge",
                    "commodity": "iron_ore",
                    "quantity_tons": 1000,
                    "price_usd_per_ton": 110,
                    "total_amount_usd": 110000,
                    "date": "2025-03-10",
                    "delivery_month": "May_2025",
                    "counterparty": "DCE Exchange",
                    "exchange": "DCE",
                    "contract_type": "futures",
                    "currency": "USD",
                    "status": "executed",
                    "risk_level": "low",
                    "margin_percent": 10,
                    "margin_usd": 11000,
                    "purpose": "price_hedging",
                    "region": "Asia",
                    "compliance_status": "exchange_traded",
                    "source": "futures_system",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "deal_omh_004_ni_indonesia",
                "document": "Специальная сделка OMH-004: Закупка 300 тонн никеля у индонезийского производителя PT Vale Indonesia. Цена: $18,000/тонна. Сумма: $5,400,000 USD. Дата: 20 апреля 2025. Доставка: Q3 2025. Особенности: экспортная лицензия получена, контракт с офшорной структурой. Риски: ограничения на экспорт никеля из Индонезии, логистические задержки из-за погодных условий. Контрагент: PT Vale Indonesia Tbk (LEI: 5493003D7O5Z4K6U172).",
                "metadata": {
                    "deal_id": "OMH-004",
                    "type": "special_purchase",
                    "commodity": "nickel",
                    "quantity_tons": 300,
                    "price_usd_per_ton": 18000,
                    "total_amount_usd": 5400000,
                    "date": "2025-04-20",
                    "delivery_period": "Q3_2025",
                    "counterparty": "PT Vale Indonesia Tbk",
                    "country": "Indonesia",
                    "special_terms": "export_license_required",
                    "currency": "USD",
                    "status": "conditional",
                    "risk_level": "high",
                    "risk_factors": ["indonesia_export_ban", "weather_delays", "offshore_structure"],
                    "region": "Southeast_Asia",
                    "compliance_status": "pending_approval",
                    "source": "special_deals",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "deal_omh_005_au_hedge",
                "document": "Инвестиционная сделка OMH-005: Хеджирование 500 унций золота через фьючерсы COMEX. Фиксированная цена: $2,650/унция. Номинальная сумма: $1,325,000 USD. Дата: 5 июня 2025. Срок экспирации: декабрь 2025. Цель: защита портфеля от инфляции и геополитических рисков. Маржа: 5% ($66,250). Контрагент: CME Group Clearing. Статус: открыта.",
                "metadata": {
                    "deal_id": "OMH-005",
                    "type": "precious_hedge",
                    "commodity": "gold",
                    "quantity_oz": 500,
                    "price_usd_per_oz": 2650,
                    "total_amount_usd": 1325000,
                    "date": "2025-06-05",
                    "expiration": "Dec_2025",
                    "counterparty": "CME Group",
                    "exchange": "COMEX",
                    "contract_type": "futures",
                    "currency": "USD",
                    "status": "open",
                    "risk_level": "low",
                    "margin_percent": 5,
                    "margin_usd": 66250,
                    "purpose": "inflation_hedge",
                    "region": "Global",
                    "compliance_status": "exchange_traded",
                    "source": "investment_system",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            }
        ]
        
        # Добавление сделок
        deal_docs = [d["document"] for d in deals]
        deal_meta = [d["metadata"] for d in deals]
        deal_ids = [d["id"] for d in deals]
        
        self.deals_collection.add(
            documents=deal_docs,
            metadatas=deal_meta,
            ids=deal_ids
        )
        print(f"✅ Загружено {len(deals)} сделок в коллекцию '{self.COLLECTIONS['deals']}'")
        
        # 3. KYC документы (4 контрагента)
        kyc = [
            {
                "id": "kyc_glencore_international",
                "document": "KYC профиль Glencore International AG - ведущего глобального трейдера сырьевыми товарами. Юридическое лицо: Glencore International AG. Регистрация: Швейцария, Baar, Zug. LEI: 213800E2AWGCG8J3CS80. Основная деятельность: торговля металлами, нефтью, сельскохозяйственной продукцией. Годовой оборот: $217 млрд (2023). Основные офисы: Baar (HQ), Лондон (торговля), Сингапур (Азия), Чикаго (США). Кредитный рейтинг: BBB+ (S&P). AML статус: Clean (последняя проверка Q4 2024). Sanctions screening: None (OFAC, EU, UN). Бенефициарные владельцы: публичная компания (LSE: GLEN). Проверено: Reuters, Bloomberg, SEC filings, OFAC database.",
                "metadata": {
                    "document_type": "kyc_profile",
                    "company_name": "Glencore International AG",
                    "lei": "213800E2AWGCG8J3CS80",
                    "legal_form": "AG",
                    "jurisdiction": "Switzerland",
                    "registration_city": "Baar",
                    "industry": "commodity_trading",
                    "sub_industry": "metals_oil_agri",
                    "annual_revenue_billion_usd": 217,
                    "credit_rating": "BBB+",
                    "aml_status": "clean",
                    "sanctions_status": "none",
                    "verification_sources": ["Reuters", "Bloomberg", "SEC", "OFAC", "EU_Sanctions"],
                    "beneficial_owners": "public_company_LSE_GLEN",
                    "risk_score": 2,
                    "risk_factors": ["complex_supply_chains", "emerging_markets"],
                    "documents_verified": ["incorporation_certificate", "financial_statements_2023", "ownership_structure", "aml_policy"],
                    "last_check_date": "2024-12-15",
                    "compliance_officer": "Chief Compliance Officer",
                    "compliance_framework": "Swiss_FINMA_ISO_37001",
                    "source": "corporate_database",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "kyc_sqm_chile",
                "document": "KYC профиль Sociedad Química y Minera de Chile S.A. (SQM) - ведущего производителя лития и химических продуктов. Юридическое лицо: SQM S.A. Регистрация: Чили, Santiago, Región Metropolitana. LEI: 549300J7U7O5Z4K6U171. Основная деятельность: добыча лития из соляного озера Salar de Atacama, производство удобрений и йода. Годовой оборот: $7.4 млрд (2023). Владельцы: Codelco (30%, государственная компания Чили), Tianqi Lithium (23%, Китай). Основные активы: концессия на добычу лития в Салар-де-Атакама. AML статус: Clean. Sanctions: None. Проверено: filings CNMV (Чили), SEC (USA ADR), OFAC, World Bank.",
                "metadata": {
                    "document_type": "kyc_profile",
                    "company_name": "SQM S.A.",
                    "lei": "549300J7U7O5Z4K6U171",
                    "legal_form": "S.A.",
                    "jurisdiction": "Chile",
                    "registration_city": "Santiago",
                    "industry": "mining_chemicals",
                    "sub_industry": "lithium_production",
                    "annual_revenue_billion_usd": 7.4,
                    "credit_rating": "BBB",
                    "aml_status": "clean",
                    "sanctions_status": "none",
                    "ownership_structure": "Codelco_30%, Tianqi_23%, public_47%",
                    "key_assets": "Salar_de_Atacama_concession",
                    "verification_sources": ["CNMV_Chile", "SEC_USA", "OFAC", "World_Bank"],
                    "risk_score": 3,
                    "risk_factors": ["chile_politics", "chinese_ownership", "environmental"],
                    "documents_verified": ["incorporation", "concession_agreement", "financial_statements", "ownership_disclosure"],
                    "last_check_date": "2024-11-20",
                    "compliance_officer": "Director of Legal and Compliance",
                    "compliance_framework": "Chile_SV_Superintendencia_ISO_37001",
                    "source": "mining_database",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "kyc_vale_indonesia",
                "document": "KYC профиль PT Vale Indonesia Tbk - индонезийского производителя никеля. Юридическое лицо: PT Vale Indonesia Tbk. Регистрация: Индонезия, Jakarta. LEI: 549300K8I9J5Z4K6U180. Основная деятельность: добыча и переработка никеля (Соровия, Сулавеси). Владелец: Vale S.A. (Бразилия, 59.4%), Sumitomo Metal Mining (Япония, 15%). Годовой объем производства никеля: 80,000 тонн. AML статус: Clean. Особенности: работает по специальной лицензии на downstream processing (локальная переработка). Проверено: IDX (Индонезия), Vale annual report, OFAC.",
                "metadata": {
                    "document_type": "kyc_profile",
                    "company_name": "PT Vale Indonesia Tbk",
                    "lei": "549300K8I9J5Z4K6U180",
                    "legal_form": "Tbk",
                    "jurisdiction": "Indonesia",
                    "registration_city": "Jakarta",
                    "industry": "nickel_mining",
                    "sub_industry": "downstream_processing",
                    "annual_nickel_production_tons": 80000,
                    "ownership": "Vale_Brazil_59.4%, Sumitomo_Japan_15%",
                    "aml_status": "clean",
                    "sanctions_status": "none",
                    "special_terms": "indonesia_downstream_license",
                    "verification_sources": ["IDX_Indonesia", "Vale_Annual_Report", "OFAC"],
                    "risk_score": 4,
                    "risk_factors": ["indonesia_export_ban", "environmental", "local_content"],
                    "documents_verified": ["mining_license", "downstream_permit", "financials", "ownership"],
                    "last_check_date": "2024-10-15",
                    "compliance_officer": "VP Legal Indonesia",
                    "compliance_framework": "Indonesia_Minerba_ISO_37001",
                    "source": "mining_database",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            },
            {
                "id": "kyc_norilsk_nickel",
                "document": "KYC профиль PJSC MMC Norilsk Nickel - крупнейшего производителя палладия и никеля в России. Юридическое лицо: ПАО «ГМК «Норильский никель». Регистрация: Россия, Москва. LEI: 549300R4K5J5Z4K6U190. Основная деятельность: добыча никеля, палладия, меди, платины на Таймыре. Годовая добыча: 200,000 тонн никеля, 800,000 унций палладия. Владельцы: Rusal (27.8%), Crispian Investments (25.2%). AML статус: Enhanced monitoring (санкции ЕС/США). Особенности: работает под санкциями, использует рублевые расчеты. Проверено: CBR Russia, OFAC, EU Sanctions List.",
                "metadata": {
                    "document_type": "kyc_profile",
                    "company_name": "PJSC MMC Norilsk Nickel",
                    "lei": "549300R4K5J5Z4K6U190",
                    "legal_form": "PAO",
                    "jurisdiction": "Russia",
                    "registration_city": "Moscow",
                    "industry": "mining_metals",
                    "sub_industry": "nickel_palladium",
                    "annual_nickel_tons": 200000,
                    "annual_palladium_oz": 800000,
                    "ownership": "Rusal_27.8%, Crispian_25.2%",
                    "aml_status": "enhanced_monitoring",
                    "sanctions_status": "EU_US_sanctions",
                    "special_terms": "ruble_payments",
                    "verification_sources": ["CBR_Russia", "OFAC", "EU_Sanctions", "Rusal_reports"],
                    "risk_score": 5,
                    "risk_factors": ["russia_sanctions", "geopolitics", "payment_restrictions"],
                    "documents_verified": ["registration", "financials", "ownership", "sanctions_disclosure"],
                    "last_check_date": "2025-01-10",
                    "compliance_officer": "Head of International Compliance",
                    "compliance_framework": "Russia_FATF_ISO_37001",
                    "source": "sanctioned_entities_db",
                    "loaded_at": datetime.now().isoformat(),
                    "environment": "test" if self.is_test_mode else "production"
                }
            }
        ]
        
        # Добавление KYC
        kyc_docs = [k["document"] for k in kyc]
        kyc_meta = [k["metadata"] for k in kyc]
        kyc_ids = [k["id"] for k in kyc]
        
        self.kyc_collection.add(
            documents=kyc_docs,
            metadatas=kyc_meta,
            ids=kyc_ids
        )
        print(f"✅ Загружено {len(kyc)} KYC профилей в коллекцию '{self.COLLECTIONS['kyc']}'")
        
        # Обновление статистики
        stats = self.get_collection_stats()
        print(f"\n📊 Финальная статистика:")
        for key, coll in self.COLLECTIONS.items():
            count = getattr(self, f"{key}_collection").count()
            print(f"   • {key}: {count} документов")
        
        return True
    
    def search_minerals(self, query: str, n_results: int = 3, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Семантический поиск по минералам с фильтрами"""
        try:
            where_filter = filters or {}
            if self.is_test_mode:
                where_filter["environment"] = "test"
            
            results = self.minerals_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            )
            
            enriched_results = []
            for doc, meta, dist in zip(results["documents"][0] or [], results["metadatas"][0] or [], results["distances"][0] or []):
                enriched = {
                    "document": doc,
                    "metadata": meta,
                    "distance": dist,
                    "relevance_score": 1 - dist,  # Нормализованный score
                    "commodity_type": meta.get("type", "unknown"),
                    "current_price": f"${meta.get('current_price', 0):,.0f}/{meta.get('unit', 'N/A')}"
                }
                enriched_results.append(enriched)
            
            return {
                "success": True,
                "query": query,
                "filters": filters,
                "results_count": len(enriched_results),
                "results": enriched_results,
                "processing_time_ms": 0,  # TODO: измерить реальное время
                "environment": "test" if self.is_test_mode else "production"
            }
        except Exception as e:
            logger.error(f"Ошибка поиска минералов: {e}")
            return {"success": False, "error": str(e), "query": query}

    def rag_query(self, query: str, n_results: int = 3, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """RAG query: Chroma search + OpenAI LLM summary"""
        try:
            # Step 1: Chroma search
            search_results = self.search_minerals(query, n_results, filters)
            if not search_results["success"]:
                return search_results
            
            # Step 2: Prepare context from results
            context_docs = [r["document"] for r in search_results["results"]]
            context = "\n\n".join(context_docs)
            
            # Step 3: LLM prompt
            prompt_template = PromptTemplate(
                input_variables=["query", "context"],
                template="""Based on the following mineral commodity information, answer the user's query in Russian.

Context:
{context}

User Query: {query}

Provide a concise, informative response focusing on key facts, prices, producers, and risks. Include any relevant market insights."""
            )
            
            # Step 4: OpenAI call
            if self.is_test_mode:
                # Mock response for testing
                llm_response = "Мок-ответ: Для вашего запроса найдена информация о минералах. В production режиме будет использован OpenAI."
            else:
                llm = ChatOpenAI(
                    model="gpt-4-turbo-preview",
                    temperature=0.1,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
                chain = prompt_template | llm | StrOutputParser()
                llm_response = chain.invoke({"query": query, "context": context})
            
            return {
                "success": True,
                "query": query,
                "rag_enabled": True,
                "chroma_results_count": search_results["results_count"],
                "llm_model": "gpt-4-turbo-preview" if not self.is_test_mode else "mock",
                "response": llm_response,
                "sources": [r["metadata"] for r in search_results["results"]],
                "environment": "test" if self.is_test_mode else "production"
            }
        except Exception as e:
            logger.error(f"Ошибка RAG query: {e}")
            return {"success": False, "error": str(e), "query": query}
    
    def search_deals(self, query: str, n_results: int = 5, status_filter: Optional[str] = None, risk_filter: Optional[str] = None) -> Dict[str, Any]:
        """Поиск по торговым сделкам"""
        try:
            where_filter = {}
            if status_filter:
                where_filter["status"] = status_filter
            if risk_filter:
                where_filter["risk_level"] = risk_filter
            if self.is_test_mode:
                where_filter["environment"] = "test"
            
            results = self.deals_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            )
            
            enriched_results = []
            total_value = 0
            for doc, meta, dist in zip(results["documents"][0] or [], results["metadatas"][0] or [], results["distances"][0] or []):
                deal_value = meta.get("total_amount_usd", 0)
                total_value += deal_value
                
                enriched = {
                    "document": doc,
                    "metadata": meta,
                    "distance": dist,
                    "relevance_score": 1 - dist,
                    "deal_value_usd": f"${deal_value:,.0f}",
                    "status": meta.get("status", "unknown"),
                    "risk": meta.get("risk_level", "unknown"),
                    "counterparty": meta.get("counterparty", "N/A")
                }
                enriched_results.append(enriched)
            
            return {
                "success": True,
                "query": query,
                "filters": {"status": status_filter, "risk": risk_filter},
                "results_count": len(enriched_results),
                "total_deal_value_usd": total_value,
                "results": enriched_results,
                "environment": "test" if self.is_test_mode else "production"
            }
        except Exception as e:
            logger.error(f"Ошибка поиска сделок: {e}")
            return {"success": False, "error": str(e), "query": query}
    
    def search_kyc(self, query: str, n_results: int = 3, aml_filter: Optional[str] = "clean") -> Dict[str, Any]:
        """Поиск KYC документов с compliance фильтрами"""
        try:
            where_filter = {"aml_status": aml_filter}
            if self.is_test_mode:
                where_filter["environment"] = "test"
            
            results = self.kyc_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_filter
            )
            
            clean_count = 0
            total_risk_score = 0
            enriched_results = []
            
            for doc, meta, dist in zip(results["documents"][0] or [], results["metadatas"][0] or [], results["distances"][0] or []):
                risk_score = meta.get("risk_score", 0)
                total_risk_score += risk_score
                
                if meta.get("aml_status") == "clean":
                    clean_count += 1
                
                enriched = {
                    "document": doc,
                    "metadata": meta,
                    "distance": dist,
                    "relevance_score": 1 - dist,
                    "company": meta.get("company_name", "N/A"),
                    "jurisdiction": meta.get("jurisdiction", "N/A"),
                    "aml_status": meta.get("aml_status", "unknown"),
                    "risk_score": risk_score,
                    "risk_level": "low" if risk_score <= 2 else "medium" if risk_score <= 3 else "high",
                    "lei": meta.get("lei", "N/A"),
                    "verification_sources": meta.get("verification_sources", [])
                }
                enriched_results.append(enriched)
            
            avg_risk = total_risk_score / len(enriched_results) if enriched_results else 0
            
            return {
                "success": True,
                "query": query,
                "aml_filter": aml_filter,
                "results_count": len(enriched_results),
                "clean_entities": clean_count,
                "average_risk_score": round(avg_risk, 1),
                "results": enriched_results,
                "environment": "test" if self.is_test_mode else "production"
            }
        except Exception as e:
            logger.error(f"Ошибка поиска KYC: {e}")
            return {"success": False, "error": str(e), "query": query}
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Статистика всех коллекций"""
        try:
            stats = {
                "minerals": self.minerals_collection.count(),
                "deals": self.deals_collection.count(),
                "kyc": self.kyc_collection.count(),
                "total_vectors": self.minerals_collection.count() + self.deals_collection.count() + self.kyc_collection.count(),
                "status": "healthy",
                "last_updated": datetime.now().isoformat(),
                "environment": "test" if self.is_test_mode else "production"
            }
            
            # Дополнительная статистика по сделкам
            deals_meta = self.deals_collection.get()["metadatas"] or []
            total_deal_value = sum(d.get("total_amount_usd", 0) for d in deals_meta)
            confirmed_deals = sum(1 for d in deals_meta if d.get("status") == "confirmed")
            
            stats["deals_value_usd"] = total_deal_value
            stats["confirmed_deals"] = confirmed_deals
            stats["deals_avg_value"] = total_deal_value / len(deals_meta) if deals_meta else 0
            
            return {"success": True, "data": stats}
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {"success": False, "error": str(e)}
    
    def add_document(self, collection_name: str, document: str, metadata: Dict[str, Any], id: Optional[str] = None) -> Dict[str, Any]:
        """Добавление одного документа в коллекцию"""
        try:
            coll_map = {
                "minerals": self.minerals_collection,
                "deals": self.deals_collection,
                "kyc": self.kyc_collection
            }
            
            if collection_name not in coll_map:
                return {"success": False, "error": f"Unknown collection: {collection_name}"}
            
            doc_id = id or f"doc_{uuid.uuid4().hex[:8]}"
            metadata["added_at"] = datetime.now().isoformat()
            metadata["source"] = "api_add_document"
            if self.is_test_mode:
                metadata["test_mode"] = True
                metadata["environment"] = "test"
            else:
                metadata["environment"] = "production"
            
            coll_map[collection_name].add(
                documents=[document],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            return {
                "success": True,
                "collection": collection_name,
                "document_id": doc_id,
                "new_count": coll_map[collection_name].count(),
                "test_mode": self.is_test_mode
            }
        except Exception as e:
            logger.error(f"Ошибка добавления документа: {e}")
            return {"success": False, "error": str(e)}

    def cleanup_test_db(self) -> bool:
        """Очистка тестовой БД (удаление локальных коллекций и файлов)"""
        if not self.is_test_mode:
            logger.warning("cleanup_test_db вызван не в тестовом режиме")
            return False
        
        try:
            # Удаление всех коллекций
            for coll_name in self.COLLECTIONS.values():
                try:
                    self.client.delete_collection(coll_name)
                    logger.info(f"Коллекция {coll_name} удалена")
                except Exception as coll_e:
                    logger.debug(f"Коллекция {coll_name} не найдена для удаления: {coll_e}")
            
            # Удаление файлов БД
            import shutil
            if os.path.exists(self.test_db_path):
                shutil.rmtree(self.test_db_path)
                logger.info(f"Тестовая БД {self.test_db_path} удалена")
            
            # Пересоздание пустого клиента
            self.client = chromadb.PersistentClient(path=self.test_db_path)
            self._setup_collections()
            
            return True
        except Exception as e:
            logger.error(f"Ошибка очистки тестовой БД: {e}")
            return False

# Глобальный singleton экземпляр
chroma_service: Optional[ChromaService] = None
test_chroma_service: Optional[ChromaService] = None

def get_chroma_service(is_test_mode: bool = False) -> ChromaService:
    """Получение экземпляра Chroma сервиса (prod или test)"""
    global chroma_service, test_chroma_service
    
    if is_test_mode:
        if test_chroma_service is None:
            test_chroma_service = ChromaService(is_test_mode=True)
        return test_chroma_service
    else:
        if chroma_service is None:
            chroma_service = ChromaService(is_test_mode=False)
        return chroma_service
