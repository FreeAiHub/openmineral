import React, { useState, useEffect } from 'react';
import './App.css';
import BCFlowWizard from './components/BCFlowWizard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>OpenMineral BC Flow</h1>
        <p>Business Confirmation Flow with AI-Powered Validation</p>
      </header>
      <main>
        <BCFlowWizard />
      </main>
    </div>
  );
}

export default App;
