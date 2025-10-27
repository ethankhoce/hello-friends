# RAG (Retrieval-Augmented Generation) Directory

This directory contains files and utilities for the RAG functionality of the Hello Friends app.

## Structure

- `uploads/` - Directory for storing uploaded PDF files that will be processed for RAG
- `README.md` - This file explaining the RAG setup

## Future RAG Implementation

The current implementation uses a simple keyword-matching approach. In the future, this will be enhanced with:

1. **PDF Processing**: Extract text from uploaded PDFs
2. **Embeddings**: Generate vector embeddings for text chunks
3. **Vector Database**: Store and retrieve relevant information
4. **LLM Integration**: Use OpenAI or other LLMs for generating responses

## Current Status

- PDF upload functionality is implemented in the main app
- Files are stored in the `uploads/` directory
- Ready for future RAG integration without UI changes

## Integration Points

The main app (`app.py`) has a stub function `generate_response()` where RAG functionality will be integrated:

```python
def generate_response(query: str, knowledge_base: Dict, prompt_manager: PromptManager, response_filter: ResponseFilter) -> str:
    # Current: Simple keyword matching
    # Future: RAG with embeddings and LLM
```

This design allows for seamless integration of RAG without changing the user interface.
