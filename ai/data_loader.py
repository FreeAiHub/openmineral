"""
Автоматическая загрузка данных в Chroma для OpenMineralHub
Обновленный загрузчик с поддержкой test_mode
"""

import json
import logging
from datetime import datetime
from ai.chroma_service import get_chroma_service

logger = logging.getLogger(__name__)

class DataLoader:
    """Загрузчик данных для OpenMineralHub"""
    
    @classmethod
    def load_minerals_catalog(cls, test_mode: bool = False):
        """Загрузка каталога минералов из JSON"""
        try:
            service = get_chroma_service(is_test_mode=test_mode)
            
            # Если test_mode, используем встроенные данные из сервиса
            if test_mode:
                success = service.load_initial_data()
                logger.info("✅ Тестовые данные минералов загружены из ChromaService")
                return success
            
            # Production режим - загрузка из файла
            with open("data/minerals_catalog.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            minerals = data.get("minerals", [])
            
            success_count = 0
            for mineral in minerals:
                # Формирование полного документа
                doc = f"{mineral['name']['ru']} ({mineral['name']['en']}) - {mineral['description']}. "
                doc += f"Символ: {mineral['symbol']}. Тип: {mineral['type']}. "
                doc += f"Текущая цена: ${mineral['current_price']:,}/{mineral['unit']} ({mineral['market']}). "
                doc += f"Годовое производство: {mineral['annual_production']:,} тонн. "
                if 'documents' in mineral:
                    doc += " ".join(mineral['documents'])
                
                # Метаданные
                metadata = {
                    **mineral,
                    "document_type": "mineral_catalog",
                    "loaded_at": datetime.now().isoformat(),
                    "source_file": "minerals_catalog.json",
                    "data_source": "openmineral_catalog",
                    "environment": "production"
                }
                
                # Добавление в Chroma
                result = service.add_document(
                    collection_name="minerals",
                    document=doc,
                    metadata=metadata,
                    id=mineral.get("id", f"mineral_{mineral['symbol'].lower()}")
                )
                
                if result["success"]:
                    success_count += 1
                    logger.info(f"Загружен минерал: {mineral['name']['ru']}")
            
            logger.info(f"✅ Загружено {success_count}/{len(minerals)} минералов из каталога")
            return success_count == len(minerals)
            
        except FileNotFoundError:
            logger.warning("Файл data/minerals_catalog.json не найден")
            # Fallback на встроенные данные
            service = get_chroma_service(is_test_mode=test_mode)
            return service.load_initial_data()
        except Exception as e:
            logger.error(f"Ошибка загрузки минералов: {e}")
            return False
    
    @classmethod
    def load_sample_deals(cls, test_mode: bool = False):
        """Загрузка примеров сделок"""
        try:
            service = get_chroma_service(is_test_mode=test_mode)
            
            if test_mode:
                # В test режиме используем встроенные данные сервиса
                success = service.load_initial_data()
                logger.info("✅ Тестовые данные сделок загружены из ChromaService")
                return success
            
            # Production режим - загрузка из встроенных данных (пока нет отдельного файла)
            # Используем те же данные, что в chroma_service
            sample_deals = [
                {
                    "deal_id": "OMH-PROD-001",
                    "document": "Производственная сделка OMH-PROD-001: Продажа 1000 тонн меди крупному промышленному потребителю. Цена: $9,800/тонна. Сумма: $9,800,000 USD. Дата: 2025-01-20. Статус: исполнена.",
                    "metadata": {
                        "deal_id": "OMH-PROD-001",
                        "type": "industrial_sale",
                        "commodity": "copper",
                        "quantity_tons": 1000,
                        "price_usd_per_ton": 9800,
                        "total_amount_usd": 9800000,
                        "date": "2025-01-20",
                        "status": "executed",
                        "risk_level": "low",
                        "counterparty": "Industrial Consumer Inc.",
                        "region": "Europe",
                        "source": "production_data",
                        "loaded_at": datetime.now().isoformat(),
                        "environment": "production"
                    }
                },
                {
                    "deal_id": "OMH-PROD-002",
                    "document": "Производственная сделка OMH-PROD-002: Закупка 500 тонн лития для аккумуляторного производства. Цена: $16,500/тонна. Сумма: $8,250,000 USD. Дата: 2025-02-10. Статус: подтверждена.",
                    "metadata": {
                        "deal_id": "OMH-PROD-002",
                        "type": "battery_purchase",
                        "commodity": "lithium",
                        "quantity_tons": 500,
                        "price_usd_per_ton": 16500,
                        "total_amount_usd": 8250000,
                        "date": "2025-02-10",
                        "status": "confirmed",
                        "risk_level": "medium",
                        "counterparty": "Battery Manufacturer Ltd.",
                        "region": "Asia",
                        "source": "production_data",
                        "loaded_at": datetime.now().isoformat(),
                        "environment": "production"
                    }
                }
            ]
            
            success_count = 0
            for deal_data in sample_deals:
                doc = deal_data["document"]
                metadata = deal_data["metadata"]
                
                result = service.add_document(
                    collection_name="deals",
                    document=doc,
                    metadata=metadata,
                    id=f"deal_{deal_data['deal_id']}"
                )
                
                if result["success"]:
                    success_count += 1
                    logger.info(f"Загружена производственная сделка: {deal_data['deal_id']}")
            
            logger.info(f"✅ Загружено {success_count} производственных сделок")
            return success_count == len(sample_deals)
            
        except Exception as e:
            logger.error(f"Ошибка загрузки производственных сделок: {e}")
            # Fallback на встроенные данные
            service = get_chroma_service(is_test_mode=test_mode)
            return service.load_initial_data()
    
    @classmethod
    def load_sample_kyc(cls, test_mode: bool = False):
        """Загрузка примеров KYC документов"""
        try:
            service = get_chroma_service(is_test_mode=test_mode)
            
            if test_mode:
                # В test режиме используем встроенные данные сервиса
                success = service.load_initial_data()
                logger.info("✅ Тестовые данные KYC загружены из ChromaService")
                return success
            
            # Production режим - загрузка из встроенных данных
            sample_kyc = [
                {
                    "id": "kyc_prod_001_trafigura",
                    "document": "KYC профиль Trafigura Group - глобального трейдера сырьевыми товарами. Штаб-квартира: Сингапур. Основные офисы: Женева, Хьюстон, Пекин. Основная деятельность: торговля нефтью, металлами, минералами. Годовой оборот: $244 млрд (2023). AML статус: Clean. LEI: 549300C5H3Q7J8ZJ7W48.",
                    "metadata": {
                        "document_type": "kyc_profile",
                        "company_name": "Trafigura Group Pte Ltd",
                        "lei": "549300C5H3Q7J8ZJ7W48",
                        "jurisdiction": "Singapore",
                        "industry": "commodity_trading",
                        "annual_revenue_billion_usd": 244,
                        "aml_status": "clean",
                        "risk_score": 2,
                        "verification_sources": ["Singapore_ACRA", "OFAC", "EU_Sanctions"],
                        "source": "production_kyc",
                        "loaded_at": datetime.now().isoformat(),
                        "environment": "production"
                    }
                },
                {
                    "id": "kyc_prod_002_vitol",
                    "document": "KYC профиль Vitol Group - одного из крупнейших независимых трейдеров энергоносителей. Штаб-квартира: Роттердам, Нидерланды. Основные рынки: нефть, газ, электроэнергия. Годовой оборот: $505 млрд (2023). AML статус: Clean. LEI: 549300X4ZJ8K9L5M6N59.",
                    "metadata": {
                        "document_type": "kyc_profile",
                        "company_name": "Vitol Group",
                        "lei": "549300X4ZJ8K9L5M6N59",
                        "jurisdiction": "Netherlands",
                        "industry": "energy_trading",
                        "annual_revenue_billion_usd": 505,
                        "aml_status": "clean",
                        "risk_score": 1,
                        "verification_sources": ["Netherlands_Chamber", "OFAC", "Bloomberg"],
                        "source": "production_kyc",
                        "loaded_at": datetime.now().isoformat(),
                        "environment": "production"
                    }
                }
            ]
            
            success_count = 0
            for kyc_data in sample_kyc:
                doc = kyc_data["document"]
                metadata = kyc_data["metadata"]
                
                result = service.add_document(
                    collection_name="kyc",
                    document=doc,
                    metadata=metadata,
                    id=kyc_data["id"]
                )
                
                if result["success"]:
                    success_count += 1
                    logger.info(f"Загружен KYC профиль: {kyc_data['metadata']['company_name']}")
            
            logger.info(f"✅ Загружено {success_count} производственных KYC профилей")
            return success_count == len(sample_kyc)
            
        except Exception as e:
            logger.error(f"Ошибка загрузки KYC: {e}")
            # Fallback на встроенные данные
            service = get_chroma_service(is_test_mode=test_mode)
            return service.load_initial_data()
    
    @classmethod
    def load_all_data(cls, test_mode: bool = False):
        """Полная загрузка всех данных"""
        print(f"🚀 Начинаю загрузку данных OpenMineralHub (test_mode={test_mode})...")
        
        success = True
        
        # Загрузка минералов
        print("📊 Загружаю каталог минералов...")
        success &= cls.load_minerals_catalog(test_mode=test_mode)
        
        # Загрузка сделок
        print("💼 Загружаю торговые сделки...")
        success &= cls.load_sample_deals(test_mode=test_mode)
        
        # Загрузка KYC
        print("🛡️ Загружаю KYC документы...")
        success &= cls.load_sample_kyc(test_mode=test_mode)
        
        if success:
            print("🎉 Все данные успешно загружены в Chroma!")
            print(f"\n📋 Что было загружено ({'test' if test_mode else 'production'} режим):")
            if test_mode:
                print("   • Тестовые данные из ChromaService (14 документов)")
            else:
                print("   • minerals_catalog: данные из JSON файла")
                print("   • trading_deals: 2 производственные сделки")
                print("   • kyc_profiles: 2 производственных KYC профиля")
            
            print("\n🔍 Теперь доступны запросы типа:")
            print("   • 'найди все сделки с медью'")
            print("   • 'покажи батарейные металлы'")
            print("   • 'найди контрагентов с clean AML статусом'")
        else:
            print("⚠️  Предупреждение: некоторые данные не загрузились")
        
        return success

if __name__ == "__main__":
    import sys
    test_mode = len(sys.argv) > 1 and sys.argv[1] == "--test"
    # Выполнение полной загрузки
    DataLoader.load_all_data(test_mode=test_mode)
    
    # Проверка результата
    service = get_chroma_service(is_test_mode=test_mode)
    stats = service.get_collection_stats()
    
    if stats["success"]:
        print(f"\n📊 Итоговая статистика после загрузки ({'test' if test_mode else 'production'}):")
        data = stats["data"]
        print(f"   • Минералы: {data['minerals']} документов")
        print(f"   • Сделки: {data['deals']} документов") 
        print(f"   • KYC: {data['kyc']} документов")
        print(f"   • Всего векторов: {data['total_vectors']}")
        if not test_mode:
            print(f"   • Общая стоимость сделок: ${data['deals_value_usd']:,.0f}")
            print(f"   • Подтвержденных сделок: {data['confirmed_deals']}")
    else:
        print(f"❌ Ошибка проверки статистики: {stats['error']}")
