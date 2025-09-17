import React from 'react';
import './StepIndicator.css';

const StepIndicator = ({ currentStep }) => {
  const steps = [
    { number: 1, title: 'Deal Basics', description: 'Seller, Buyer, Material & Quantity' },
    { number: 2, title: 'Commercial Terms', description: 'Delivery, Assay & Pricing' },
    { number: 3, title: 'Payment Terms', description: 'Method, Stages & Surveyor' },
    { number: 4, title: 'Review & Submit', description: 'Validate & Confirm' },
    { number: 5, title: 'Summary', description: 'Processing Results' }
  ];

  return (
    <div className="step-indicator">
      {steps.map((step) => (
        <div
          key={step.number}
          className={`step-item ${currentStep === step.number ? 'active' : ''} ${currentStep > step.number ? 'completed' : ''}`}
        >
          <div className="step-circle">
            {currentStep > step.number ? (
              <span className="checkmark">✓</span>
            ) : (
              <span className="step-number">{step.number}</span>
            )}
          </div>
          <div className="step-info">
            <h3 className="step-title">{step.title}</h3>
            <p className="step-description">{step.description}</p>
          </div>
          {step.number < steps.length && (
            <div className={`step-connector ${currentStep > step.number ? 'completed' : ''}`}></div>
          )}
        </div>
      ))}
    </div>
  );
};

export default StepIndicator;
