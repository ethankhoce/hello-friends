"""
RAG Service for Hello Friends
Combines document retrieval with AI generation for enhanced responses
"""

import logging
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document

from .pdf_processor import PDFProcessor
from .vector_db import VectorDatabaseService
from .openai_service import OpenAIService

logger = logging.getLogger(__name__)

class RAGService:
    """Retrieval-Augmented Generation service for migrant worker rights"""
    
    def __init__(
        self,
        upload_dir: str = "rag/uploads",
        vector_db_dir: str = "rag/vector_db",
        openai_service: Optional[OpenAIService] = None,
    ):
        """
        Initialize RAG service
        
        Args:
            upload_dir: Directory containing uploaded PDF files
            vector_db_dir: Directory for vector database storage
        """
        self.upload_dir = upload_dir
        self.pdf_processor = PDFProcessor()
        self.vector_db = VectorDatabaseService(persist_directory=vector_db_dir)
        self.openai_service = openai_service or OpenAIService()
    
    def process_uploaded_documents(self) -> Dict[str, Any]:
        """
        Process all uploaded PDF documents and add them to vector database
        
        Returns:
            Dictionary with processing results
        """
        try:
            # Process PDFs to documents
            documents = self.pdf_processor.process_uploaded_files(self.upload_dir)
            
            if not documents:
                return {
                    "success": False,
                    "message": "No documents found to process",
                    "documents_processed": 0
                }
            
            # Add to vector database
            success = self.vector_db.add_documents(documents)
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully processed {len(documents)} document chunks",
                    "documents_processed": len(documents)
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to add documents to vector database",
                    "documents_processed": 0
                }
                
        except Exception as e:
            logger.error(f"Error processing uploaded documents: {e}")
            return {
                "success": False,
                "message": f"Error processing documents: {str(e)}",
                "documents_processed": 0
            }
    
    def query_with_rag(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system with a question
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            # Perform similarity search
            similar_docs = self.vector_db.similarity_search(question, k=3)
            
            if not similar_docs:
                # No relevant documents found
                return {
                    "success": False,
                    "answer": "⚠️ **General Response** (No relevant documents found)\n\nI couldn't find relevant information in the uploaded documents. Please try rephrasing your question or contact MOM at 6438 5122 for assistance.",
                    "source_documents": [],
                    "method": "fallback_no_docs"
                }
            
            # Combine document content
            context = "\n\n".join([doc.page_content for doc in similar_docs])
            
            # Use OpenAI service to generate response with context
            if self.openai_service.is_available():
                response = self.openai_service.generate_response(
                    question, 
                    {"retrieved_context": context}
                )
            else:
                # Basic response with document snippets
                response = f"Based on the available information:\n\n{context[:500]}..."
            
            return {
                "success": True,
                "answer": response,
                "source_documents": [
                    {
                        "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                        "source": doc.metadata.get("source", "Unknown"),
                        "chunk_id": doc.metadata.get("chunk_id", "Unknown")
                    }
                    for doc in similar_docs
                ],
                "method": "retrieval_augmented"
            }
            
        except Exception as e:
            logger.error(f"Error querying RAG system: {e}")
            return {
                "success": False,
                "answer": "⚠️ **General Response** (System error)\n\nI'm sorry, I encountered an error while processing your question. Please try again or contact MOM at 6438 5122 for assistance.",
                "source_documents": [],
                "method": "error"
            }
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get information about the vector database
        
        Returns:
            Dictionary with database information
        """
        try:
            db_info = self.vector_db.get_collection_info()
            file_info = self.pdf_processor.get_file_info(self.upload_dir)
            
            return {
                "vector_db": db_info,
                "uploaded_files": file_info,
                "rag_chain_available": True,  # Simplified version always available
                "openai_available": self.openai_service.is_available()
            }
            
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {
                "vector_db": {"error": str(e)},
                "uploaded_files": [],
                "rag_chain_available": False,
                "openai_available": False
            }
    
    def rebuild_database(self) -> Dict[str, Any]:
        """
        Rebuild the entire vector database from uploaded documents
        
        Returns:
            Dictionary with rebuild results
        """
        try:
            # Process all documents
            documents = self.pdf_processor.process_uploaded_files(self.upload_dir)
            
            if not documents:
                return {
                    "success": False,
                    "message": "No documents found to rebuild database",
                    "documents_processed": 0
                }
            
            # Rebuild vector database
            success = self.vector_db.rebuild_from_documents(documents)
            
            if success:
                return {
                    "success": True,
                    "message": f"Successfully rebuilt database with {len(documents)} document chunks",
                    "documents_processed": len(documents)
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to rebuild vector database",
                    "documents_processed": 0
                }
                
        except Exception as e:
            logger.error(f"Error rebuilding database: {e}")
            return {
                "success": False,
                "message": f"Error rebuilding database: {str(e)}",
                "documents_processed": 0
            }
