import { useEffect, useState } from 'preact/hooks'
// import { useEffect, useState } from 'react';
import './app.css'

// const VITE_TEXT_PROCESSOR_API_URL = import.meta.env.VITE_TEXT_PROCESSOR_API_URL
const VITE_TEXT_PROCESSOR_API_URL = 'http://localhost:8000'


function textProcessor(textOperations) {
  const [inputText, setinputText] = useState('');
  const [operation, setOperation] = useState(textOperations[0]); // Default to first operation
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);


  const handleSubmit = (e) => {
    e.preventDefault();
    // Perform text processing based on the selected operation

    const form = e.target;
    const formData = new FormData(form);
    const selectedOperation = formData.get('operation');
    const selectedInputText = formData.get('input-text');

    try {
      fetch(`${VITE_TEXT_PROCESSOR_API_URL}/text-operations/${selectedOperation}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text_content: selectedInputText,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            throw new Error(data.error);
          }
          setResult(data.result);
        });


    } catch (err) {
      setError('Error processing text');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="operation">Select Operation:</label>
          <select
            name="operation"
            value={operation}
            defaultValue={operation}
            onChange={(e) => setOperation(e.target.value)}
          >
            {textOperations.map((operation) => (
              <option key={operation} value={operation}>
                {operation}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="input-text">Enter Text:</label>
          <textarea
            name="input-text"
            value={inputText}
            onChange={(e) => setinputText(e.target.value)}
          />
        </div>
        <button type="submit">Process Text</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <h3>Operation Result:</h3>
          {Object.entries(result).map(([key, value]) => (
            <div key={key}>
              <strong>{key}:</strong> {value}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export function App() {
  const [textOperations, setTextOperations] = useState([]);

  const fetchTextOperations = async () => {
    try {
      const response = await fetch(`${VITE_TEXT_PROCESSOR_API_URL}/text-operations`);
      const data = await response.json();
      return data["available_operations"] || [];
    } catch (error) {
      console.error('Error fetching text operations:', error);
    }
  };

  useEffect(() => {
    fetchTextOperations().then((data) => {
      if (data) {
        setTextOperations(data);
      }
    });
  }, []);

  return (
    <>
      <div>
        <div>
          <h1 className='app-title'>Text Processing App</h1>
        </div>
        <div>
          <h3>Text Processing Operations</h3>
          {textProcessor(textOperations)}
        </div>
      </div>
    </>
  )
}
