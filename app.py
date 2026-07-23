#uv run streamlit run app.py

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

# OpenAI-Client initialisieren
client = OpenAI()

st.title("🤖 Chatbot")
st.write("Gebe eine Frage ein und erhalte eine Antwort von der KI!")

# 1. Chat-Verlauf im Session-State initialisieren, falls die Seite neu geladen wurde
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Alle bisherigen Chat-Nachrichten bei jedem Seiten-Rerun anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3. Das moderne Eingabefeld am unteren Bildschirmrand nutzen
if prompt := st.chat_input("Schreibe eine Nachricht..."):
    
    # A. Benutzereingabe sofort im UI anzeigen
    with st.chat_message("user"):
        st.write(prompt)
    
    # B. Benutzereingabe im Session-State speichern
    st.session_state.messages.append({"role": "user", "content": prompt})

    # C. Antwort vom Assistenten generieren
    with st.chat_message("assistant"):
        with st.spinner("Antwort wird generiert..."):
            try:
                # Wir übergeben die gesamte 'messages'-Liste als 'input'.
                # Dadurch 'erinnert' sich die KI an den Kontext des bisherigen Gesprächs.
                response = client.responses.create(
                    model="gpt-5-nano",
                    instructions="You are a helpful assistant.",
                    input=st.session_state.messages
                )
                
                assistant_response = response.output_text
                
                # Antwort im UI anzeigen
                st.write(assistant_response)
                
                # Antwort im Session-State speichern, damit sie beim nächsten Rerun bestehen bleibt
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
            except Exception as e:
                st.error(f"Ein Fehler ist aufgetreten: {e}")