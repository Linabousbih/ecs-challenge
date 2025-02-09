import * as XLSX from 'xlsx';
import QrScanner from 'react-qr-scanner';
import { useState, useRef } from 'react'; // Removed explicit React import


const JudgeAssignment = () => {
  const [judges, setJudges] = useState([]);
  const [posters, setPosters] = useState([]);
  const [assignments, setAssignments] = useState({});
  const [selectedPoster, setSelectedPoster] = useState(null);
  const [selectedJudge, setSelectedJudge] = useState(null);
  const [score, setScore] = useState(0);
  const [scannedData, setScannedData] = useState(null);

  const onFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      parseExcel(workbook);
    };
    reader.readAsArrayBuffer(file);
  };

  const parseExcel = (workbook) => {
    const judgesSheet = workbook.Sheets[workbook.SheetNames[0]];
    const postersSheet = workbook.Sheets[workbook.SheetNames[1]];
    setJudges(XLSX.utils.sheet_to_json(judgesSheet));
    setPosters(XLSX.utils.sheet_to_json(postersSheet));
  };

  const assignJudges = () => {
    axios.post('/api/assign', { judges, posters })
      .then(response => setAssignments(response.data.assignments));
  };

  const swapJudges = (poster1, poster2) => {
    axios.post('/api/swap', { poster1, poster2 })
      .then(response => setAssignments(response.data.assignments));
  };

  const handleScoreSubmit = () => {
    if (selectedJudge && selectedPoster) {
      axios.post('/api/submit-score', { judge: selectedJudge, poster: selectedPoster, score })
        .then(response => alert('Score submitted successfully'));
    } else {
      alert('Please select a judge and poster');
    }
  };

  const handleScan = (data) => {
    if (data) {
      setScannedData(data.text);
      setSelectedPoster(data.text);
    }
  };

  const handleError = (err) => {
    console.error(err);
  };

  return (
    <div>
      <h2>Judge Assignment</h2>
      <input type="file" onChange={onFileUpload} />
      <button onClick={assignJudges}>Assign Judges</button>
      <button onClick={() => swapJudges('Poster1', 'Poster2')}>Swap Judges</button>
      <pre>{JSON.stringify(assignments, null, 2)}</pre>

      <h3>QR Code Scanner</h3>
      <QrScanner delay={300} onError={handleError} onScan={handleScan} />
      {scannedData && <p>Scanned Poster ID: {scannedData}</p>}

      <h3>Enter Scores</h3>
      <select onChange={(e) => setSelectedJudge(e.target.value)}>
        <option value="">Select Judge</option>
        {judges.map((judge, index) => (
          <option key={index} value={judge.JudgeID}>{judge.Name}</option>
        ))}
      </select>
      <select onChange={(e) => setSelectedPoster(e.target.value)}>
        <option value="">Select Poster</option>
        {posters.map((poster, index) => (
          <option key={index} value={poster.PosterID}>{poster.Title}</option>
        ))}
      </select>
      <input type="number" min="1" max="10" value={score} onChange={(e) => setScore(e.target.value)} />
      <button onClick={handleScoreSubmit}>Submit Score</button>
    </div>
  );
};

export default JudgeAssignment;
