"""
Hello Friends - Migrant Worker Rights Assistant
A Streamlit app providing guidance for migrant workers in Singapore.
"""

import streamlit as st
import os
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from datetime import datetime

# Import our utility modules
from utils.kb_loader import KnowledgeBaseLoader
from utils.prompts import PromptManager
from utils.filters import ResponseFilter
from utils.i18n import I18nManager
from utils.openai_service import OpenAIService
from utils.rag_service import RAGService

# Configure Streamlit page
st.set_page_config(
    page_title="Hello Friends",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
@st.cache_resource
def load_managers():
    """Load and cache utility managers"""
    kb_loader = KnowledgeBaseLoader()
    prompt_manager = PromptManager()
    response_filter = ResponseFilter()
    i18n_manager = I18nManager()
    openai_service = OpenAIService()
    rag_service = RAGService()
    return kb_loader, prompt_manager, response_filter, i18n_manager, openai_service, rag_service

def main():
    """Main application function"""
    
    # Load managers
    kb_loader, prompt_manager, response_filter, i18n_manager, openai_service, rag_service = load_managers()
    
    # Load knowledge base
    knowledge_base = kb_loader.load_knowledge_base()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 3rem;">🤝 Hello Friends</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Trusted guidance for migrant-worker rights in Singapore. Not legal advice.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📁 Admin Panel")
        
        # File upload section
        uploaded_files = st.file_uploader(
            "Upload PDF files for knowledge base",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload PDF documents that will be used to enhance the knowledge base"
        )
        
        if uploaded_files:
            upload_dir = Path("rag/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            for uploaded_file in uploaded_files:
                file_path = upload_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        # Show uploaded files
        upload_dir = Path("rag/uploads")
        if upload_dir.exists():
            uploaded_files_list = list(upload_dir.glob("*.pdf"))
            if uploaded_files_list:
                st.markdown("**Uploaded Files:**")
                for file in uploaded_files_list:
                    st.text(f"📄 {file.name}")
            else:
                uploaded_files_list = []
        else:
            uploaded_files_list = []
        
        # RAG Management Section
        st.markdown("### 🤖 RAG System")
        
        # Process documents button
        if st.button("🔄 Process Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                result = rag_service.process_uploaded_documents()
                if result["success"]:
                    st.success(f"✅ {result['message']}")
                else:
                    st.error(f"❌ {result['message']}")
        
        # Rebuild database button
        if st.button("🔨 Rebuild Database", use_container_width=True):
            with st.spinner("Rebuilding vector database..."):
                result = rag_service.rebuild_database()
                if result["success"]:
                    st.success(f"✅ {result['message']}")
                else:
                    st.error(f"❌ {result['message']}")
        
        # Show RAG system info
        rag_info = rag_service.get_database_info()
        if rag_info:
            st.markdown("**RAG System Status:**")
            st.text(f"📊 Documents in DB: {rag_info['vector_db'].get('document_count', 0)}")
            st.text(f"🔗 RAG Chain: {'✅ Active' if rag_info['rag_chain_available'] else '❌ Inactive'}")
            st.text(f"🤖 OpenAI: {'✅ Available' if rag_info['openai_available'] else '❌ Not Available'}")
        
        # Language selection
        st.markdown("### 🌐 Language")
        language = st.selectbox(
            "Select language",
            ["English", "Tamil", "Bengali", "Tagalog", "Bahasa Indonesia"],
            index=0
        )
        
        # Statistics
        st.markdown("### 📊 Statistics")
        st.metric("Knowledge Base Entries", len(knowledge_base.get('rights', [])))
        st.metric("Uploaded Documents", len(uploaded_files_list))
    
    with col2:
        st.markdown("### 💬 Chat Assistant")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Example prompts
        st.markdown("**Quick questions you can ask:**")
        example_prompts = prompt_manager.get_example_prompts()
        
        # Display example prompts as chips
        cols = st.columns(3)
        for i, prompt in enumerate(example_prompts):
            with cols[i % 3]:
                if st.button(prompt, key=f"example_{i}", use_container_width=True):
                    st.session_state.user_input = prompt
        
        # Chat input
        if prompt := st.chat_input("Ask about your rights..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Finding information for you..."):
                    response = generate_response(prompt, knowledge_base, prompt_manager, response_filter, openai_service, kb_loader, rag_service)
                    
                    # Check if it's a RAG response and show indicator
                    if "🤖 **RAG Response**" in response:
                        st.success("📚 Response generated using RAG (document-based)")
                    elif "⚠️ **General Response**" in response:
                        st.warning("⚠️ General response (no relevant documents)")
                    
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

def generate_response(query: str, knowledge_base: Dict, prompt_manager: PromptManager, response_filter: ResponseFilter, openai_service: OpenAIService, kb_loader: KnowledgeBaseLoader, rag_service: RAGService) -> str:
    """Generate a response based on the query using RAG and knowledge base"""
    
    # Check if this is an emergency query
    if prompt_manager.is_emergency_query(query):
        return prompt_manager.format_emergency_response()
    
    # Try RAG first if available
    try:
        rag_result = rag_service.query_with_rag(query)
        if rag_result["success"]:
            response = rag_result["answer"]
            method = rag_result.get("method", "unknown")
            
            # Add RAG source indicator
            if method == "retrieval_augmented":
                response = "🤖 **RAG Response** (Based on uploaded documents)\n\n" + response
            
            # Add source information if available
            if rag_result.get("source_documents"):
                sources = rag_result["source_documents"]
                if sources:
                    response += "\n\n---\n**📚 Sources:**\n"
                    for i, source in enumerate(sources[:2], 1):  # Show max 2 sources
                        source_name = source.get("source", "Document")
                        response += f"{i}. 📄 {source_name}\n"
            
            return response
    except Exception as e:
        st.error(f"RAG query failed: {e}")
    
    # Fallback to original method
    return _generate_fallback_response(query, knowledge_base, prompt_manager, response_filter, kb_loader)

def _get_relevant_rights(query: str, knowledge_base: Dict, prompt_manager: PromptManager, kb_loader: KnowledgeBaseLoader) -> List[Dict]:
    """Get relevant rights for the query"""
    # Categorize the query
    categories = prompt_manager.categorize_query(query)
    
    # Find relevant rights based on categories
    relevant_rights = []
    for category in categories:
        category_rights = kb_loader.get_rights_by_category(category)
        relevant_rights.extend(category_rights)
    
    # Remove duplicates while preserving order
    seen_ids = set()
    unique_rights = []
    for right in relevant_rights:
        if right.get('id') not in seen_ids:
            seen_ids.add(right.get('id'))
            unique_rights.append(right)
    
    # If no specific match, search by keywords
    if not unique_rights:
        search_results = kb_loader.search_rights(query)
        unique_rights = search_results[:3]  # Limit to 3 results
    
    # If still no results, get general information
    if not unique_rights:
        all_rights = knowledge_base.get('rights', [])
        unique_rights = all_rights[:2]  # Get first 2 as general info
    
    return unique_rights

def _generate_fallback_response(query: str, knowledge_base: Dict, prompt_manager: PromptManager, response_filter: ResponseFilter, kb_loader: KnowledgeBaseLoader) -> str:
    """Generate fallback response using original method"""
    relevant_rights = _get_relevant_rights(query, knowledge_base, prompt_manager, kb_loader)
    response = response_filter.format_response(query, relevant_rights)
    return response

if __name__ == "__main__":
    main()