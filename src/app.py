"""Module doc string"""

import openai
import streamlit as st
from openai import OpenAI


def return_true():
    """_summary_"""
    return True


def reset_history():
    """_summary_"""
    st.session_state.messages = []


def check_openai_api_key():
    """_summary_"""
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        try:
            client.models.list()
        except openai.AuthenticationError as error:
            with st.chat_message("assistant"):
                st.error(str(error))
            return False
        return True
    except Exception as error:
        with st.chat_message("assistant"):
            st.error(str(error))
        return False


def main():
    """_summary_"""
    st.set_page_config(
        page_title="Test", layout="centered", initial_sidebar_state="auto"
    )
    st.title("Simple Chat Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "openai_api_key" not in st.session_state:
        st.session_state["openai_api_key"] = None

    if "openai_maxtokens" not in st.session_state:
        st.session_state["openai_maxtokens"] = 50

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
        st.text_input(
            label="OpenAI API key",
            value="***",
            key="openai_api_key",
            help="This will not be saved or stored.",
            type="password",
        )

        st.selectbox(
            "Select the GPT model",
            ("gpt-3.5-turbo", "gpt-4-turbo-preview"),
        )
        st.slider(
            "Max Tokens", min_value=20, max_value=80, step=10, key="openai_maxtokens"
        )
        st.button(label="Reset Chat", on_click=reset_history)


if __name__ == "__main__":
    main()
