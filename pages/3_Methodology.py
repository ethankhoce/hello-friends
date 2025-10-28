import streamlit as st


def _header() -> None:
    st.markdown(
        """
        <div style="text-align: center; padding: 1.5rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 1.5rem;">
            <h1 style="margin: 0; font-size: 2.2rem;">Methodology</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Data flows and implementation details for Hello Friends</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _intro() -> None:
    st.markdown(
        """
        ### Overview
        - **Home Chat Assistant**: Retrieval-Augmented Generation (RAG) over uploaded PDFs + curated rights YAML. Uses OpenAI when available and falls back to local logic otherwise.
        - **Recreation Centres**: Client-side search and filtering over a curated list; no external calls.

        Below are flowcharts for each use case and brief implementation notes.
        """
    )


def _chat_flow() -> None:
    st.markdown("### 💬 Home Chat Assistant – Flow")
    dot = r"""
    digraph ChatRAG {
      rankdir=LR;
      node [shape=rounded, style=filled, fillcolor="#e8f0ff"];

      U[label="User Query"]
      C1[label="Check emergency intent (PromptManager)"]
      EM[label="Return emergency response", shape=box, fillcolor="#fff3cd"]
      RAG[label="RAG Service Query"]
      VS[label="Vector Similarity Search (k=3)"]
      RET[label="Top-k context"]
      OA[label="OpenAI Chat Completion", fillcolor="#e6ffed"]
      RAGFallback[label="RAG fallback response", fillcolor="#f0f0f0"]
      KB[label="Knowledge Base fallback"]
      Resp[label="Compose final response + sources", shape=box]

      U -> C1
      C1 -> EM [label="yes"]
      C1 -> RAG [label="no"]
      RAG -> VS
      VS -> RET
      RET -> OA [label="OpenAI available"]
      RET -> RAGFallback [label="no OpenAI"]
      OA -> Resp
      RAGFallback -> Resp
      RAG -> KB [label="RAG fails"]
      KB -> Resp
    }
    """
    st.graphviz_chart(dot, use_container_width=True)

    st.markdown(
        """
        **Key implementation points**
        - `utils.rag_service.RAGService.query_with_rag()`: performs vector similarity search (k=3), combines context, and calls OpenAI or fallback.
        - `utils.vector_db.VectorDatabaseService`: manages Chroma persistence and embeddings (OpenAI if key is set, else SentenceTransformer `all-MiniLM-L6-v2`).
        - `utils.openai_service.OpenAIService`: wraps Chat Completions; builds system prompt with retrieved context and rights excerpts.
        - `Home.generate_response()`: emergency check → RAG query → knowledge base fallback; tags responses and surfaces sources.
        """
    )


def _rc_flow() -> None:
    st.markdown("### 🏟️ Recreation Centres – Flow")
    dot = r"""
    digraph RCFlow {
      rankdir=LR;
      node [shape=rounded, style=filled, fillcolor="#e8f0ff"];

      U[label="User Input (search text, facilities)"]
      Data[label="In-app curated centres list", shape=box]
      Filter1[label="Normalize text / digits"]
      Match[label="Substring + fuzzy + token match"]
      Fac[label="Facilities filter (any-match)"]
      UI[label="Render cards + map/booking links", shape=box]

      U -> Filter1 -> Match -> Fac -> UI
      Data -> Match
      Data -> UI
    }
    """
    st.graphviz_chart(dot, use_container_width=True)

    st.markdown(
        """
        **Key implementation points**
        - Page: `pages/1_Recreation_Centres.py` holds the curated dataset and UI.
        - Search: substring, postal-code digits match, and fuzzy token ratios with `difflib.SequenceMatcher`.
        - Filters: multiselect of facilities; results rendered as responsive cards with booking and map links.
        - No backend or external API calls required.
        """
    )


def _tips() -> None:
    st.markdown(
        """
        ### Design Tips
        - **Clear labels** and concise descriptions in messages and cards.
        - **Logical flow** with early exits (e.g., emergency responses).
        - **Visual clarity** using consistent components and status tags.
        - **Highlight key points** such as RAG vs general responses.
        """
    )


def main() -> None:
    _header()
    _intro()
    _chat_flow()
    _rc_flow()
    _tips()


if __name__ == "__main__":
    main()


