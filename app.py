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
    return kb_loader, prompt_manager, response_filter, i18n_manager

def main():
    """Main application function"""
    
    # Load managers
    kb_loader, prompt_manager, response_filter, i18n_manager = load_managers()
    
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
                    response = generate_response(prompt, knowledge_base, prompt_manager, response_filter)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

def generate_response(query: str, knowledge_base: Dict, prompt_manager: PromptManager, response_filter: ResponseFilter) -> str:
    """Generate a response based on the query and knowledge base"""
    
    # Check if this is an emergency query
    if prompt_manager.is_emergency_query(query):
        return prompt_manager.format_emergency_response()
    
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
    
    # Generate structured response
    response = response_filter.format_response(query, unique_rights)
    
    return response

if __name__ == "__main__":
    main()