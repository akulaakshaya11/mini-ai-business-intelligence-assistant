
import requests
import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# Configuration
# --------------------------------------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="InsightAI | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

# --------------------------------------------------
# Premium dashboard styling
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #0b1020;
    --panel: #111a2e;
    --border: #26334d;
    --text: #f1f5ff;
    --muted: #94a3b8;
    --accent: #8b7cff;
    --cyan: #5eead4;
}

.stApp {
    background:
        radial-gradient(ellipse at 70% 0%, #1b2750 0%, transparent 42%),
        #0b1020;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0d1425;
    border-right: 1px solid #26334d;
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f1f5ff !important;
    letter-spacing: -0.6px;
}

p, label, li {
    color: #c0cbe0;
}

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -1px;
}

.brand span {
    color: #a99cff;
}

.brand-icon {
    display: inline-flex;
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: linear-gradient(135deg, #8b7cff, #5e68e8);
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 12px;
    box-shadow: 0 8px 30px #7465ff33;
}

.eyebrow {
    color: #a99cff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero {
    padding: 32px;
    border: 1px solid #344164;
    border-radius: 24px;
    background:
        radial-gradient(circle at 90% 20%, #7565ff26, transparent 35%),
        linear-gradient(135deg, #17223b, #10172a 75%);
    margin: 8px 0 26px 0;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(30px, 4vw, 44px);
    font-weight: 700;
    line-height: 1.15;
    letter-spacing: -1.7px;
    color: #f8fafc;
    margin: 12px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #b6aaff, #6ee7dc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-copy {
    color: #a9b7d0;
    font-size: 15px;
    line-height: 1.8;
    max-width: 700px;
}

.pill {
    display: inline-block;
    border: 1px solid #394766;
    border-radius: 30px;
    background: #1c2944;
    color: #c6d1e8;
    font-size: 11px;
    padding: 6px 11px;
    margin: 12px 5px 0 0;
}

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: #edf2ff;
    margin: 10px 0 5px;
}

.section-caption {
    font-size: 13px;
    color: #8494b2;
    margin-bottom: 16px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, #131e34, #10182a);
    border: 1px solid #293753;
    border-radius: 16px;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #344361;
    background: #151f34;
    color: #e3eaff;
    min-height: 43px;
    transition: all 0.2s ease;
    font-weight: 500;
}

div.stButton > button:hover {
    border-color: #9a8cff;
    color: #ffffff;
    background: #202a46;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #7868f6, #5d70e9);
    border: none;
    color: white;
    font-weight: 700;
    box-shadow: 0 6px 20px #7565ff25;
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(100deg, #8d80ff, #7083ff);
    box-shadow: 0 8px 28px #7565ff45;
}

div[data-testid="stTextInput"] input {
    background: #101a2d;
    color: #f1f5ff;
    border: 1px solid #344361;
    border-radius: 12px;
    min-height: 48px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #9a8cff;
    box-shadow: 0 0 0 1px #9a8cff;
}

div[data-testid="stMetric"] {
    background: #131e34;
    border: 1px solid #2b3956;
    padding: 17px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"] {
    color: #98a8c4;
}

div[data-testid="stMetricValue"] {
    color: #f1f5ff;
    font-family: 'Space Grotesk', sans-serif;
}

[data-testid="stDataFrame"] {
    border: 1px solid #293753;
    border-radius: 12px;
}

hr {
    border-color: #26334d;
}

.small-muted {
    color: #8292b0;
    font-size: 12px;
}

.answer-banner {
    border: 1px solid #31544f;
    background: linear-gradient(100deg, #12302f, #14253a);
    border-radius: 14px;
    padding: 17px 20px;
    margin: 10px 0 18px;
}

.footer {
    color: #71819e;
    font-size: 12px;
    text-align: center;
    padding: 28px 0 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def check_api():
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.ok
    except requests.RequestException:
        return False


def pretty_label(value):
    return str(value).replace("_", " ").title()


def format_value(key, value):
    if value is None:
        return "Not available"

    key_lower = key.lower()

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, (int, float)):
        if "percentage" in key_lower or "percent" in key_lower:
            return f"{value:,.2f}%"
        if any(word in key_lower for word in
               ["revenue", "difference", "amount", "sales"]):
            return f"{value:,.0f}"
        return f"{value:,}"

    return str(value)


def render_answer(answer):
    """Render structured API answers as readable cards and tables."""

    if not isinstance(answer, dict) or not answer:
        st.info(str(answer))
        return

    for section_name, data in answer.items():
        st.markdown(
            f'<div class="section-heading">{pretty_label(section_name)}</div>',
            unsafe_allow_html=True,
        )

        # Dictionary responses become metric cards.
        if isinstance(data, dict):
            items = list(data.items())

            # Product answer: make the product name prominent.
            if "product" in data and "revenue" in data:
                st.markdown(
                    f"""
                    <div class="answer-banner">
                        <div class="eyebrow">TOP-PERFORMING PRODUCT</div>
                        <div style="font-size:30px;font-weight:700;
                                    color:#f8fafc;margin-top:7px">
                            {data["product"]}
                        </div>
                        <div style="color:#a8b8d3;margin-top:5px">
                            Revenue: {format_value("revenue", data["revenue"])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                remaining = [
                    (k, v) for k, v in items
                    if k not in ("product", "revenue")
                ]
                if remaining:
                    cols = st.columns(min(len(remaining), 4))
                    for i, (key, value) in enumerate(remaining):
                        with cols[i % len(cols)]:
                            st.metric(pretty_label(key), format_value(key, value))
                continue

            # Month comparison: display the main figures together.
            if "revenue_a" in data and "revenue_b" in data:
                cols = st.columns(4)
                metrics = [
                    ("Month A", data.get("month_a", "—")),
                    ("Revenue A", format_value("revenue_a", data["revenue_a"])),
                    ("Revenue B", format_value("revenue_b", data["revenue_b"])),
                    ("Change", format_value(
                        "percentage_change",
                        data.get("percentage_change")
                    )),
                ]

                for col, (label, value) in zip(cols, metrics):
                    with col:
                        st.metric(label, value)

                if "difference" in data:
                    st.caption(
                        f"Absolute revenue difference: "
                        f"{format_value('difference', data['difference'])}"
                    )
                continue

            # General structured answer.
            cols = st.columns(min(len(items), 4))
            for i, (key, value) in enumerate(items):
                with cols[i % len(cols)]:
                    if isinstance(value, (dict, list)):
                        st.markdown(f"**{pretty_label(key)}**")
                        if isinstance(value, dict):
                            st.json(value)
                        else:
                            st.dataframe(
                                pd.DataFrame(value),
                                use_container_width=True,
                                hide_index=True,
                            )
                    else:
                        st.metric(pretty_label(key), format_value(key, value))

        # List responses become tables, with an optional chart.
        elif isinstance(data, list):
            if data and all(isinstance(row, dict) for row in data):
                df = pd.DataFrame(data)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                numeric_cols = df.select_dtypes(
                    include="number"
                ).columns.tolist()

                # Plot only when a numeric series is available.
                if numeric_cols and len(df) > 1:
                    chart_col = next(
                        (
                            col for col in numeric_cols
                            if any(term in col.lower()
                                   for term in ["revenue", "sales", "amount"])
                        ),
                        numeric_cols[0],
                    )
                    st.markdown("**Trend visualization**")
                    st.line_chart(df.set_index(df.columns[0])[[chart_col]])

            else:
                st.write(data)

        else:
            st.metric(pretty_label(section_name), format_value(section_name, data))


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand-icon">✦</div>
        <div class="brand">Insight<span>AI</span></div>
        <div class="small-muted">BUSINESS INTELLIGENCE PLATFORM</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("#### Workspace")
    st.markdown("📊  Sales Analytics")
    st.markdown("✦  AI Question Assistant")
    st.markdown("🗂️  Query History")

    st.divider()

    st.markdown("#### System status")
    api_online = check_api()

    if api_online:
        st.success("API connected", icon="🟢")
    else:
        st.error("API unavailable", icon="🔴")
        st.caption("Start FastAPI to run queries.")

    st.divider()

    st.markdown("#### Capabilities")
    st.markdown(
        """
        <div class="small-muted">
        ✓ Revenue analysis<br><br>
        ✓ Product performance<br><br>
        ✓ Regional comparison<br><br>
        ✓ Monthly trends<br><br>
        ✓ Natural-language questions
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    if st.button("Clear query history", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    st.markdown(
        '<div class="small-muted">InsightAI · Student project</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Hero
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">INTELLIGENCE, WITHOUT THE COMPLEXITY</div>
        <div class="hero-title">
            Your data.<br>
            <span class="gradient-text">Your questions. Clear answers.</span>
        </div>
        <div class="hero-copy">
            Explore business performance using natural language.
            Ask a question, let AI interpret your intent, and get
            answers powered by real SQL analytics.
        </div>
        <span class="pill">✦ Gemini AI</span>
        <span class="pill">◈ FastAPI</span>
        <span class="pill">▦ SQLite Analytics</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Query workspace
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">Ask your business data</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Ask in plain English. No SQL knowledge required.'
    '</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown("**✦  AI Query Workspace**")

    question = st.text_input(
        "Your question",
        key="question_input",
        placeholder="e.g. Which product generated the highest revenue?",
        label_visibility="collapsed",
    )

    col_ask, col_hint = st.columns([1, 3])

    with col_ask:
        ask_clicked = st.button(
            "✦  Analyze question",
            type="primary",
            use_container_width=True,
        )

    with col_hint:
        st.markdown(
            '<div class="small-muted" style="padding-top:12px">'
            'AI interprets your question · SQL calculates the answer'
            '</div>',
            unsafe_allow_html=True,
        )

    if ask_clicked:
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            with st.spinner("Interpreting your question and analyzing data..."):
                try:
                    response = requests.post(
                        f"{API_URL}/ask",
                        json={"question": question.strip()},
                        timeout=90,
                    )

                    if response.ok:
                        result = response.json()
                        st.session_state.last_result = result
                        st.session_state.last_question = question.strip()

                        st.session_state.history.insert(
                            0,
                            {
                                "question": question.strip(),
                                "intent": result.get(
                                    "interpreted_intent", "unknown"
                                ),
                                "time": datetime.now().strftime("%H:%M"),
                                "result": result,
                            },
                        )
                        st.session_state.history = (
                            st.session_state.history[:10]
                        )
                    else:
                        st.error(
                            f"Request failed ({response.status_code}). "
                            f"{response.text[:500]}"
                        )

                except requests.RequestException as exc:
                    st.error(
                        "Could not reach the backend. Make sure FastAPI "
                        "is running in your other terminal."
                    )
                    st.caption(str(exc))


# --------------------------------------------------
# Quick prompts
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">Explore with one click</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Try one of these popular business questions.'
    '</div>',
    unsafe_allow_html=True,
)

quick_questions = [
    ("💰", "Total revenue", "What is the total revenue?"),
    ("🏆", "Top product", "Which product generated the highest revenue?"),
    ("🌍", "Top region", "Which region generated the highest revenue?"),
    ("📈", "Monthly trend", "Show me the monthly revenue trend."),
    (
        "↔️",
        "Compare months",
        "Compare revenue between April 2026 and May 2026.",
    ),
]

quick_cols = st.columns(5)

def select_question(prompt):
    st.session_state.question_input = prompt


for col, (emoji, label, prompt) in zip(quick_cols, quick_questions):
    with col:
        with st.container(border=True):
            st.markdown(f"### {emoji}")
            st.markdown(f"**{label}**")
            st.button(
                "Use question",
                key=f"quick_{label}",
                use_container_width=True,
                on_click=select_question,
                args=(prompt,),
            )


# --------------------------------------------------
# Latest answer
# --------------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="section-heading">Analysis results</div>',
    unsafe_allow_html=True,
)

result = st.session_state.last_result

if result:
    st.markdown(
        """
        <div class="answer-banner">
            <span style="color:#5eead4;font-weight:700">
                ✓ ANALYSIS COMPLETED
            </span>
            <div style="color:#aab8d0;font-size:13px;margin-top:5px">
                Your answer is based on the connected analytics API.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("**Your question**")
        st.write(result.get("question", st.session_state.last_question))

        st.markdown(
            f'<span class="pill">Intent: '
            f'{result.get("interpreted_intent", "unknown")}</span>',
            unsafe_allow_html=True,
        )

        st.markdown("")
        render_answer(result.get("answer", {}))

        with st.expander("View raw API response"):
            st.json(result)

else:
    with st.container(border=True):
        st.markdown("### ✨ Your insights will appear here")
        st.write(
            "Ask a question above or choose one of the suggested prompts. "
            "Your results will appear here as soon as the analysis finishes."
        )
        st.caption(
            "Example: Compare revenue between April 2026 and May 2026."
        )


# --------------------------------------------------
# Recent queries
# --------------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="section-heading">Recent queries</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Your latest questions in this session.'
    '</div>',
    unsafe_allow_html=True,
)

if st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        with st.container(border=True):
            col_question, col_intent, col_time = st.columns([5, 2, 1])

            with col_question:
                st.markdown(f"**{item['question']}**")

            with col_intent:
                st.caption(item["intent"])

            with col_time:
                st.caption(item["time"])

            if st.button(
                "View result",
                key=f"history_{i}",
            ):
                st.session_state.last_result = item["result"]
                st.session_state.last_question = item["question"]
                st.rerun()
else:
    st.caption("Your completed questions will appear here.")


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        INSIGHTAI &nbsp;·&nbsp; AI-POWERED BUSINESS INTELLIGENCE
        <br><br>
        Gemini interprets questions. SQL performs the calculations.
    </div>
    """,
    unsafe_allow_html=True,
)
