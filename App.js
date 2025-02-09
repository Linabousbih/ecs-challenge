import { useState, useRef } from 'react';
import JudgeAssignment from "./components/JudgeAssignment"; // Adjust the path if needed

function App() {
  const ref = useRef(); // Example usage of useRef

  return (
    <div>
      <JudgeAssignment />
    </div>
  );
}

export default App;