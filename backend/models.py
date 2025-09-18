from django.db import models
from django.contrib.postgres.fields import JSONField # Для PostgreSQL JSONBField

class Company(models.Model):
    """
    Модель для хранения информации о компаниях (продавцах/покупателях).
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Название компании")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Контактное лицо")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес компании")
    # Дополнительные поля, если необходимо
    type = models.CharField(max_length=50, choices=[('Seller', 'Seller'), ('Buyer', 'Buyer')], verbose_name="Тип компании")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

class Deal(models.Model):
    """
    Модель для хранения общей информации о сделке.
    Использует JSONField для quality_assay и additional_terms для гибкости.
    """
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    seller = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='deals_as_seller', verbose_name="Продавец")
    buyer = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='deals_as_buyer', verbose_name="Покупатель")
    
    material = models.CharField(max_length=255, verbose_name="Тип материала")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество")
    quantity_unit = models.CharField(max_length=50, verbose_name="Единица измерения количества")
    quantity_tolerance_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Допуск по количеству (%)")
    
    delivery_term = models.CharField(max_length=100, verbose_name="Условия доставки")
    delivery_point = models.CharField(max_length=255, verbose_name="Пункт доставки")
    delivery_mode = models.CharField(max_length=255, verbose_name="Способ доставки")
    
    shipment_period_start = models.DateField(verbose_name="Начало периода отгрузки")
    shipment_period_end = models.DateField(verbose_name="Конец периода отгрузки")
    
    tc_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость TC")
    tc_currency = models.CharField(max_length=10, verbose_name="Валюта TC")
    tc_unit = models.CharField(max_length=50, verbose_name="Единица измерения TC")
    
    rc_ag_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость RC Ag")
    rc_ag_currency = models.CharField(max_length=10, verbose_name="Валюта RC Ag")
    rc_ag_unit = models.CharField(max_length=50, verbose_name="Единица измерения RC Ag")
    
    no_transportation_credit = models.BooleanField(default=False, verbose_name="Без транспортного кредита")
    no_other_payables = models.BooleanField(default=False, verbose_name="Без других платежей")
    
    prices_used = models.TextField(verbose_name="Используемые цены")
    quotational_period = models.CharField(max_length=255, verbose_name="Период котирования")
    
    payment_method = models.CharField(max_length=100, verbose_name="Метод оплаты")
    prepayment_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Процент предоплаты")
    provisional_payment_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Процент промежуточного платежа")
    final_payment_description = models.TextField(blank=True, null=True, verbose_name="Описание окончательного платежа")
    
    wsmd_final_location = models.CharField(max_length=255, verbose_name="Место окончательного WSMD")
    wsmd_expense_sharing = models.CharField(max_length=100, verbose_name="Распределение расходов WSMD")
    surveyor_nominated_by = models.CharField(max_length=100, verbose_name="Сюрвейер номинирован")
    surveyor_agreed_by = models.CharField(max_length=100, verbose_name="Сюрвейер согласован")
    
    assay_determination_method = models.CharField(max_length=255, verbose_name="Метод определения анализа")
    
    # JSONField для гибких данных
    additional_terms = JSONField(blank=True, null=True, verbose_name="Дополнительные условия")
    quality_assay = JSONField(blank=True, null=True, verbose_name="Типичный анализ качества")

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

    def __str__(self):
        return f"Deal {self.id} - {self.material}"
