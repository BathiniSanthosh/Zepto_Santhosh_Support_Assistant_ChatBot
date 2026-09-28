import streamlit as st
from rag import retrieve

st.set_page_config(
    page_title="Zepto Support Assistant_ChatBot",
    page_icon="🤖"
)

st.title("🤖 Zepto Support Assistant")

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

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )