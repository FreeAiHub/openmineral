import React from 'react';

const PaymentTermsStep = ({ data, onChange, validationResults, dropdownData }) => {
  const handleInputChange = (field, value) => {
    onChange('paymentTerms', { [field]: value });
  };

  return (
    <div className="step-container">
      <h2>Step 3: Payment Terms</h2>
      <p className="step-description">
        Define payment method, stages, and surveyor details for the transaction
      </p>

      <div className="form-section">
        <h3>Payment Method</h3>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="paymentMethod">Payment Method *</label>
            <select
              id="paymentMethod"
              value={data.paymentMethod}
              onChange={(e) => handleInputChange('paymentMethod', e.target.value)}
              required
            >
              <option value="">Select payment method</option>
              <option value="T/T">Telegraphic Transfer (T/T)</option>
              <option value="L/C">Letter of Credit (L/C)</option>
              <option value="D/P">Documents against Payment (D/P)</option>
              <option value="D/A">Documents against Acceptance (D/A)</option>
              <option value="Open Account">Open Account</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="currency">Currency *</label>
            <select
              id="currency"
              value={data.currency}
              onChange={(e) => handleInputChange('currency', e.target.value)}
              required
            >
              {dropdownData.currencies?.map((currency, index) => (
                <option key={index} value={currency}>{currency}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3>Payment Stages</h3>
        <p className="step-subdescription">Total must equal 100%</p>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="prepaymentPercentage">Prepayment % *</label>
            <input
              type="number"
              id="prepaymentPercentage"
              value={data.prepaymentPercentage}
              onChange={(e) => handleInputChange('prepaymentPercentage', parseInt(e.target.value) || 0)}
              placeholder="0-100"
              min="0"
              max="100"
              step="1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="provisionalPercentage">Provisional % *</label>
            <input
              type="number"
              id="provisionalPercentage"
              value={data.provisionalPercentage}
              onChange={(e) => handleInputChange('provisionalPercentage', parseInt(e.target.value) || 0)}
              placeholder="0-100"
              min="0"
              max="100"
              step="1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="finalPercentage">Final % *</label>
            <input
              type="number"
              id="finalPercentage"
              value={data.finalPercentage}
              onChange={(e) => handleInputChange('finalPercentage', parseInt(e.target.value) || 0)}
              placeholder="0-100"
              min="0"
              max="100"
              step="1"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="triggeringEvent">Triggering Event</label>
            <select
              id="triggeringEvent"
              value={data.triggeringEvent || ''}
              onChange={(e) => handleInputChange('triggeringEvent', e.target.value)}
            >
              <option value="">Select triggering event</option>
              <option value="Bill of Lading">Bill of Lading</option>
              <option value="Arrival">Arrival at destination</option>
              <option value="Payment">Payment receipt</option>
              <option value="Inspection">Inspection completion</option>
            </select>
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3>WSMD & Surveyor</h3>
        <p className="step-subdescription">Weigh, Sample, Moisture, Determination and Surveyor</p>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="wsmdLocation">WSMD Location *</label>
            <input
              type="text"
              id="wsmdLocation"
              value={data.wsmdLocation}
              onChange={(e) => handleInputChange('wsmdLocation', e.target.value)}
              placeholder="e.g., Receiving smelter warehouse"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="costSharingPercentage">Cost Sharing (%)</label>
            <input
              type="number"
              id="costSharingPercentage"
              value={data.costSharingPercentage}
              onChange={(e) => handleInputChange('costSharingPercentage', parseInt(e.target.value) || 50)}
              placeholder="50"
              min="0"
              max="100"
              step="1"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="surveyor">Surveyor *</label>
            <select
              id="surveyor"
              value={data.surveyor}
              onChange={(e) => handleInputChange('surveyor', e.target.value)}
              required
            >
              <option value="">Select surveyor</option>
              {dropdownData.surveyors?.map((surveyor, index) => (
                <option key={index} value={surveyor}>{surveyor}</option>
              ))}
            </select>
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

export default PaymentTermsStep;
