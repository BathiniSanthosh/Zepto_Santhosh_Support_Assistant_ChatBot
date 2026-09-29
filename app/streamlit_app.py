import streamlit as st

from rag import retrieve
from ingest import ingest_documents
from db import collection

# Run ingestion once when app starts
if collection is not None and collection.count() == 0:
    ingest_documents()

st.set_page_config(
    page_title="Zepto Support Assistant ChatBot",
    page_icon="🤖",
    layout="wide"
)

# Main Header
st.title("🤖 Zepto Support Assistant")

# Knowledge Base Status
if collection is not None:
    st.success(
        f"📄 Knowledge Base Ready | Documents Loaded: {collection.count()}"
    )
else:
    st.error("❌ Database unavailable")

# Suggested Questions
with st.expander("💡 Sample Questions You Can Ask", expanded=False):
    st.markdown("""
    - What is Zepto's refund policy?
    - How can I cancel an order?
    - What happens if an item is damaged?
    - How long does a refund take?
    - What payment methods are accepted?
    - How can I contact customer support?
    - What is Zepto Pass subscription?
    - What happens if my order is delayed?
    - How are refunds processed?
    - How do I report a missing item?
    """)

# Sidebar
st.sidebar.header("System Status")

if collection is not None:
    st.sidebar.success(
        f"Documents Loaded: {collection.count()}"
    )
else:
    st.sidebar.error(
        "Database unavailable"
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if (
            msg["role"] == "assistant"
            and "sources" in msg
        ):
            st.caption(
                f"Sources: {', '.join(msg['sources'])}"
            )

            st.caption(
                f"Confidence: {msg['confidence']:.2f}"
            )

# Chat input
question = st.chat_input(
    "Ask me about orders, refunds or deliveries..."
)

if question:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Get answer
    result = retrieve(question)

    answer = result["answer"]

    # Assistant message
    with st.chat_message("assistant"):

        st.markdown(answer)

        if result["sources"]:
            st.caption(
                f"Sources: {', '.join(result['sources'])}"
            )

        st.caption(
            f"Confidence: {result['confidence']:.2f}"
        )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": result["sources"],
            "confidence": result["confidence"]
        }
    )
