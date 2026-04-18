import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const BookDetail = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBook = useCallback(async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/books/${id}/`);
      setBook(response.data);
    } catch (err) {
      setError('Failed to fetch book details');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchBook();
  }, [fetchBook]);

  if (loading) return <div className="text-center">Loading...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;
  if (!book) return <div className="text-center">Book not found</div>;

  return (
    <div className="max-w-2xl mx-auto">
      <Link to="/" className="text-blue-500 mb-4 inline-block">&larr; Back to Dashboard</Link>
      <div className="bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-bold mb-2">{book.title}</h1>
        <p className="text-lg mb-2">Author: {book.author}</p>
        <p className="text-lg mb-4">Rating: {book.rating}</p>
        <p className="mb-4">{book.description}</p>
        <a href={book.url} target="_blank" rel="noopener noreferrer" className="text-blue-500">
          View on Website
        </a>
      </div>
    </div>
  );
};

export default BookDetail;