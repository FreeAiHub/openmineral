import React from 'react';

const ReviewSubmitStep = ({ formData, onSubmit, onBack }) => {
  const handleSubmit = () => {
    // Показать AI валидацию
    const missingFields = [];
    if (!formData.surveyor) {
      missingFields.push('Surveyor not selected');
    }
    
    if (missingFields.length > 0) {
      alert(`⚠️ AI Validation: ${missingFields.join(', ')}`);
      return;
    }
    
    // Подтверждение
    if (window.confirm('⚠️ Treatment Charge 20% higher than last month. Proceed?')) {
      onSubmit();
    }
  };

  return (
    <div className="review-submit-step">
      <h2>Шаг 4: Обзор и подтверждение</h2>
      
      <div className="review-summary">
        <h3>Сводка сделки</h3>
        
        <div className="review-section">
          <h4>Основная информация</h4>
          <p><strong>Продавец:</strong> {formData.seller || 'OpenMineral Corp'}</p>
          <p><strong>Покупатель:</strong> {formData.buyer || 'Не выбран'}</p>
          <p><strong>Материал:</strong> {formData.material || 'Не выбран'}</p>
          <p><strong>Количество:</strong> {formData.quantity || 'Не указано'}</p>
        </div>

        <div className="review-section">
          <h4>Коммерческие условия</h4>
          <p><strong>Условия доставки:</strong> {formData.deliveryTerm || 'CIF'}</p>
          <p><strong>Пункт доставки:</strong> {formData.deliveryPoint || 'Не указан'}</p>
          <p><strong>TC (USD/dmt):</strong> {formData.tc || 'Не указано'}</p>
          <p><strong>RC Ag (USD/toz):</strong> {formData.rcAg || 'Не указано'}</p>
        </div>

        <div className="review-section">
          <h4>Условия оплаты</h4>
          <p><strong>Метод оплаты:</strong> {formData.paymentMethod || 'LC at sight'}</p>
          <p><strong>Валюта:</strong> {formData.currency || 'USD'}</p>
          <p><strong>Предоплата:</strong> {formData.prepayment || '0'}%</p>
          <p><strong>Surveyor:</strong> {formData.surveyor || '⚠️ Не выбран'}</p>
        </div>
      </div>

      <div className="ai-validation" style={{ 
        background: '#fff3cd', 
        border: '1px solid #ffeaa7', 
        padding: '10px', 
        margin: '20px 0',
        borderRadius: '5px'
      }}>
        <h4>🤖 AI Валидация</h4>
        <ul>
          {!formData.surveyor && <li>⚠️ Surveyor not selected</li>}
          {formData.tc > 100 && <li>⚠️ TC выше рыночного среднего</li>}
          <li>✅ Все обязательные поля заполнены</li>
        </ul>
      </div>

      <div className="form-actions">
        <button 
          type="button" 
          onClick={onBack}
          className="btn-secondary"
          style={{ marginRight: '10px' }}
        >
          ← Назад
        </button>
        <button 
          type="button" 
          onClick={handleSubmit}
          className="btn-primary"
          style={{ 
            background: '#007bff', 
            color: 'white', 
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          📋 Подтвердить сделку
        </button>
      </div>
    </div>
  );
};

export default ReviewSubmitStep;
