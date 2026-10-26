"""Interface Streamlit minimale du prototype."""

from __future__ import annotations

import streamlit as st

from src.assistant import reply
from src.contrats import EtatConversation


st.set_page_config(page_title="Assistant bancaire frugal", page_icon="🏦")
st.title("Assistant bancaire frugal")
st.caption("Prototype local — aucune action bancaire réelle n'est exécutée.")

client_id = st.sidebar.selectbox(
    "Client fictif",
    ["CLIENT-001", "CLIENT-002", "CLIENT-003"],
)

if "etat" not in st.session_state:
    st.session_state.etat = EtatConversation()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Écrivez votre demande bancaire…")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    reponse, st.session_state.etat = reply(
        question, client_id, st.session_state.etat
    )
    st.session_state.messages.append({"role": "assistant", "content": reponse.texte})
    st.rerun()

with st.sidebar.expander("Panneau technique", expanded=True):
    etat = st.session_state.etat
    st.write("Intention détectée :", etat.intention or "—")
    if st.session_state.messages:
        st.write("Messages :", len(st.session_state.messages))
        if etat.derniere_reponse:
            st.write("Dernière réponse :", etat.derniere_reponse)
    st.caption("Le détail des étapes sera enrichi par le module de mesure.")
