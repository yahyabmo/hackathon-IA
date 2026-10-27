"""Thème autonome : styles locaux, aucun appel réseau."""
from pathlib import Path
import streamlit as st


def injecter() -> None:
    css = Path(__file__).with_name("styles.css").read_text(encoding="utf-8")
    st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)
