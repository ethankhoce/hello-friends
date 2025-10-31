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
import html
import re
import logging
import markdown

# Import our utility modules
from utils.kb_loader import KnowledgeBaseLoader
from utils.prompts import PromptManager
from utils.filters import ResponseFilter
from utils.i18n import I18nManager
from utils.openai_service import OpenAIService
from utils.rag_service import RAGService

# Configure logging once for the app
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

logger = logging.getLogger("hellofriends.chat")

# Configure Streamlit page
st.set_page_config(
    page_title="Hello Friends",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hardcoded login credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def show_login_page():
    """Display login page"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 1rem;">🤝 Hello Friends</h1>
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
            Migrant Worker Rights Assistant
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        st.markdown("### Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login", use_container_width=True)
        
        if submit_button:
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please try again.")
    
    # Show credentials info (for reference)
    with st.expander("ℹ️ Login Information"):
        st.info(f"Username: `{VALID_USERNAME}`\n\nPassword: `{VALID_PASSWORD}`")

# Initialize managers
@st.cache_resource
def load_managers():
    """Load and cache utility managers"""
    kb_loader = KnowledgeBaseLoader()
    prompt_manager = PromptManager()
    response_filter = ResponseFilter()
    i18n_manager = I18nManager()
    openai_service = OpenAIService()
    rag_service = RAGService(openai_service=openai_service)
    return kb_loader, prompt_manager, response_filter, i18n_manager, openai_service, rag_service

def main():
    """Main application function"""
    
    # Display disclaimer
    st.markdown("""
        <div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 1rem; margin-bottom: 1.5rem; border-radius: 5px;">
            <h4 style="margin: 0 0 0.5rem 0; color: #856404;">⚠️ IMPORTANT NOTICE</h4>
            <p style="margin: 0; color: #856404;">
                <strong>This web application is a prototype developed for educational purposes only.</strong> The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #856404;">
                Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #856404;">
                Always consult with qualified professionals for accurate and personalized advice.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Load managers
    kb_loader, prompt_manager, response_filter, i18n_manager, openai_service, rag_service = load_managers()
    
    # Load knowledge base
    knowledge_base = kb_loader.load_knowledge_base()
    
    # Header with logout button
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 3rem;">🤝 Hello Friends</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Trusted guidance for migrant-worker rights in Singapore. Not legal advice.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Only show chat to end-users; admin panel gated by env var
    show_admin = os.getenv("ADMIN_MODE", "0") == "1"
    
    if show_admin:
        col1, col2 = st.columns([1, 2])
    else:
        # When not in admin mode, use full width for chat
        col2 = st.container()
    
    if show_admin:
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
        api_key_display = openai_service.api_key if getattr(openai_service, "api_key", None) else "Not configured"
        st.info(f"**OpenAI API Key:** `{api_key_display}`")

        openai_status = openai_service.get_status()
        status_text = "✅ OpenAI client ready" if openai_service.is_available() and not openai_status.get("last_error") else "⚠️ OpenAI client fallback"
        st.caption(f"{status_text} · model: {openai_status.get('model', 'unknown')}")
        if openai_status.get("last_error"):
            st.warning(f"Last OpenAI error: {openai_status['last_error']}")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Example prompts
        st.markdown("**Quick questions you can ask:**")
        example_prompts = prompt_manager.get_example_prompts()
        
        # Display example prompts as chips
        cols = st.columns(3)
        for i, prompt in enumerate(example_prompts):
            with cols[i % 3]:
                if st.button(prompt, key=f"example_{i}", use_container_width=True):
                    st.session_state.user_input = prompt
        
        # If a quick question was clicked, process it like a chat submission
        if st.session_state.get("user_input"):
            queued_prompt = st.session_state.user_input
            # Clear immediately to avoid duplicate submissions on rerun
            st.session_state.user_input = ""
            
            # Ensure messages list exists
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Add user message and generate response
            st.session_state.messages.append({"role": "user", "content": queued_prompt})
            with st.spinner("Finding information for you..."):
                response = generate_response(
                    queued_prompt,
                    knowledge_base,
                    prompt_manager,
                    response_filter,
                    openai_service,
                    kb_loader,
                    rag_service,
                )
                if "🤖 **RAG Response**" in response:
                    response = "📚 Response generated using RAG (document-based)\n\n" + response
                elif "⚠️ **General Response**" in response:
                    response = "⚠️ General response (no relevant documents)\n\n" + response
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        # Create a container for chat messages with fixed height and scroll
        chat_container = st.container()
        
        with chat_container:
            # Display chat history in a scrollable area
            if st.session_state.messages:
                # Render messages inline without grey framed container
                st.markdown("", unsafe_allow_html=True)
                
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        # Clean the content to remove any stray HTML tags
                        clean_content = re.sub(r'</?div[^>]*>', '', message["content"]).strip()
                        clean_content = html.escape(clean_content)
                        st.markdown(f"""
                        <div style="margin-bottom: 1rem; text-align: right;">
                            <div style="display: inline-block; background-color: #007bff; color: white; padding: 0.5rem 1rem; border-radius: 18px; max-width: 70%; word-wrap: break-word;">
                                {clean_content}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Clean the content to remove any stray HTML tags and render markdown
                        clean_content = re.sub(r'</?div[^>]*>', '', message["content"]).strip()
                        rendered_markdown = markdown.markdown(clean_content)
                        st.markdown(
                            f"""
                            <div style="margin-bottom: 1rem; text-align: left;">
                                <div style="display: inline-block; background-color: #f1f3f4; color: #333; padding: 0.5rem 1rem; border-radius: 18px; max-width: 70%; word-wrap: break-word;">
                                    {rendered_markdown}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                
                st.markdown("", unsafe_allow_html=True)
            else:
                # Show empty state
                st.markdown(
                    "<p style=\"color: #666; text-align: center; margin: 1.5rem 0;\">Start a conversation by asking about your rights...</p>",
                    unsafe_allow_html=True,
                )
        
        # Bottom section with input and controls
        st.markdown("---")
        
        # Chat input at the bottom
        if prompt := st.chat_input("Ask about your rights..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.spinner("Finding information for you..."):
                response = generate_response(prompt, knowledge_base, prompt_manager, response_filter, openai_service, kb_loader, rag_service)
                
                # Check if it's a RAG response and show indicator
                if "🤖 **RAG Response**" in response:
                    response = "📚 Response generated using RAG (document-based)\n\n" + response
                elif "⚠️ **General Response**" in response:
                    response = "⚠️ General response (no relevant documents)\n\n" + response
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

def generate_response(query: str, knowledge_base: Dict, prompt_manager: PromptManager, response_filter: ResponseFilter, openai_service: OpenAIService, kb_loader: KnowledgeBaseLoader, rag_service: RAGService) -> str:
    """Generate a response based on the query using RAG and knowledge base"""
    
    logger.info("Chat assistant received query: %s", query)
    
    # Check if this is an emergency query
    if prompt_manager.is_emergency_query(query):
        emergency_response = prompt_manager.format_emergency_response()
        logger.info("Emergency response returned for query: %s", query)
        return emergency_response

    # Handle simple greetings directly without invoking RAG
    if prompt_manager.is_greeting_query(query):
        logger.info("Greeting detected, responding directly without RAG")
        return openai_service.generate_response(query)
    
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
            
            logger.info("Responding with RAG (%s) for query '%s'", method, query)
            return response
    except Exception as e:
        logger.exception("RAG query failed for query '%s'", query)
        st.error(f"RAG query failed: {e}")
    
    # Fallback to original method
    fallback_response = _generate_fallback_response(query, knowledge_base, prompt_manager, response_filter, kb_loader)
    logger.info("Responding with fallback response for query '%s'", query)
    return fallback_response

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
    # Check authentication before showing main app
    if not check_authentication():
        show_login_page()
    else:
        main()