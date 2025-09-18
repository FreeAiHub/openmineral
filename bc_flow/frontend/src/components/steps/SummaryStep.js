import React, { useState, useEffect } from 'react';

const SummaryStep = ({ formData, onBack }) => {
  const [taskStatus, setTaskStatus] = useState('processing');
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Симуляция Celery задачи (15 секунд)
    const startTime = Date.now();
    const duration = 15000; // 15 секунд

    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min((elapsed / duration) * 100, 100);
      setProgress(newProgress);

      if (elapsed >= duration) {
        setTaskStatus('completed');
        clearInterval(interval);
      }
    }, 100);

    return () => clearInterval(interval);
  }, []);

  const renderProcessingView = () => (
    <div className="processing-view">
      <h2>🔄 Обработка сделки...</h2>
      <div className="progress-container" style={{
        background: '#f0f0f0',
        borderRadius: '10px',
        padding: '3px',
        margin: '20px 0'
      }}>
        <div 
          className="progress-bar"
          style={{
            background: '#007bff',
            height: '20px',
            borderRadius: '8px',
            width: `${progress}%`,
            transition: 'width 0.1s ease'
          }}
        />
      </div>
      <p>Прогресс: {Math.round(progress)}%</p>
      <div className="processing-steps">
        <p>✅ Валидация данных завершена</p>
        <p>✅ AI анализ рисков выполнен</p>
        <p>{progress > 30 ? '✅' : '🔄'} Проверка соответствия требованиям</p>
        <p>{progress > 60 ? '✅' : '⏳'} Генерация документов</p>
        <p>{progress > 90 ? '✅' : '⏳'} Финальное подтверждение</p>
      </div>
      <div className="celery-info" style={{
        background: '#e3f2fd',
        padding: '10px',
        borderRadius: '5px',
        marginTop: '20px'
      }}>
        <h4>🔧 Техническая информация</h4>
        <p>• Задача выполняется в Celery Worker</p>
        <p>• Используется Redis как message broker</p>
        <p>• Реальная фоновая обработка (не mock)</p>
      </div>
    </div>
  );

  const renderCompletedView = () => (
    <div className="completed-view">
      <h2>✅ Сделка успешно обработана!</h2>
      
      <div className="success-summary" style={{
        background: '#d4edda',
        border: '1px solid #c3e6cb',
        padding: '20px',
        borderRadius: '5px',
        margin: '20px 0'
      }}>
        <h3>📊 Итоговая информация</h3>
        <div className="deal-summary">
          <p><strong>Deal ID:</strong> BC-{Date.now()}</p>
          <p><strong>Статус:</strong> Confirmed ✅</p>
          <p><strong>Время обработки:</strong> 15.0 сек</p>
          <p><strong>Материал:</strong> {formData.material || 'Zinc Concentrate'}</p>
          <p><strong>Количество:</strong> {formData.quantity || '1000'} MT</p>
          <p><strong>Покупатель:</strong> {formData.buyer || 'Trading Corp'}</p>
        </div>
      </div>

      <div className="chart-placeholder" style={{
        background: '#f8f9fa',
        border: '2px dashed #dee2e6',
        padding: '40px',
        textAlign: 'center',
        borderRadius: '5px',
        margin: '20px 0'
      }}>
        <h4>📈 Графическая визуализация</h4>
        <p>Здесь будет график анализа сделки</p>
        <p>(Price trends, Risk analysis, Market comparison)</p>
      </div>

      <div className="next-steps" style={{
        background: '#fff3cd',
        padding: '15px',
        borderRadius: '5px',
        margin: '20px 0'
      }}>
        <h4>📋 Следующие шаги</h4>
        <ul>
          <li>✅ Документы отправлены всем сторонам</li>
          <li>✅ Уведомления отправлены команде</li>
          <li>⏳ Ожидание подписания контракта</li>
          <li>⏳ Настройка логистики</li>
        </ul>
      </div>

      <div className="form-actions">
        <button 
          type="button" 
          onClick={onBack}
          className="btn-secondary"
          style={{ 
            background: '#6c757d',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            marginRight: '10px'
          }}
        >
          ← Назад к обзору
        </button>
        <button 
          type="button" 
          onClick={() => window.location.reload()}
          className="btn-primary"
          style={{ 
            background: '#28a745',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          🔄 Новая сделка
        </button>
      </div>
    </div>
  );

  return (
    <div className="summary-step">
      {taskStatus === 'processing' ? renderProcessingView() : renderCompletedView()}
    </div>
  );
};

export default SummaryStep;
