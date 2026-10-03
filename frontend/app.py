import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("AI Chatbot")

if "conversation_id" not in st.session_state:
    response = requests.post(
        BACKEND_URL + "/conversations"
    )
    st.session_state.conversation_id = (
        response.json()["conversation_id"]
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    history = st.session_state.messages.copy()
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    try:
        response = requests.post(
            BACKEND_URL + "/chat/stream",
            json={
                "message": prompt,
                "history": history,
            },
            stream=True,
            timeout=60,
        )

        if response.status_code == 200:
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                for chunk in response.iter_content(
                    chunk_size=None,
                    decode_unicode=True,
                ):

                    if chunk:
                        full_response += chunk
                        response_placeholder.markdown(
                            full_response
                        )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )
        else:
            try:
                error_data = response.json()
                st.error(
                    error_data.get(
                        "detail",
                        "Something went wrong.",
                    )
                )
            except ValueError:
                st.error(
                    "Something went wrong while generating the response."
                )
    except requests.exceptions.RequestException:
        st.error(
            "Could not connect to the backend."
        )