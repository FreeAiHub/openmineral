import React, { useState, useEffect } from 'react';
import StepIndicator from './StepIndicator';
import DealBasicsStep from './steps/DealBasicsStep';
import CommercialTermsStep from './steps/CommercialTermsStep';
import PaymentTermsStep from './steps/PaymentTermsStep';
import ReviewSubmitStep from './steps/ReviewSubmitStep';
import SummaryStep from './steps/SummaryStep';
import './BCFlowWizard.css';

const BCFlowWizard = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    dealBasics: {
      seller: 'Open Mineral',
      buyer: '',
      material: '',
      quantity: '',
      quantityTolerance: 10
    },
    commercialTerms: {
      deliveryTerm: '',
      deliveryPoint: '',
      deliveryMode: '',
      shipmentPeriod: '',
      packaging: '',
      assayData: {},
      tcUsdPerDmt: '',
      rcAgUsdPerToz: '',
      transportationCredit: false,
      otherPayables: ''
    },
    paymentTerms: {
      paymentMethod: '',
      currency: 'USD',
      prepaymentPercentage: '',
      provisionalPercentage: '',
      finalPercentage: '',
      wsmdLocation: '',
      costSharingPercentage: 50,
      surveyor: ''
    }
  });

  const [validationResults, setValidationResults] = useState({
    suggestions: [],
    warnings: []
  });

  const [dropdownData, setDropdownData] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);

  // Load dropdown data on component mount
  useEffect(() => {
    loadDropdownData();
  }, []);

  // Poll task status when submitting
  useEffect(() => {
    if (taskId && !taskStatus?.completed) {
      const interval = setInterval(() => {
        checkTaskStatus();
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [taskId, taskStatus]);

  const loadDropdownData = async () => {
    try {
      const response = await fetch('http://localhost:8000/bc-flow/dropdown-data');
      const data = await response.json();
      setDropdownData(data);
    } catch (error) {
      console.error('Failed to load dropdown data:', error);
    }
  };

  const validateStep = async (stepNumber, stepData) => {
    try {
      const response = await fetch(`http://localhost:8000/bc-flow/validate/step${stepNumber}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(stepData),
      });
      const result = await response.json();
      setValidationResults(result);
      return result;
    } catch (error) {
      console.error('Validation failed:', error);
      return { is_valid: false, suggestions: [], warnings: ['Validation service unavailable'] };
    }
  };

  const handleNext = async () => {
    const stepData = getCurrentStepData();
    const validation = await validateStep(currentStep, stepData);

    if (validation.is_valid || currentStep === 4) { // Allow proceeding even with warnings on review step
      if (currentStep < 5) {
        setCurrentStep(currentStep + 1);
      }
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleStepDataChange = (stepName, data) => {
    setFormData(prev => ({
      ...prev,
      [stepName]: { ...prev[stepName], ...data }
    }));
  };

  const getCurrentStepData = () => {
    switch (currentStep) {
      case 1:
        return formData.dealBasics;
      case 2:
        return formData.commercialTerms;
      case 3:
        return formData.paymentTerms;
      default:
        return {};
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const response = await fetch('http://localhost:8000/bc-flow/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      setTaskId(result.task_id);
    } catch (error) {
      console.error('Submission failed:', error);
      setIsSubmitting(false);
    }
  };

  const checkTaskStatus = async () => {
    if (!taskId) return;

    try {
      const response = await fetch(`http://localhost:8000/bc-flow/task/${taskId}`);
      const status = await response.json();
      setTaskStatus(status);

      if (status.status === 'completed') {
        setIsSubmitting(false);
        setCurrentStep(5); // Move to summary
      }
    } catch (error) {
      console.error('Failed to check task status:', error);
    }
  };

  const renderCurrentStep = () => {
    const commonProps = {
      data: getCurrentStepData(),
      onChange: handleStepDataChange,
      validationResults,
      dropdownData
    };

    switch (currentStep) {
      case 1:
        return <DealBasicsStep {...commonProps} />;
      case 2:
        return <CommercialTermsStep {...commonProps} />;
      case 3:
        return <PaymentTermsStep {...commonProps} />;
      case 4:
        return (
          <ReviewSubmitStep
            formData={formData}
            validationResults={validationResults}
            onSubmit={handleSubmit}
            isSubmitting={isSubmitting}
          />
        );
      case 5:
        return <SummaryStep taskStatus={taskStatus} />;
      default:
        return null;
    }
  };

  return (
    <div className="bc-flow-wizard">
      <StepIndicator currentStep={currentStep} />

      <div className="step-content">
        {renderCurrentStep()}
      </div>

      <div className="step-navigation">
        {currentStep > 1 && currentStep < 5 && (
          <button
            className="btn btn-secondary"
            onClick={handlePrevious}
            disabled={isSubmitting}
          >
            Previous
          </button>
        )}

        {currentStep < 4 && (
          <button
            className="btn btn-primary"
            onClick={handleNext}
            disabled={isSubmitting}
          >
            Next
          </button>
        )}

        {currentStep === 4 && !isSubmitting && (
          <button
            className="btn btn-success"
            onClick={handleSubmit}
          >
            Submit BC Form
          </button>
        )}
      </div>

      {isSubmitting && (
        <div className="processing-indicator">
          <div className="spinner"></div>
          <p>Processing your Business Confirmation...</p>
        </div>
      )}
    </div>
  );
};

export default BCFlowWizard;
