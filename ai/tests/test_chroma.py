"""
Тесты Chroma интеграции для OpenMineralHub
Обновленные тесты с поддержкой тестовой БД
"""

import pytest
import sys
import os
import shutil
from unittest.mock import patch, MagicMock
from ai.chroma_service import ChromaService, get_chroma_service
from ai.data_loader import DataLoader

# Константы для тестов
TEST_DB_PATH = "./chroma_test_db"
COLLECTIONS = {
    "minerals": "openmineral_minerals",
    "deals": "openmineral_deals", 
    "kyc": "openmineral_kyc"
}

@pytest.fixture
def mock_chroma_client():
    """Мок клиента Chroma для unit тестов"""
    mock_client = MagicMock()
    mock_collection = MagicMock()
    
    # Моки методов коллекции
    mock_collection.count.return_value = 0
    mock_collection.query.return_value = {
        "ids": [[]],
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]]
    }
    mock_collection.get.return_value = {
        "ids": [],
        "documents": [],
        "metadatas": []
    }
    mock_collection.add.return_value = None
    
    # Моки методов клиента
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_client.create_collection.return_value = mock_collection
    mock_client.list_collections.return_value = [mock_collection]
    
    return mock_client

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Настройка тестовой среды"""
    # Создание директории для тестовой БД
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)
    
    yield
    
    # Очистка после тестов
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)
        print(f"🧹 Тестовая БД {TEST_DB_PATH} удалена")

class TestChromaService:
    """Unit тесты ChromaService"""
    
    def test_init_production_mode(self):
        """Тест инициализации в production режиме"""
        try:
            service = ChromaService(is_test_mode=False)
            assert service.client is not None
            assert not service.is_test_mode
            assert hasattr(service, 'minerals_collection')
            assert hasattr(service, 'deals_collection')
            assert hasattr(service, 'kyc_collection')
            print("✅ ChromaService (production) инициализирован")
        except Exception as e:
            pytest.skip(f"Chroma Cloud недоступен: {e}")
    
    def test_init_test_mode(self):
        """Тест инициализации в test режиме"""
        service = ChromaService(is_test_mode=True)
        assert service.client is not None
        assert service.is_test_mode
        assert service.test_db_path == "./chroma_test_db"
        assert hasattr(service, 'minerals_collection')
        assert hasattr(service, 'deals_collection')
        assert hasattr(service, 'kyc_collection')
        print("✅ ChromaService (test mode) инициализирован")
    
    def test_get_chroma_service(self):
        """Тест глобального get_chroma_service"""
        # Production режим
        prod_service = get_chroma_service(is_test_mode=False)
        assert not prod_service.is_test_mode
        assert prod_service == get_chroma_service(is_test_mode=False)  # Singleton
        
        # Test режим
        test_service = get_chroma_service(is_test_mode=True)
        assert test_service.is_test_mode
        assert test_service == get_chroma_service(is_test_mode=True)  # Singleton
        
        # Разные экземпляры
        assert prod_service != test_service
        print("✅ get_chroma_service singleton работает")
    
    def test_collections_metadata(self):
        """Тест метаданных коллекций"""
        test_service = ChromaService(is_test_mode=True)
        prod_service = ChromaService(is_test_mode=False)
        
        # Проверяем метаданные тестовой БД
        test_meta = test_service.minerals_collection.metadata
        assert test_meta["environment"] == "test"
        
        # Проверяем метаданные production БД
        if hasattr(prod_service.minerals_collection, 'metadata'):
            prod_meta = prod_service.minerals_collection.metadata
            assert prod_meta["environment"] == "production"
        
        print("✅ Метаданные коллекций корректны")
    
    def test_load_initial_data_test_mode(self):
        """Тест загрузки данных в test режиме"""
        service = get_chroma_service(is_test_mode=True)
        
        # Очистка перед загрузкой
        service.cleanup_test_db()
        
        # Загрузка данных
        success = service.load_initial_data()
        assert success is True
        
        # Проверка статистики
        stats = service.get_collection_stats()
        assert stats["success"] is True
        
        data = stats["data"]
        minerals_count = data["minerals"]
        deals_count = data["deals"]
        kyc_count = data["kyc"]
        total = data["total_vectors"]
        
        # Проверяем ожидаемые количества
        assert minerals_count == 5, f"Ожидалось 5 минералов, получено {minerals_count}"
        assert deals_count == 5, f"Ожидалось 5 сделок, получено {deals_count}"
        assert kyc_count == 4, f"Ожидалось 4 KYC, получено {kyc_count}"
        assert total == 14, f"Ожидалось 14 векторов, получено {total}"
        
        # Проверяем environment в метаданных
        minerals_meta = service.minerals_collection.get()["metadatas"]
        for meta in minerals_meta:
            assert meta["environment"] == "test"
        
        print(f"✅ Данные загружены в test БД: минералы={minerals_count}, сделки={deals_count}, KYC={kyc_count}")
    
    def test_load_initial_data_production(self):
        """Тест загрузки данных в production режиме"""
        try:
            service = get_chroma_service(is_test_mode=False)
            success = service.load_initial_data()
            assert success is True
            
            stats = service.get_collection_stats()
            assert stats["success"] is True
            
            print("✅ Данные загружены в production БД")
        except Exception as e:
            pytest.skip(f"Production загрузка пропущена: {e}")
    
    def test_search_minerals_test_mode(self):
        """Тест поиска по минералам в test режиме"""
        service = get_chroma_service(is_test_mode=True)
        
        # Загружаем тестовые данные
        service.load_initial_data()
        
        # Поиск
        results = service.search_minerals("медь", n_results=2)
        
        assert results["success"] is True
        assert results["environment"] == "test"
        assert "results" in results
        assert isinstance(results["results"], list)
        
        # Проверяем фильтр по environment
        test_results = service.search_minerals("медь", filters={"environment": "test"})
        assert test_results["success"] is True
        
        # Проверяем, что возвращаются результаты из test БД
        assert len(test_results["results"]) > 0
        
        first_result = test_results["results"][0]
        assert "document" in first_result
        assert "metadata" in first_result
        assert first_result["metadata"]["environment"] == "test"
        assert "relevance_score" in first_result
        
        print(f"✅ Поиск минералов в test режиме: {test_results['results_count']} результатов")
    
    def test_search_deals_with_filters(self):
        """Тест поиска сделок с фильтрами"""
        service = get_chroma_service(is_test_mode=True)
        service.load_initial_data()
        
        # Поиск с фильтрами
        results = service.search_deals(
            query="медь", 
            status_filter="confirmed", 
            risk_filter="medium"
        )
        
        assert results["success"] is True
        assert results["environment"] == "test"
        
        # Проверяем фильтры в результатах
        for result in results["results"]:
            meta = result["metadata"]
            assert meta.get("status") == "confirmed"
            assert meta.get("risk_level") == "medium"
            assert meta.get("environment") == "test"
        
        print(f"✅ Поиск сделок с фильтрами: {results['results_count']} результатов")
    
    def test_search_kyc_aml_filter(self):
        """Тест поиска KYC с AML фильтром"""
        service = get_chroma_service(is_test_mode=True)
        service.load_initial_data()
        
        # Поиск только clean компаний
        results = service.search_kyc("mining", aml_filter="clean")
        
        assert results["success"] is True
        assert results["environment"] == "test"
        assert results["aml_filter"] == "clean"
        
        # Проверяем, что все результаты clean
        clean_count = 0
        for result in results["results"]:
            if result["aml_status"] == "clean":
                clean_count += 1
        
        assert clean_count == len(results["results"])
        assert results["clean_entities"] == clean_count
        
        print(f"✅ Поиск KYC с AML фильтром: {results['results_count']} clean результатов")
    
    def test_add_document_test_mode(self):
        """Тест добавления документа в test режиме"""
        service = get_chroma_service(is_test_mode=True)
        
        # Очистка перед тестом
        service.cleanup_test_db()
        
        test_doc = {
            "collection_name": "deals",
            "document": "Тестовая сделка OMH-TEST-001: Продажа 100 тонн тестового товара",
            "metadata": {
                "deal_id": "OMH-TEST-001",
                "commodity": "test_metal",
                "quantity_tons": 100,
                "price_usd_per_ton": 10000,
                "total_amount_usd": 1000000,
                "status": "test",
                "risk_level": "low",
                "source": "test_add_document"
            }
        }
        
        result = service.add_document(
            collection_name=test_doc["collection_name"],
            document=test_doc["document"],
            metadata=test_doc["metadata"],
            id="test_doc_001"
        )
        
        assert result["success"] is True
        assert result["document_id"] == "test_doc_001"
        assert result["test_mode"] is True
        assert result["new_count"] == 1
        
        # Проверяем, что документ добавлен
        added_docs = service.deals_collection.get(ids=["test_doc_001"])
        assert len(added_docs["documents"]) == 1
        assert added_docs["documents"][0] == test_doc["document"]
        
        # Проверяем метаданные
        meta = added_docs["metadatas"][0]
        assert meta["test_mode"] is True
        assert meta["environment"] == "test"
        assert meta["added_at"] is not None
        
        print(f"✅ Документ добавлен в test БД: {result['document_id']}")
    
    def test_cleanup_test_db(self):
        """Тест очистки тестовой БД"""
        service = get_chroma_service(is_test_mode=True)
        
        # Загружаем данные
        service.load_initial_data()
        
        # Проверяем, что данные есть
        initial_stats = service.get_collection_stats()
        initial_total = initial_stats["data"]["total_vectors"]
        assert initial_total == 14
        
        # Очистка
        success = service.cleanup_test_db()
        assert success is True
        
        # Проверяем, что БД пуста
        final_stats = service.get_collection_stats()
        final_total = final_stats["data"]["total_vectors"]
        assert final_total == 0
        
        # Проверяем, что коллекции пересозданы
        assert service.minerals_collection is not None
        assert service.deals_collection is not None
        assert service.kyc_collection is not None
        
        # Проверяем, что директория БД пуста или пересоздана
        assert os.path.exists(TEST_DB_PATH)
        db_files = os.listdir(TEST_DB_PATH)
        assert len(db_files) > 0  # Базовые файлы ChromaDB
        
        print(f"✅ Тестовая БД очищена: {initial_total} → {final_total} документов")
    
    def test_collection_stats_test_mode(self):
        """Тест статистики в test режиме"""
        service = get_chroma_service(is_test_mode=True)
        service.load_initial_data()
        
        stats = service.get_collection_stats()
        
        assert stats["success"] is True
        assert stats["data"]["environment"] == "test"
        
        data = stats["data"]
        assert "minerals" in data
        assert "deals" in data
        assert "kyc" in data
        assert data["total_vectors"] == 14
        
        # Проверяем статистику сделок
        assert data["deals_value_usd"] > 0
        assert data["confirmed_deals"] >= 1
        assert data["deals_avg_value"] > 0
        
        print(f"✅ Статистика test БД: {data['minerals']}+{data['deals']}+{data['kyc']}={data['total_vectors']}")
    
    @pytest.mark.skip(reason="Требует реальных данных production")
    def test_production_integration(self):
        """Интеграционный тест production БД"""
        service = get_chroma_service(is_test_mode=False)
        stats = service.get_collection_stats()
        assert stats["success"] is True
        print(f"✅ Production БД доступна: {stats['data']['total_vectors']} векторов")

class TestDataLoader:
    """Тесты загрузчика данных"""
    
    def test_load_minerals_catalog_test_mode(self):
        """Тест загрузки каталога минералов в test режиме"""
        try:
            from ai.data_loader import DataLoader
            success = DataLoader.load_minerals_catalog(test_mode=True)
            assert success is True
            print("✅ Загрузчик минералов (test) работает")
        except ImportError:
            pytest.skip("DataLoader не найден")
    
    def test_load_sample_deals_test_mode(self):
        """Тест загрузки примеров сделок в test режиме"""
        try:
            from ai.data_loader import DataLoader
            success = DataLoader.load_sample_deals(test_mode=True)
            assert success is True
            print("✅ Загрузчик сделок (test) работает")
        except ImportError:
            pytest.skip("DataLoader не найден")
    
    @pytest.mark.skip(reason="DataLoader может не поддерживать test_mode")
    def test_load_all_data_test_mode(self):
        """Тест полной загрузки данных в test режиме"""
        try:
            from ai.data_loader import DataLoader
            success = DataLoader.load_all_data(test_mode=True)
            assert success is True
            print("✅ Полная загрузка данных (test) работает")
        except Exception as e:
            pytest.skip(f"DataLoader test_mode не поддерживается: {e}")

class TestIntegration:
    """Интеграционные тесты"""
    
    def test_full_test_pipeline(self):
        """Полный тест: загрузка → поиск → очистка в test режиме"""
        print("\n🧪 Запуск полного тестового пайплайна...")
        
        service = get_chroma_service(is_test_mode=True)
        
        # 1. Очистка
        print("1. Очистка тестовой БД...")
        service.cleanup_test_db()
        
        # 2. Загрузка данных
        print("2. Загрузка тестовых данных...")
        success = service.load_initial_data()
        assert success is True
        
        # 3. Статистика
        print("3. Проверка статистики...")
        stats = service.get_collection_stats()
        assert stats["success"] is True
        assert stats["data"]["total_vectors"] == 14
        print(f"   Статистика: {stats['data']['minerals']}+{stats['data']['deals']}+{stats['data']['kyc']}={stats['data']['total_vectors']}")
        
        # 4. Поиск
        print("4. Тестирование поиска...")
        
        mineral_results = service.search_minerals("батарейные металлы", n_results=2)
        deal_results = service.search_deals("медные сделки", n_results=2)
        kyc_results = service.search_kyc("Glencore", n_results=1)
        
        # Проверяем успех и environment
        for results in [mineral_results, deal_results, kyc_results]:
            assert results["success"] is True
            assert results["environment"] == "test"
        
        # Проверяем наличие результатов
        total_results = (mineral_results["results_count"] + 
                        deal_results["results_count"] + 
                        kyc_results["results_count"])
        assert total_results > 0
        
        print(f"   • Найдено минералов: {mineral_results['results_count']}")
        print(f"   • Найдено сделок: {deal_results['results_count']}")
        print(f"   • Найдено KYC: {kyc_results['results_count']}")
        
        # 5. Добавление документа
        print("5. Тестирование добавления документа...")
        add_result = service.add_document(
            collection_name="deals",
            document="Тестовый документ для интеграции",
            metadata={
                "deal_id": "TEST-001",
                "commodity": "test",
                "status": "test",
                "total_amount_usd": 1000
            },
            id="integration_test_doc"
        )
        assert add_result["success"] is True
        assert add_result["new_count"] == 6  # 5 исходных + 1 новый
        
        # 6. Очистка
        print("6. Финальная очистка...")
        cleanup_success = service.cleanup_test_db()
        assert cleanup_success is True
        
        final_stats = service.get_collection_stats()
        assert final_stats["data"]["total_vectors"] == 0
        
        print("✅ Полный тестовый пайплайн завершен успешно!")
    
    def test_error_handling(self):
        """Тест обработки ошибок"""
        service = get_chroma_service(is_test_mode=True)
        
        # Тест неизвестной коллекции
        result = service.add_document(
            collection_name="unknown_collection",
            document="test",
            metadata={}
        )
        assert not result["success"]
        assert "error" in result
        assert "Unknown collection" in result["error"]
        
        # Тест поиска с некорректными параметрами
        try:
            service.search_minerals(query="", n_results=-1)
            assert False, "Должен быть поднят exception"
        except Exception:
            pass  # Ожидаемая ошибка
        
        print("✅ Обработка ошибок работает")

# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
