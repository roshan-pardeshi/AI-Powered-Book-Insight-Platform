import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/books/');
      setBooks(response.data);
    } catch (err) {
      setError('Failed to fetch books');
    } finally {
      setLoading(false);
    }
  };

  const handleScrape = async () => {
    setLoading(true);
    try {
      await axios.post('http://localhost:8000/api/upload/', {
        url: 'https://example.com/books', // Replace with actual URL
        pages: 2
      });
      fetchBooks();
    } catch (err) {
      setError('Failed to scrape books');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center">Loading...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Book Dashboard</h2>
        <div>
          <button onClick={handleScrape} className="bg-green-500 text-white px-4 py-2 rounded mr-2">
            Scrape Books
          </button>
          <Link to="/qa" className="bg-blue-500 text-white px-4 py-2 rounded">
            Ask Questions
          </Link>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {books.map(book => (
          <div key={book.id} className="bg-white p-4 rounded shadow">
            <h3 className="font-bold">{book.title}</h3>
            <p>Author: {book.author}</p>
            <p>Rating: {book.rating}</p>
            <p className="text-sm text-gray-600">{book.description.substring(0, 100)}...</p>
            <Link to={`/book/${book.id}`} className="text-blue-500">View Details</Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;