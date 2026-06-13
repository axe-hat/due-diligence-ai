"""DueDiligenceAI — Streamlit Frontend"""

import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

st.set_page_config(
    page_title="DueDiligenceAI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- sidebar ----------
st.sidebar.title("DueDiligenceAI")
st.sidebar.caption("AI-powered due diligence from SEC filings")

# Try to load available companies
try:
    from src.retrieval.retriever import get_available_companies
    from src.vectorstore.chroma_store import collection_stats
    companies = get_available_companies()
    stats = collection_stats()
    st.sidebar.metric("Chunks Indexed", stats["total_chunks"])
    st.sidebar.metric("Companies", len(companies))
except Exception:
    companies = []
    st.sidebar.warning("No data indexed yet. Run the ingestion pipeline first.")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Built with** ChromaDB, Sentence-Transformers, Ollama, Streamlit"
)

# ---------- tabs ----------
tab1, tab2, tab3 = st.tabs(["Ask a Question", "Due Diligence Report", "Risk Assessment"])

# ========================
# TAB 1: Q&A
# ========================
with tab1:
    st.header("Ask a Question")
    st.markdown("Ask anything about the ingested SEC filings. Answers are source-cited.")

    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input(
            "Your question",
            placeholder="What are Apple's top risk factors in their latest 10-K?",
        )
    with col2:
        selected_company = st.selectbox(
            "Filter by company",
            ["All Companies"] + companies,
            key="qa_company",
        )

    if st.button("Get Answer", key="qa_btn", type="primary") and question:
        company_filter = None if selected_company == "All Companies" else selected_company

        with st.spinner("Retrieving and generating answer..."):
            try:
                from src.generation.qa_chain import answer_question
                result = answer_question(question, company=company_filter)

                # Confidence badge
                conf = result["confidence"]
                if conf >= 0.8:
                    badge_color = "green"
                elif conf >= 0.5:
                    badge_color = "orange"
                else:
                    badge_color = "red"
                st.markdown(
                    f"**Confidence:** :{badge_color}[{conf:.1%}]"
                )

                # Answer
                st.markdown("### Answer")
                st.markdown(result["answer"])

                # Sources
                if result["sources"]:
                    st.markdown("### Sources")
                    for i, src in enumerate(result["sources"]):
                        with st.expander(
                            f"Source {i+1}: {src['company']} | {src['filing_type']} | {src['section']} "
                            f"(relevance: {src['relevance']:.1%})"
                        ):
                            st.text(src["excerpt"])
            except Exception as e:
                st.error(f"Error: {e}")

# ========================
# TAB 2: Executive Summary
# ========================
with tab2:
    st.header("Due Diligence Report")
    st.markdown("Generate a 1-page executive due diligence summary for any company.")

    summary_company = st.selectbox(
        "Select company",
        companies if companies else ["No companies available"],
        key="summary_company",
    )

    if st.button("Generate Report", key="summary_btn", type="primary") and companies:
        with st.spinner(f"Generating executive summary for {summary_company}..."):
            try:
                from src.generation.executive_summary import generate_executive_summary
                result = generate_executive_summary(summary_company)

                st.markdown(f"### Executive Summary: {summary_company}")
                st.markdown(result["summary"])
                st.caption(f"Based on {result['chunks_analyzed']} document chunks")
            except Exception as e:
                st.error(f"Error: {e}")

# ========================
# TAB 3: Risk Assessment
# ========================
with tab3:
    st.header("Risk Assessment")
    st.markdown("Analyze red flags, green flags, and amber flags from SEC filings.")

    risk_company = st.selectbox(
        "Select company",
        companies if companies else ["No companies available"],
        key="risk_company",
    )

    if st.button("Run Risk Assessment", key="risk_btn", type="primary") and companies:
        with st.spinner(f"Analyzing risks for {risk_company}..."):
            try:
                from src.generation.risk_assessor import assess_risk
                result = assess_risk(risk_company)

                st.markdown(f"### Risk Assessment: {risk_company}")
                st.markdown(result["assessment"])
                st.caption(
                    f"Analyzed {result['chunks_analyzed']} chunks | "
                    f"Avg relevance: {result['avg_relevance']:.1%}"
                )
            except Exception as e:
                st.error(f"Error: {e}")
