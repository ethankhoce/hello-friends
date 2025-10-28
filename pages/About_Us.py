import streamlit as st
from pathlib import Path


def _section_heading(title: str, emoji: str = "") -> None:
    if emoji:
        st.markdown(f"### {emoji} {title}")
    else:
        st.markdown(f"### {title}")


def main() -> None:
    st.markdown(
        """
        <div style="text-align: center; padding: 1.5rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 1.5rem;">
            <h1 style="margin: 0; font-size: 2.4rem;">About Us</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Migrant Worker Rights Assistant (Singapore)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Optional logo rendering (ignore failures silently)
    logo_path = Path("assets/logo.svg")
    if logo_path.exists():
        st.markdown(
            f"<div style='text-align:center; margin-bottom: 1rem;'><img src='{logo_path.as_posix()}' alt='Hello Friends Logo' width='120'/></div>",
            unsafe_allow_html=True,
        )

    _section_heading("Project Scope", "🧭")
    st.markdown(
        """
        Hello Friends is a community-oriented Streamlit application that helps migrant workers in Singapore
        understand their rights in clear, accessible language. The app provides:

        - Quick, trustworthy guidance on common rights questions
        - Multilingual UI and responses for better accessibility
        - Links to official resources and NGOs for further help
        - A friendly, mobile-first interface that works well on low-end devices
        """
    )

    _section_heading("Objectives", "🎯")
    st.markdown(
        """
        - Provide general, non-legal guidance on key rights topics
        - Help users discover relevant official resources quickly
        - Support administrators in enriching the knowledge base with documents
        - Lay a foundation for privacy-preserving Retrieval-Augmented Generation (RAG)
        """
    )

    _section_heading("Data Sources", "📚")
    st.markdown(
        """
        The assistant draws information from two main sources:
        
        1. Curated knowledge base: `kb/rights_sg.yaml` (structured summaries of rights topics)
        2. Uploaded documents: PDFs added via the Admin Panel (`rag/uploads/`) that can be processed into a
           vector database for document-grounded answers

        Notes:
        - Content is intended as general guidance only and not legal advice
        - Where possible, responses include links or references to official sources
        """
    )

    _section_heading("Features", "✨")
    st.markdown(
        """
        - Multilingual support: English, Tamil, Bengali, Tagalog, Bahasa Indonesia
        - Admin panel for PDF uploads and database maintenance
        - Chat assistant with structured, action-oriented responses
        - Optional RAG mode for answers grounded in uploaded documents
        - Accessible UI with clear layout and friendly tone
        """
    )

    _section_heading("How It Works", "🛠️")
    st.markdown(
        """
        - Questions are first checked against uploaded documents (if processed) using a vector database
        - If relevant passages are found, answers are generated and attributed to those sources (RAG)
        - If not, the assistant falls back to the curated knowledge base summaries
        - Emergency or crisis prompts are routed to clear, jurisdiction-appropriate guidance
        """
    )

    _section_heading("Disclaimer", "⚠️")
    st.info(
        "This app provides general guidance only and does not constitute legal advice. "
        "For specific legal matters, consult a qualified lawyer or contact MOM directly.",
        icon="⚖️",
    )

    _section_heading("Credits & Open Source", "🤝")
    st.markdown(
        """
        Built with Streamlit and open-source libraries. The project welcomes
        contributions that improve accessibility, accuracy, and usability for migrant workers.
        """
    )


if __name__ == "__main__":
    main()


