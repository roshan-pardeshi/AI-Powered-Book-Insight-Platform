from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from .models import Book
from .serializers import BookSerializer
from .scraper import scrape_books, save_books_to_db
from .rag import rag_system
import random

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(['POST'])
def upload_books(request):
    """
    Scrape and store books.
    Expects: {"url": "https://example.com/books", "pages": 2}
    """
    url = request.data.get('url')
    pages = request.data.get('pages', 2)
    if not url:
        return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        books_data = scrape_books(url, pages)
        save_books_to_db(books_data)
        # Update vector DB
        rag_system.add_books_to_vector_db()
        return Response({"message": f"Scraped and saved {len(books_data)} books"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def recommend_books(request):
    """
    Recommend similar books based on a random selection or query.
    """
    cache_key = 'recommended_books'
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    books = list(Book.objects.all())
    if len(books) < 3:
        recommendations = BookSerializer(books, many=True).data
    else:
        recommendations = BookSerializer(random.sample(books, 3), many=True).data

    cache.set(cache_key, recommendations, timeout=3600)  # Cache for 1 hour
    return Response(recommendations)

@api_view(['POST'])
def ask_question(request):
    """
    RAG-based question answering.
    Expects: {"question": "What is a good book about AI?"}
    """
    question = request.data.get('question')
    if not question:
        return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        result = rag_system.ask_question(question)
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
