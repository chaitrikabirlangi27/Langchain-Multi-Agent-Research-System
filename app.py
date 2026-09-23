import streamlit as st
import time


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# IMPORT PROJECT COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────

from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');


/* =========================================================
   MAIN APP
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(20, 184, 255, 0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 100% 100%,
            rgba(124, 58, 237, 0.16),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #061321 0%,
            #081426 100%
        );

    color: #f8fbff;
}


/* =========================================================
   HIDE STREAMLIT DEFAULT UI
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   PAGE CONTAINER
   ========================================================= */

.block-container {
    max-width: 1350px !important;
    padding: 1rem 3.5rem 4rem !important;
}


/* =========================================================
   HERO SECTION
   ========================================================= */

.hero {
    text-align: center;
    padding-top: 2.5rem;
    padding-bottom: 2rem;
}

.hero-icon {
    font-size: 4rem;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 4.7rem;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.04em;
    color: #f8fbff;
    margin: 0;
}

.hero-title span {
    background: linear-gradient(
        135deg,
        #38bdf8 10%,
        #6366f1 55%,
        #8b5cf6 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-family: 'Syne', sans-serif;
    font-size: 1.65rem;
    font-weight: 600;
    color: #edf3ff;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
}

.hero-description {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 300;
    color: #b9c7da;
    margin: 0 auto;
    max-width: 900px;
}


/* =========================================================
   DIVIDER
   ========================================================= */

.divider {
    height: 1px;
    margin: 1.5rem 0 2.8rem;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(56, 189, 248, 0.30),
        transparent
    );
}


/* =========================================================
   RESEARCH TOPIC LABEL
   ========================================================= */

.stTextInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #38bdf8 !important;
}


/* =========================================================
   RESEARCH INPUT
   ========================================================= */

.stTextInput > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.stTextInput input {
    height: 64px !important;

    background: #152438 !important;

    color: #f8fbff !important;

    border: 1px solid rgba(56, 189, 248, 0.48) !important;

    border-radius: 15px !important;

    padding: 0 1.25rem !important;

    font-family: 'DM Sans', sans-serif !important;

    font-size: 1.08rem !important;

    box-shadow: none !important;
}

.stTextInput input::placeholder {
    color: #aab9cd !important;
    opacity: 1 !important;
}

.stTextInput input:focus {
    background: #182b41 !important;

    border-color: #38bdf8 !important;

    box-shadow:
        0 0 0 3px rgba(56, 189, 248, 0.12) !important;

    outline: none !important;
}


/* =========================================================
   RUN BUTTON
   ========================================================= */

.stButton > button {
    height: 64px !important;

    background: linear-gradient(
        135deg,
        #38bdf8 0%,
        #6366f1 52%,
        #8b5cf6 100%
    ) !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 15px !important;

    font-family: 'Syne', sans-serif !important;

    font-size: 1.08rem !important;

    font-weight: 700 !important;

    letter-spacing: 0.02em !important;

    box-shadow:
        0 12px 35px rgba(56, 189, 248, 0.22) !important;

    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;

    box-shadow:
        0 16px 40px rgba(56, 189, 248, 0.32) !important;
}


/* =========================================================
   TRY SECTION
   ========================================================= */

.try-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.76rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #8da0b8;
    margin-top: 2.3rem;
    margin-bottom: 0.9rem;
}

.example-container {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
}

.example-chip {
    display: inline-block;

    padding: 0.75rem 1.15rem;

    border-radius: 10px;

    background: rgba(255, 255, 255, 0.045);

    border: 1px solid rgba(255, 255, 255, 0.11);

    color: #dce6f3;

    font-family: 'DM Sans', sans-serif;

    font-size: 0.9rem;
}


/* =========================================================
   PIPELINE
   ========================================================= */

.pipeline-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f8fbff;
    margin-top: 3.5rem;
    margin-bottom: 1rem;
}

.pipeline-card {
    background: rgba(255, 255, 255, 0.035);

    border: 1px solid rgba(255, 255, 255, 0.09);

    border-radius: 15px;

    padding: 1.2rem 1.5rem;

    margin-bottom: 0.8rem;
}

.pipeline-card.done {
    border-color: rgba(34, 197, 94, 0.28);
    background: rgba(34, 197, 94, 0.04);
}

.pipeline-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
}

.pipeline-number {
    font-family: 'DM Mono', monospace;
    color: #38bdf8;
    font-size: 0.75rem;
}

.pipeline-name {
    font-family: 'Syne', sans-serif;
    color: #f8fbff;
    font-size: 1rem;
    font-weight: 700;
}

.pipeline-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #22c55e;
}

.pipeline-description {
    margin-left: 2rem;
    margin-top: 0.35rem;
    color: #8da0b8;
    font-size: 0.85rem;
}


/* =========================================================
   RESULTS
   ========================================================= */

.results-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f8fbff;
    margin-top: 3rem;
    margin-bottom: 1rem;
}

.report-box {
    background: rgba(255, 255, 255, 0.035);

    border: 1px solid rgba(56, 189, 248, 0.22);

    border-radius: 17px;

    padding: 1.8rem 2rem;

    margin-top: 1.5rem;
}

.report-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #38bdf8;
    padding-bottom: 0.8rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(56, 189, 248, 0.15);
}

.critic-box {
    background: rgba(255, 255, 255, 0.035);

    border: 1px solid rgba(34, 197, 94, 0.22);

    border-radius: 17px;

    padding: 1.8rem 2rem;

    margin-top: 1.5rem;
}

.critic-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #22c55e;
    padding-bottom: 0.8rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(34, 197, 94, 0.15);
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer-text {
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #64748b;
    margin-top: 4rem;
    padding-bottom: 1rem;
}

</style>
""",
unsafe_allow_html=True
)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

if "results" not in st.session_state:
    st.session_state.results = {}

if "running" not in st.session_state:
    st.session_state.running = False

if "done" not in st.session_state:
    st.session_state.done = False


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
"""
<div class="hero">

<div class="hero-icon">🔬</div>

<div class="hero-title">
AI Research <span>Assistant</span>
</div>

<div class="hero-subtitle">
Multi-Agent Research System
</div>

<div class="hero-description">
Search → Read → Write → Critique — to deliver a polished research report on any topic.
</div>

</div>

<div class="divider"></div>
""",
unsafe_allow_html=True
)


# ─────────────────────────────────────────────────────────────────────────────
# RESEARCH TOPIC
# ─────────────────────────────────────────────────────────────────────────────

topic = st.text_input(
    "Research Topic",
    placeholder="Enter your research topic here...",
    key="topic_input"
)


# ─────────────────────────────────────────────────────────────────────────────
# RUN BUTTON
# ─────────────────────────────────────────────────────────────────────────────

run_btn = st.button(
    "⚡ Run Research Pipeline",
    use_container_width=True
)


# ─────────────────────────────────────────────────────────────────────────────
# EXAMPLE TOPICS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
"""
<div class="try-label">
TRY →
</div>

<div class="example-container">

<span class="example-chip">
Latest AI tools for developers
</span>

<span class="example-chip">
How Generative AI is Transforming Software Development in 2026
</span>

<span class="example-chip">
Python programming language
</span>

</div>
""",
unsafe_allow_html=True
)


# ─────────────────────────────────────────────────────────────────────────────
# START PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

if run_btn:

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

    else:

        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False

        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# RUN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

if (
    st.session_state.running
    and not st.session_state.done
):

    results = {}

    # Read the topic from session state before any pipeline step.
    topic_val = st.session_state.get("topic_input", "").strip()

    if not topic_val:
        st.session_state.running = False
        st.warning("Please enter a research topic first.")
        st.stop()

    # =====================================================
    # STEP 1 — SEARCH AGENT
    # =====================================================

    with st.spinner("🔍 Search Agent is working..."):

        search_agent = build_search_agent()

        try:
            sr = search_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"""
Find recent, reliable and detailed information about:

{topic_val}

Use the web search tool to find relevant sources.
Make sure the search results contain the actual URLs.
"""
                        )
                    ]
                }
            )

            # Prefer the actual result returned by the web_search tool.
            # This preserves the URLs for the Reader Agent.
            tool_messages = [
                msg for msg in sr["messages"]
                if getattr(msg, "type", "") == "tool"
            ]

            if tool_messages:
                results["search"] = tool_messages[-1].content
            else:
                results["search"] = sr["messages"][-1].content

        except Exception as e:
            st.error(f"Search Agent failed: {e}")
            st.session_state.running = False
            st.stop()

        st.session_state.results = dict(results)

    # =====================================================
    # STEP 2 — READER AGENT
    # =====================================================

    with st.spinner("📄 Reader Agent is scraping top resources..."):

        reader_agent = build_reader_agent()

        # Keep the Reader request small enough for Groq.
        search_for_reader = results["search"][:1500]

        try:
            rr = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"""
For the topic "{topic_val}", use the search results below.

Choose one of the actual URLs shown in the search results.
Use the scrape_url tool to scrape that URL and return the
important extracted content.

SEARCH RESULTS:
{search_for_reader}
"""
                        )
                    ]
                }
            )

            results["reader"] = rr["messages"][-1].content

        except Exception as e:
            st.warning(
                "Reader Agent could not complete the scrape. "
                "The report will continue using the available search results."
            )
            results["reader"] = f"Reader Agent error: {e}"

        st.session_state.results = dict(results)

    # =====================================================
    # STEP 3 — WRITER
    # =====================================================

    with st.spinner("✍️ Writer is drafting the research report..."):

        # Limit the research passed to the Writer to keep
        # the Groq request size manageable.
        research_combined = (
            f"SEARCH RESULTS:\n{results['search'][:2500]}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader'][:3500]}"
        )

        try:
            results["writer"] = writer_chain.invoke(
                {
                    "topic": topic_val,
                    "research": research_combined
                }
            )

        except Exception as e:
            st.error(f"Writer Chain failed: {e}")
            st.session_state.running = False
            st.stop()

        st.session_state.results = dict(results)

    # =====================================================
    # STEP 4 — CRITIC
    # =====================================================

    with st.spinner("🧐 Critic is reviewing the report..."):

        try:
            results["critic"] = critic_chain.invoke(
                {
                    "report": results["writer"][:6000]
                }
            )

        except Exception as e:
            st.warning(f"Critic Chain could not complete: {e}")
            results["critic"] = f"Critic Chain error: {e}"

        st.session_state.results = dict(results)

    # =====================================================
    # PIPELINE COMPLETE
    # =====================================================

    st.session_state.running = False
    st.session_state.done = True

    st.rerun()



# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────

r = st.session_state.results


if r:

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # PIPELINE
    # =====================================================

    st.markdown(
        '<div class="pipeline-heading">Pipeline</div>',
        unsafe_allow_html=True
    )


    pipeline_steps = [
        (
            "01",
            "Search Agent",
            "Gathers recent web information"
        ),
        (
            "02",
            "Reader Agent",
            "Scrapes and extracts deep content"
        ),
        (
            "03",
            "Writer Chain",
            "Drafts the research report"
        ),
        (
            "04",
            "Critic Chain",
            "Reviews and scores the report"
        )
    ]


    for number, name, description in pipeline_steps:

        st.markdown(
            f"""
<div class="pipeline-card done">

<div class="pipeline-header">

<span class="pipeline-number">
{number}
</span>

<span class="pipeline-name">
{name}
</span>

<span class="pipeline-status">
✓ DONE
</span>

</div>

<div class="pipeline-description">
{description}
</div>

</div>
""",
            unsafe_allow_html=True
        )


    # =====================================================
    # RESEARCH RESULTS
    # =====================================================

    st.markdown(
        '<div class="results-heading">Research Results</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # SEARCH RESULTS
    # =====================================================

    if "search" in r:

        with st.expander(
            "🔍 Search Results",
            expanded=False
        ):

            st.markdown(
                r["search"]
            )


    # =====================================================
    # SCRAPED CONTENT
    # =====================================================

    if "reader" in r:

        with st.expander(
            "📄 Scraped Content",
            expanded=False
        ):

            st.markdown(
                r["reader"]
            )


    # =====================================================
    # FINAL REPORT
    # =====================================================

    if "writer" in r:

        st.markdown(
            """
<div class="report-box">

<div class="report-label">
📝 Final Research Report
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            r["writer"]
        )


        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=(
                f"research_report_{int(time.time())}.md"
            ),
            mime="text/markdown"
        )


    # =====================================================
    # CRITIC FEEDBACK
    # =====================================================

    if "critic" in r:

        st.markdown(
            """
<div class="critic-box">

<div class="critic-label">
🧐 Critic Feedback
</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            r["critic"]
        )


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
"""
<div class="footer-text">
AI Research Assistant · Powered by LangChain Multi-Agent Pipeline · Built with Streamlit
</div>
""",
unsafe_allow_html=True
)
