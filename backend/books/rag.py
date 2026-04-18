import os
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from books.models import Book

class RAGSystem:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.PersistentClient(path=os.getenv('CHROMA_DB_PATH', './chroma_db'))
        self.collection = self.chroma_client.get_or_create_collection(name="books")

    def chunk_text(self, text, chunk_size=500):
        """
        Chunk the text into smaller pieces.
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def add_books_to_vector_db(self):
        """
        Add all books from the database to the vector database.
        """
        books = Book.objects.all()
        for book in books:
            chunks = self.chunk_text(book.description)
            embeddings = self.embedding_model.encode(chunks)
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                self.collection.add(
                    ids=[f"{book.id}_{i}"],
                    embeddings=[embedding.tolist()],
                    metadatas=[{"book_id": book.id, "chunk": chunk}]
                )

    def search_similar_chunks(self, query, top_k=5):
        """
        Search for similar chunks in the vector database.
        """
        query_embedding = self.embedding_model.encode([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        return results

    def generate_answer(self, query, context_chunks):
        """
        Generate an answer using OpenAI with the retrieved context.
        """
        context = "\n".join([chunk['chunk'] for chunk in context_chunks])
        prompt = f"Based on the following book descriptions, answer the question: {query}\n\nContext:\n{context}\n\nAnswer:"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    def ask_question(self, question):
        """
        Full RAG pipeline: search and generate answer.
        """
        results = self.search_similar_chunks(question)
        if results['metadatas']:
            context_chunks = results['metadatas'][0]
            answer = self.generate_answer(question, context_chunks)
            sources = [f"Book ID: {meta['book_id']}" for meta in context_chunks]
            return {"answer": answer, "sources": sources}
        else:
            return {"answer": "No relevant information found.", "sources": []}

# Singleton instance
rag_system = RAGSystem()