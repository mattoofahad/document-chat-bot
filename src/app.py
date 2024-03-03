"""Module doc string"""

import openai
import streamlit as st
from openai import OpenAI
from .utils.utils import initiate_streamlit, check_openai_api_key, reset_history, get_pdf_text, discord_hook
discord_hook("Document Chat Bot initiated")

def myapp():
    """_summary_"""
    initiate_streamlit()
    st.title("Simple Chat Bot")

    if st.session_state.openai_api_key is not None:
        if check_openai_api_key():
            client = OpenAI(api_key=st.session_state.openai_api_key)

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Type your Query"):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        max_tokens=st.session_state["openai_maxtokens"],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
        else:
            reset_history()

    with st.sidebar:
        st.session_state.openai_api_key = st.text_input(
            label="OpenAI API key",
            value="***",
            help="This will not be saved or stored.",
            type="password",
        )
        # st.sidebar.write("---")
        st.selectbox(
            "Select the GPT model",
            ("gpt-3.5-turbo", "gpt-4-turbo-preview"),
        )
        st.slider(
            "Max Tokens", min_value=20, max_value=80, step=10, key="openai_maxtokens"
        )
        st.sidebar.write("---")
        uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
        if uploaded_file:
            st.session_state.pdf_text = get_pdf_text(uploaded_file)
            print(st.session_state.pdf_text)
        st.sidebar.write("---")
        st.button(label="Reset Chat", on_click=reset_history)

if __name__ == "__main__":
    myapp()