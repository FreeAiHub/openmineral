"""
Business Confirmation Parser API
REST API для парсинга Business Confirmation документов
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import tempfile
import os
from pathlib import Path

# Добавляем путь к сервисам
import sys
sys.path.append(str(Path(__file__).parent.parent))

from services.bc_parser import BCParser, parse_bc_file

router = APIRouter()

@router.post("/parse-text")
async def parse_bc_text(text: str) -> Dict[str, Any]:
    """
    Парсинг Business Confirmation из текста
    """
    try:
        parser = BCParser()
        bc_data = parser.parse_text(text)
        result = parser.to_json(bc_data)
        
        return {
            "success": True,
            "message": "Business Confirmation успешно распарсен",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка парсинга: {str(e)}")

@router.post("/parse-file")
async def parse_bc_file_upload(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Парсинг Business Confirmation из загруженного файла
    """
    try:
        # Проверка типа файла
        if not file.filename.endswith(('.txt', '.docx', '.doc')):
            raise HTTPException(
                status_code=400, 
                detail="Поддерживаются только файлы .txt, .doc, .docx"
            )
        
        # Создание временного файла
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
            content = await file.read()
            
            # Для .txt файлов просто записываем содержимое
            if file.filename.endswith('.txt'):
                tmp_file.write(content)
            else:
                # Для .docx/.doc файлов нужна дополнительная обработка
                # Пока что просто декодируем как текст
                try:
                    text_content = content.decode('utf-8')
                    tmp_file.write(text_content.encode('utf-8'))
                except UnicodeDecodeError:
                    raise HTTPException(
                        status_code=400,
                        detail="Не удалось декодировать файл. Используйте .txt файл."
                    )
            
            tmp_file.flush()
            
            # Парсинг файла
            result = parse_bc_file(tmp_file.name)
            
            # Удаление временного файла
            os.unlink(tmp_file.name)
            
            return {
                "success": True,
                "message": f"Файл {file.filename} успешно распарсен",
                "filename": file.filename,
                "data": result
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

@router.get("/parse-example")
async def parse_example_bc() -> Dict[str, Any]:
    """
    Парсинг примера Business Confirmation
    """
    try:
        example_file = "data/bc_template_example.txt"
        
        if not os.path.exists(example_file):
            raise HTTPException(status_code=404, detail="Файл примера не найден")
        
        result = parse_bc_file(example_file)
        
        return {
            "success": True,
            "message": "Пример Business Confirmation распарсен",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка парсинга примера: {str(e)}")

@router.get("/parser-info")
async def get_parser_info() -> Dict[str, Any]:
    """
    Информация о парсере Business Confirmation
    """
    return {
        "parser_name": "OpenMineral BC Parser",
        "version": "1.0.0",
        "supported_formats": [".txt", ".docx", ".doc"],
        "extracted_fields": [
            "date",
            "seller", 
            "buyer",
            "material",
            "quantity",
            "delivery_terms",
            "shipment_period",
            "tc_rate",
            "rc_rate", 
            "pricing_basis",
            "quotational_period",
            "assay_data",
            "payment_terms",
            "wsmd_terms"
        ],
        "description": "Парсер для извлечения структурированных данных из Business Confirmation документов в сфере торговли минеральным сырьем"
    }
