"""
Vector Database Service for Hello Friends RAG System
Handles document embeddings and similarity search using ChromaDB
"""

import os
import logging
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorDatabaseService:
    """Handles vector database operations for RAG system"""
    
    def __init__(self, persist_directory: str = "rag/vector_db", collection_name: str = "migrant_worker_rights"):
        """
        Initialize vector database service
        
        Args:
            persist_directory: Directory to persist the vector database
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = self._get_embeddings()
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize vector store
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _get_embeddings(self):
        """Get embeddings model (OpenAI if available, otherwise local)"""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if openai_api_key:
            try:
                logger.info("Using OpenAI embeddings")
                return OpenAIEmbeddings(openai_api_key=openai_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI embeddings: {e}")
        
        # Fallback to local embeddings
        logger.info("Using local sentence-transformers embeddings")
        return SentenceTransformer('all-MiniLM-L6-v2')
    
    def _initialize_vectorstore(self):
        """Initialize the vector store"""
        try:
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory),
                client=self.client
            )
            logger.info(f"Initialized vector store with collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Add documents to the vector database
        
        Args:
            documents: List of Document objects to add
            
        Returns:
            True if successful, False otherwise
        """
        if not documents:
            logger.warning("No documents to add")
            return False
        
        try:
            # Add documents to vector store
            self.vectorstore.add_documents(documents)
            
            # Persist the changes
            self.vectorstore.persist()
            
            logger.info(f"Successfully added {len(documents)} documents to vector database")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents to vector database: {e}")
            return False
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search on the vector database
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of similar Document objects
        """
        try:
            if not self.vectorstore:
                logger.error("Vector store not initialized")
                return []
            
            # Perform similarity search
            results = self.vectorstore.similarity_search(query, k=k)
            
            logger.info(f"Found {len(results)} similar documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            if self._handle_database_error(e):
                logger.warning("Vector database was reset due to schema mismatch. Please reprocess documents if needed.")
            else:
                logger.error(f"Error performing similarity search: {e}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """
        Perform similarity search with scores
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of (Document, score) tuples
        """
        try:
            if not self.vectorstore:
                logger.error("Vector store not initialized")
                return []
            
            # Perform similarity search with scores
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            logger.info(f"Found {len(results)} similar documents with scores for query: {query[:50]}...")
            return results
            
        except Exception as e:
            if self._handle_database_error(e):
                logger.warning("Vector database was reset due to schema mismatch. Please reprocess documents if needed.")
            else:
                logger.error(f"Error performing similarity search with scores: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the vector database collection
        
        Returns:
            Dictionary with collection information
        """
        try:
            collection = self.client.get_collection(self.collection_name)
            count = collection.count()
            
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": str(self.persist_directory),
                "embedding_model": "OpenAI" if hasattr(self.embeddings, 'openai_api_key') else "SentenceTransformer"
            }
            
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {
                "collection_name": self.collection_name,
                "document_count": 0,
                "persist_directory": str(self.persist_directory),
                "embedding_model": "Unknown",
                "error": str(e)
            }
    
    def clear_collection(self) -> bool:
        """
        Clear all documents from the collection
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete the collection
            self.client.delete_collection(self.collection_name)
            
            # Reinitialize
            self._initialize_vectorstore()
            
            logger.info(f"Cleared collection: {self.collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            return False
    
    def rebuild_from_documents(self, documents: List[Document]) -> bool:
        """
        Rebuild the entire vector database from documents
        
        Args:
            documents: List of Document objects
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Clear existing collection
            self.clear_collection()
            
            # Add all documents
            if documents:
                return self.add_documents(documents)
            else:
                logger.info("No documents to rebuild with")
                return True
                
        except Exception as e:
            logger.error(f"Error rebuilding vector database: {e}")
            return False

    def _handle_database_error(self, error: Exception) -> bool:
        """Handle known database errors such as schema mismatches.

        Returns True if the error was handled (e.g., by resetting the DB).
        """
        error_message = str(error)
        if "no such column: collections.schema_str" in error_message:
            logger.error("ChromaDB schema mismatch detected. Resetting persistent store at %s", self.persist_directory)
            self._reset_persistent_store()
            return True
        return False

    def _reset_persistent_store(self) -> None:
        """Reset the persistent vector store and reinitialize the client."""
        try:
            # Close existing vector store references
            self.vectorstore = None

            if self.persist_directory.exists():
                shutil.rmtree(self.persist_directory, ignore_errors=True)

            self.persist_directory.mkdir(parents=True, exist_ok=True)

            # Recreate the Chroma client and vector store
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(anonymized_telemetry=False)
            )
            self._initialize_vectorstore()
        except Exception as reset_error:
            logger.exception("Failed to reset persistent vector store: %s", reset_error)
