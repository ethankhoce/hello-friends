"""
PDF Processing Module for Hello Friends RAG System
Handles PDF document parsing and text extraction
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF document processing and text extraction"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF processor
        
        Args:
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                logger.info(f"Successfully extracted text from {pdf_path}")
                return text.strip()
                
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            raise
    
    def process_pdf_to_chunks(self, pdf_path: str) -> List[Document]:
        """
        Process PDF file and return text chunks as LangChain Documents
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of Document objects with metadata
        """
        try:
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            if not text.strip():
                logger.warning(f"No text extracted from {pdf_path}")
                return []
            
            # Split into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Create Document objects with metadata
            documents = []
            pdf_name = Path(pdf_path).name
            
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": pdf_name,
                        "page": i + 1,
                        "chunk_id": f"{pdf_name}_{i}",
                        "file_path": pdf_path
                    }
                )
                documents.append(doc)
            
            logger.info(f"Processed {pdf_path} into {len(documents)} chunks")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise
    
    def process_uploaded_files(self, upload_dir: str) -> List[Document]:
        """
        Process all PDF files in the upload directory
        
        Args:
            upload_dir: Directory containing uploaded PDF files
            
        Returns:
            List of all Document objects from all PDFs
        """
        upload_path = Path(upload_dir)
        if not upload_path.exists():
            logger.warning(f"Upload directory {upload_dir} does not exist")
            return []
        
        all_documents = []
        pdf_files = list(upload_path.glob("*.pdf"))
        
        if not pdf_files:
            logger.info(f"No PDF files found in {upload_dir}")
            return []
        
        for pdf_file in pdf_files:
            try:
                documents = self.process_pdf_to_chunks(str(pdf_file))
                all_documents.extend(documents)
                logger.info(f"Processed {pdf_file.name}: {len(documents)} chunks")
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {e}")
                continue
        
        logger.info(f"Total documents processed: {len(all_documents)}")
        return all_documents
    
    def get_file_info(self, upload_dir: str) -> List[Dict[str, Any]]:
        """
        Get information about uploaded files
        
        Args:
            upload_dir: Directory containing uploaded files
            
        Returns:
            List of file information dictionaries
        """
        upload_path = Path(upload_dir)
        if not upload_path.exists():
            return []
        
        file_info = []
        for pdf_file in upload_path.glob("*.pdf"):
            try:
                # Get basic file info
                stat = pdf_file.stat()
                file_info.append({
                    "name": pdf_file.name,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "path": str(pdf_file)
                })
            except Exception as e:
                logger.error(f"Error getting info for {pdf_file.name}: {e}")
                continue
        
        return file_info
