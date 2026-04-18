import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const QAPage = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:8000/api/ask/', { question });
      setAnswer(response.data.answer);
      setSources(response.data.sources);
    } catch (err) {
      setError('Failed to get answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Link to="/" className="text-blue-500 mb-4 inline-block">&larr; Back to Dashboard</Link>
      <h2 className="text-xl font-bold mb-4">Ask Questions About Books</h2>
      <div className="mb-4">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about books..."
          className="w-full p-2 border rounded"
          rows="4"
        />
        <button
          onClick={handleAsk}
          disabled={loading}
          className="mt-2 bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {loading ? 'Asking...' : 'Ask'}
        </button>
      </div>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      {answer && (
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-2">Answer:</h3>
          <p className="mb-4">{answer}</p>
          {sources.length > 0 && (
            <div>
              <h4 className="font-bold">Sources:</h4>
              <ul>
                {sources.map((source, index) => (
                  <li key={index} className="text-sm text-gray-600">{source}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default QAPage;