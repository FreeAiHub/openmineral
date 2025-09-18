"""
Business Confirmation Parser
Простой MVP для извлечения данных из Business Confirmation документов
"""

import re
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel

class AssayData(BaseModel):
    """Модель для данных анализа"""
    element: str
    value: str
    unit: str

class BCData(BaseModel):
    """Структурированные данные Business Confirmation"""
    date: Optional[str] = None
    seller: Optional[str] = None
    buyer: Optional[str] = None
    material: Optional[str] = None
    quantity: Optional[str] = None
    delivery_terms: Optional[str] = None
    shipment_period: Optional[str] = None
    tc_rate: Optional[str] = None
    rc_rate: Optional[str] = None
    pricing_basis: Optional[str] = None
    quotational_period: Optional[str] = None
    assay_data: List[AssayData] = []
    payment_terms: Dict[str, str] = {}
    wsmd_terms: Optional[str] = None
    
class BCParser:
    """Парсер Business Confirmation документов"""
    
    def __init__(self):
        self.patterns = {
            'date': r'(\w+\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4})',
            'seller': r'Seller:\s*([^\n]+)',
            'buyer': r'Buyer:\s*([^\n]+)',
            'material': r'Material:\s*\n([^\n]+)',
            'quantity': r'Quantity:\s*\n([^\n]+)',
            'delivery': r'Delivery:\s*\n([^\n]+(?:\n[^\n]+)*?)(?=\n\nShipment:|\nShipment:)',
            'shipment': r'Shipment:\s*\n([^\n]+)',
            'tc_rate': r'TC\s+USD\s+([\d.,]+)/dmt',
            'rc_rate': r'RC\s+\w+\s+USD\s+([\d.,]+)\s*/\s*payable\s+toz',
            'pricing': r'Prices used:\s*\n([^\n]+)',
            'quotational': r'Quotational Period:\s*\n([^\n]+)',
            'wsmd': r'WSMD:\s*\n([^\n]+(?:\n[^\n]+)*?)(?=\n\nAssay determination:|\nAssay determination:)',
        }
        
        self.assay_pattern = r'(\w+):\s*([\d.,\s%-]+(?:g/t)?)'
        
    def parse_text(self, text: str) -> BCData:
        """Основной метод парсинга текста"""
        bc_data = BCData()
        
        # Очистка текста
        text = self._clean_text(text)
        
        # Извлечение основных полей
        bc_data.date = self._extract_field(text, 'date')
        bc_data.seller = self._extract_field(text, 'seller')
        bc_data.buyer = self._extract_field(text, 'buyer')
        bc_data.material = self._extract_field(text, 'material')
        bc_data.quantity = self._extract_field(text, 'quantity')
        bc_data.delivery_terms = self._extract_field(text, 'delivery')
        bc_data.shipment_period = self._extract_field(text, 'shipment')
        bc_data.tc_rate = self._extract_field(text, 'tc_rate')
        bc_data.rc_rate = self._extract_field(text, 'rc_rate')
        bc_data.pricing_basis = self._extract_field(text, 'pricing')
        bc_data.quotational_period = self._extract_field(text, 'quotational')
        bc_data.wsmd_terms = self._extract_field(text, 'wsmd')
        
        # Извлечение данных анализа
        bc_data.assay_data = self._extract_assay_data(text)
        
        # Извлечение условий платежа
        bc_data.payment_terms = self._extract_payment_terms(text)
        
        return bc_data
    
    def _clean_text(self, text: str) -> str:
        """Очистка и нормализация текста"""
        # Сохраняем переносы строк для правильного парсинга
        text = re.sub(r'\r\n', '\n', text)  # Нормализация переносов
        text = re.sub(r'\r', '\n', text)
        return text.strip()
    
    def _extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Извлечение конкретного поля"""
        if field_name not in self.patterns:
            return None
            
        pattern = self.patterns[field_name]
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            result = match.group(1).strip()
            # Очистка от лишних символов
            result = re.sub(r'\s+', ' ', result)
            return result
        
        return None
    
    def _extract_assay_data(self, text: str) -> List[AssayData]:
        """Извлечение данных химического анализа"""
        assay_data = []
        
        # Поиск секции Typical Assay
        assay_section = re.search(r'Typical Assay:\s*\n(.+?)(?=\n\n|\nQuantity:)', text, re.DOTALL | re.IGNORECASE)
        
        if assay_section:
            assay_text = assay_section.group(1)
            
            # Извлечение отдельных элементов
            matches = re.findall(self.assay_pattern, assay_text)
            
            for element, value in matches:
                # Определение единицы измерения
                unit = '%'
                if 'g/t' in value:
                    unit = 'g/t'
                    value = value.replace('g/t', '').strip()
                
                assay_data.append(AssayData(
                    element=element.strip(),
                    value=value.strip(),
                    unit=unit
                ))
        
        return assay_data
    
    def _extract_payment_terms(self, text: str) -> Dict[str, str]:
        """Извлечение условий платежа"""
        payment_terms = {}
        
        # Поиск секции Payment
        payment_section = re.search(r'Payment:\s*\n(.+?)(?=\n\n|\nWSMD:)', text, re.DOTALL | re.IGNORECASE)
        
        if payment_section:
            payment_text = payment_section.group(1)
            
            # Извлечение предоплаты
            prepayment = re.search(r'Prepayment:\s*(.+?)(?=\n|Provisional)', payment_text, re.IGNORECASE)
            if prepayment:
                payment_terms['prepayment'] = prepayment.group(1).strip()
            
            # Извлечение промежуточного платежа
            provisional = re.search(r'Provisional payment:\s*(.+?)(?=\n|Final)', payment_text, re.IGNORECASE)
            if provisional:
                payment_terms['provisional'] = provisional.group(1).strip()
            
            # Извлечение финального платежа
            final = re.search(r'Final Payment:\s*(.+?)(?=\n|$)', payment_text, re.IGNORECASE)
            if final:
                payment_terms['final'] = final.group(1).strip()
        
        return payment_terms
    
    def to_json(self, bc_data: BCData) -> Dict[str, Any]:
        """Конвертация в JSON формат"""
        return {
            "document_type": "business_confirmation",
            "parsed_at": datetime.now().isoformat(),
            "data": {
                "basic_info": {
                    "date": bc_data.date,
                    "seller": bc_data.seller,
                    "buyer": bc_data.buyer,
                    "material": bc_data.material
                },
                "commercial_terms": {
                    "quantity": bc_data.quantity,
                    "delivery_terms": bc_data.delivery_terms,
                    "shipment_period": bc_data.shipment_period,
                    "tc_rate": bc_data.tc_rate,
                    "rc_rate": bc_data.rc_rate,
                    "pricing_basis": bc_data.pricing_basis,
                    "quotational_period": bc_data.quotational_period
                },
                "quality_specs": {
                    "assay_data": [
                        {
                            "element": assay.element,
                            "value": assay.value,
                            "unit": assay.unit
                        }
                        for assay in bc_data.assay_data
                    ]
                },
                "payment_terms": bc_data.payment_terms,
                "operational_terms": {
                    "wsmd": bc_data.wsmd_terms
                }
            }
        }

# Пример использования
def parse_bc_file(file_path: str) -> Dict[str, Any]:
    """Парсинг BC файла"""
    parser = BCParser()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    bc_data = parser.parse_text(text)
    return parser.to_json(bc_data)

if __name__ == "__main__":
    # Тест парсера
    result = parse_bc_file("data/bc_template_example.txt")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
