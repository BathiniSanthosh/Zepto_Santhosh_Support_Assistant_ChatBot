import streamlit as st

from rag import retrieve
from ingest import ingest_documents
from db import collection

# Run ingestion once when app starts
if collection is not None and collection.count() == 0:
    ingest_documents()

st.set_page_config(
    page_title="Zepto Support Assistant_ChatBot",
    page_icon="🤖"
)

st.title("🤖 Zepto Support Assistant")

# Debug info (remove later if desired)
st.sidebar.header("System Status")

if collection is not None:
    st.sidebar.success(
        f"Documents Loaded: {collection.count()}"
    )
else:
    st.sidebar.error(
        "Database unavailable"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input(
    "Ask me about orders, refunds or deliveries..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    result = retrieve(question)

    answer = result["answer"]

    with st.chat_message("assistant"):

        st.markdown(answer)

        if result["sources"]:
            st.caption(
                f"Sources: {', '.join(result['sources'])}"
            )

        st.caption(
            f"Confidence: {result['confidence']:.2f}"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
