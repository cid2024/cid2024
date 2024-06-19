import React, { useState } from 'react';
import ProblemViewer from './components/customProblemViewer';
import './App.css';
import ProblemJSON from './components/customProblem.json';
import { Problem } from './components/types';
import { getProblemById } from './components/api';

function App() {
  // State to manage the editable text
  const [editableText, setEditableText] = useState<string>('');
  const [problemData, setProblemData] = useState<Problem>(ProblemJSON as unknown as Problem);

  // Function to handle input changes
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEditableText(event.target.value);
  };

  // Function to handle confirm button click
  const handleConfirmClick = () => {
    const id = editableText.trim();
    getProblemById(id).then((problem) => {
      if (problem) {
        setProblemData(problem);
      } else { 
        console.log('Problem not found');
      }
    });
  };

  return (
    <>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
        <input 
          type="text" 
          value={editableText} 
          onChange={handleInputChange} 
          style={{ marginRight: '10px' }}
        />
        <button onClick={handleConfirmClick}>Confirm</button>
      </div>
      <ProblemViewer
        problem={problemData}
        width={120}
        disablePink={true}
      />
    </>
  );
}

export default App;