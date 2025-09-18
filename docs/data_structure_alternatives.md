# Структура данных для Business Confirmation Flow

В данном документе описывается комбинированный подход к структурированию данных для приложения Business Confirmation Flow, основанный на анализе документа `Full Stack Dev Test Task.docx`. Этот подход сочетает преимущества реляционных моделей для структурированных данных с гибкостью JSONB для полуструктурированных или динамических данных.

## Основные модели:

#### `Deal` (Сделка)
Основная модель для хранения общей информации о сделке, с использованием `JSONField` (который в PostgreSQL реализуется как `JSONB`) для некоторых полей.

| Поле                      | Тип данных (Django) | Описание                                                              |
| :------------------------ | :------------------ | :-------------------------------------------------------------------- |
| `id`                      | `AutoField`         | Уникальный идентификатор сделки                                       |
| `date_created`            | `DateTimeField`     | Дата создания записи о сделке                                         |
| `seller`                  | `ForeignKey` к `Company` | Продавец (ссылка на модель `Company`)                                 |
| `buyer`                   | `ForeignKey` к `Company` | Покупатель (ссылка на модель `Company`)                               |
| `material`                | `CharField`         | Тип материала (например, "Lead concentrate")                          |
| `quantity`                | `DecimalField`      | Количество (например, 1500)                                           |
| `quantity_unit`           | `CharField`         | Единица измерения количества (например, "dmt")                        |
| `quantity_tolerance_percent` | `DecimalField`      | Допуск по количеству в процентах (например, 10)                       |
| `delivery_term`           | `CharField`         | Условия доставки (например, "DAP")                                    |
| `delivery_point`          | `CharField`         | Пункт доставки (например, "ALASHANKOU")                               |
| `delivery_mode`           | `CharField`         | Способ доставки (например, "In big bags or in open railcars")         |
| `shipment_period_start`   | `DateField`         | Начало периода отгрузки                                               |
| `shipment_period_end`     | `DateField`         | Конец периода отгрузки                                                |
| `tc_value`                | `DecimalField`      | Стоимость TC (Treatment Charge)                                       |
| `tc_currency`             | `CharField`         | Валюта TC (например, "USD")                                           |
| `tc_unit`                 | `CharField`         | Единица измерения TC (например, "/dmt")                               |
| `rc_ag_value`             | `DecimalField`      | Стоимость RC Ag (Refining Charge Silver)                              |
| `rc_ag_currency`          | `CharField`         | Валюта RC Ag (например, "USD")                                        |
| `rc_ag_unit`              | `CharField`         | Единица измерения RC Ag (например, "/payable toz")                    |
| `no_transportation_credit` | `BooleanField`      | Отсутствие транспортного кредита                                      |
| `no_other_payables`       | `BooleanField`      | Отсутствие других платежей                                            |
| `prices_used`             | `TextField`         | Используемые цены (например, "At LME Lead Cash...")                   |
| `quotational_period`      | `CharField`         | Период котирования (например, "M+3, basis RWB shipped date")          |
| `payment_method`          | `CharField`         | Метод оплаты (например, "T/T")                                        |
| `prepayment_percent`      | `DecimalField`      | Процент предоплаты                                                    |
| `provisional_payment_percent` | `DecimalField`      | Процент промежуточного платежа                                        |
| `final_payment_description` | `TextField`         | Описание окончательного платежа                                       |
| `wsmd_final_location`     | `CharField`         | Место окончательного WSMD                                             |
| `wsmd_expense_sharing`    | `CharField`         | Распределение расходов WSMD (например, "50-50")                       |
| `surveyor_nominated_by`   | `CharField`         | Сюрвейер номинирован (например, "Buyer")                              |
| `surveyor_agreed_by`      | `CharField`         | Сюрвейер согласован (например, "Seller")                              |
| `assay_determination_method` | `CharField`         | Метод определения анализа (например, "Exchange on company letterhead") |
| `additional_terms`        | `JSONField`         | Дополнительные условия (хранятся как JSON-объект)                     |
| `quality_assay`           | `JSONField`         | Типичный анализ качества (хранится как JSON-объект)                   |

#### `Company` (Компания)
Модель для хранения информации о компаниях, аналогичная реляционной модели.

| Поле      | Тип данных (Django) | Описание                 |
| :-------- | :------------------ | :----------------------- |
| `id`      | `AutoField`         | Уникальный идентификатор |
| `name`    | `CharField`         | Название компании        |
| `contact_person` | `CharField`         | Контактное лицо          |
| `address` | `TextField`         | Адрес компании           |
| `type`    | `CharField`         | Тип компании (Seller/Buyer) |

### Структура `quality_assay` (JSONField):
Пример JSON-структуры для поля `quality_assay`:
```json
{
  "Zn": {"min": 9.0, "unit": "%"},
  "Pb": {"min": 65.0, "unit": "%"},
  "Cu": {"min": 0.2, "unit": "%"},
  "Au": {"min": 0.1, "unit": "g/t"},
  "Ag": {"min": 815.0, "unit": "g/t"},
  "Fe": {"min": 1.2, "max": 2.0, "unit": "%"},
  "SiO2": {"min": 0.1, "max": 0.15, "unit": "%"},
  "CaO": {"min": 0.4, "max": 0.8, "unit": "%"}
}
```
Каждый ключ представляет собой элемент, а его значение - объект с `min`, `max` (если применимо) и `unit`.

### Структура `additional_terms` (JSONField):
Пример JSON-структуры для поля `additional_terms`:
```json
{
  "clauses": [
    {"name": "Transportation Credit", "applies": false, "text": "No transportation credit to Buyer or Seller"},
    {"name": "Other Payables", "applies": false, "text": "No other payables shall apply. No other deductions shall apply subject to Material being in line with the declared typical assay"}
  ],
  "custom_terms": "Rest of terms and conditions to be mutually agreed."
}
```
Это позволяет хранить список именованных условий с их статусом применения и текстом, а также общее поле для произвольных "остальных условий".

### Преимущества:
*   **Гибкость:** Легко добавлять новые элементы анализа или дополнительные условия без изменения схемы базы данных.
*   **Производительность запросов:** PostgreSQL позволяет эффективно запрашивать данные внутри JSONB-полей.
*   **Сохранение реляционной целостности:** Основные связи и структурированные данные остаются в реляционных таблицах.

### Недостатки:
*   **Менее строгая валидация:** Валидация внутри JSONB-полей должна быть реализована на уровне приложения (Django).
*   **Сложность запросов:** Запросы к вложенным JSONB-данным могут быть сложнее, чем к обычным столбцам.
