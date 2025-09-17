import React from 'react';

const DealBasicsStep = ({ data, onChange, validationResults, dropdownData }) => {
  const handleInputChange = (field, value) => {
    onChange('dealBasics', { [field]: value });
  };

  return (
    <div className="step-container">
      <h2>Step 1: Deal Basics</h2>
      <p className="step-description">
        Enter the basic information about your trade deal
      </p>

      <div className="form-section">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="seller">Seller *</label>
            <input
              type="text"
              id="seller"
              value={data.seller}
              onChange={(e) => handleInputChange('seller', e.target.value)}
              placeholder="Seller name"
              readOnly
              className="readonly-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="buyer">Buyer *</label>
            <input
              type="text"
              id="buyer"
              value={data.buyer}
              onChange={(e) => handleInputChange('buyer', e.target.value)}
              placeholder="Enter buyer name"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="material">Material *</label>
            <select
              id="material"
              value={data.material}
              onChange={(e) => handleInputChange('material', e.target.value)}
              required
            >
              <option value="">Select material</option>
              {dropdownData.materials?.map((material, index) => (
                <option key={index} value={material}>{material}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="quantity">Quantity (MT) *</label>
            <input
              type="number"
              id="quantity"
              value={data.quantity}
              onChange={(e) => handleInputChange('quantity', e.target.value)}
              placeholder="Enter quantity"
              min="0"
              step="0.01"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="quantityTolerance">Quantity Tolerance (%) *</label>
            <input
              type="number"
              id="quantityTolerance"
              value={data.quantityTolerance}
              onChange={(e) => handleInputChange('quantityTolerance', e.target.value)}
              placeholder="Enter tolerance"
              min="0"
              max="50"
              step="0.1"
              required
            />
          </div>
        </div>
      </div>

      {/* AI Suggestions and Warnings */}
      {validationResults.suggestions && validationResults.suggestions.length > 0 && (
        <div className="validation-section suggestions">
          <h3>💡 AI Suggestions</h3>
          <ul>
            {validationResults.suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}

      {validationResults.warnings && validationResults.warnings.length > 0 && (
        <div className="validation-section warnings">
          <h3>⚠️ Warnings</h3>
          <ul>
            {validationResults.warnings.map((warning, index) => (
              <li key={index}>{warning}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DealBasicsStep;
