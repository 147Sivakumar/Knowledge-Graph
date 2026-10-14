
import streamlit as st
from langchain_graphrag_chatbot import answer_question

st.set_page_config(
    page_title="GraphRAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #111827);
    color: #f8fafc;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #263449;
}
.hero {
    padding: 1.5rem;
    border: 1px solid #334155;
    border-radius: 20px;
    background: linear-gradient(120deg, #172554, #172033);
    margin-bottom: 1.5rem;
}
.hero h1 {
    color: #ffffff;
    margin-bottom: 0.3rem;
}
.hero p {
    color: #cbd5e1;
    margin-bottom: 0;
}
.stChatMessage {
    border: 1px solid #293548;
    border-radius: 16px;
    padding: 1rem;
    background: #131d2e;
}
div[data-testid="stChatInput"] {
    border-color: #475569;
}
.small-note {
    color: #94a3b8;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = []

# Sidebar
with st.sidebar:
    st.markdown("## 🧠 GraphRAG")
    st.caption("Knowledge Graph Assistant")
    st.divider()

    st.markdown("### Your workspace")
    st.markdown("🔗 Neo4j AuraDB")
    st.markdown("🕸️ NetworkX")
    st.markdown("✨ LangChain + OpenAI")

    st.divider()
    st.markdown("### Try asking")
    st.markdown("- What schemes are in my graph?")
    st.markdown("- Which departments are connected?")
    st.markdown("- Tell me more about that scheme.")
    st.markdown("- What benefits are recorded?")

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memory = []
        st.rerun()

    st.markdown(
        '<p class="small-note">Conversation memory lasts '
        'until this session is reset.</p>',
        unsafe_allow_html=True,
    )

# Main page
st.markdown("""
<div class="hero">
    <h1>✨ GraphRAG Assistant</h1>
    <p>Explore your government schemes knowledge graph
    using natural language.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("### 👋 Welcome!")
    st.write(
        "Ask a question about your knowledge graph. "
        "I'll retrieve relevant facts and use them to formulate an answer."
    )

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask your knowledge graph anything...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your knowledge graph..."):
            try:
                answer = answer_question(
                    question,
                    st.session_state.memory,
                )
            except Exception as error:
                answer = (
                    f"Sorry, something went wrong: "
                    f"{type(error).__name__}: {error}"
                )

        st.markdown(answer)

    # Save this exchange for follow-up questions
    st.session_state.memory.extend([
        f"You: {question}",
        f"Assistant: {answer}",
    ])

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })
