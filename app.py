# frontend/src/frontend/app.py
#uv run streamlit run frontend/src/frontend/app.py

import streamlit as st

st.title("RAG Chatbot")

question = st.text_input("Deine Frage")

if question:
    st.write("Antwort kommt später vom Backend.")
