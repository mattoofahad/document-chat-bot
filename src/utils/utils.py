from discord_webhook import DiscordWebhook
from openai import OpenAI
import openai
import streamlit as st
import pdfplumber
import os
from dotenv import load_dotenv
load_dotenv()

def initiate_streamlit():
    st.set_page_config(
        page_title="Test", layout="centered", initial_sidebar_state="auto"
    )
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"

    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = None

    if "openai_maxtokens" not in st.session_state:
        st.session_state.openai_maxtokens = 50

    if "pdf_file" not in st.session_state:
        st.session_state.pdf_file = None


def reset_history():
    """_summary_"""
    st.session_state.messages = []


def discord_hook(message):
    url = os.environ['DISCORD_HOOK']
    webhook = DiscordWebhook(
        url=url, username="document-chat-bot", content=message
    )
    webhook.execute()


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


def get_pdf_text(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for pages in pdf.pages:
            text += pages.extract_text()
    return text
