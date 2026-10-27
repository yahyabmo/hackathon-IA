"""Interface de démonstration : conversation, contexte et preuve de frugalité."""

from __future__ import annotations

import streamlit as st
from html import escape

from src import llm
from src.assistant import reply
from src.comprendre import classifieur
from src.conseiller import clients
from src.contrats import EtatConversation
from src.mesure import resumer
from src.ui import components, theme

MESSAGES_DEMO = {
    "C01": [("Carte perdue", "J'ai perdu ma carte hier soir, je fais quoi ?"), ("Confirmer", "oui")],
    "C02": [("Frais", "Pourquoi j'ai payé 8 € de frais ce mois-ci ?")],
    "C03": [("Épargne enfants", "Je voudrais mettre de côté pour mes enfants."), ("Projet", "Dans 10 ans, 100 euros par mois")],
    "C04": [("Virement", "Je dois envoyer 500 € à mon fils."), ("Confirmer", "oui")],
    "C05": [("Crédit auto", "Je veux un crédit pour acheter une voiture."), ("Montant", "12000"), ("Durée", "48 mois")],
    "C06": [("Insatisfaction", "Votre appli ne marche jamais !")],
    "C07": [("Immobilier", "Je veux acheter un appartement"), ("Budget", "Autour de 250 000, et je peux mettre les 25 000"), ("Alternative", "Et avec un bien à 200 000 ?")],
    "C08": [("Épargne", "Je voudrais mettre de côté"), ("Horizon", "Dans 2 ans"), ("Versement", "50 euros"), ("TAEG", "C'est quoi un TAEG ?")],
}

def _initialiser(client_id: str) -> None:
    st.session_state.client = client_id
    st.session_state.etat = EtatConversation()
    st.session_state.messages = []
    st.session_state.derniere = None
    st.session_state.reponses = []


def _envoyer(message: str) -> None:
    st.session_state.etat.mots_simples = st.session_state.get("mots_simples", False)
    with st.spinner("Noria prépare votre réponse…"):
        reponse, etat = reply(message, st.session_state.client, st.session_state.etat)
    st.session_state.messages.append({"role": "user", "content": message})
    st.session_state.etat = etat
    st.session_state.messages.append({"role": "assistant", "content": reponse.texte})
    st.session_state.derniere = reponse
    st.session_state.reponses.append(reponse)


@st.cache_data(ttl=30, show_spinner=False)
def _serveur_joignable(role: str) -> bool:
    return llm.joignable(role)


def _statut_moteur() -> tuple[str, str]:
    if not llm.actif():
        return "Local · gabarits", "Le LLM est désactivé. La cascade répond localement."
    if not _serveur_joignable("formulation"):
        return "Local · gabarits", "Serveur LLM injoignable. Réponse de secours active."
    return f"Local · {llm.MODELE_FORMULATION}", "Serveur LLM local joignable."


def _statut_comprehension() -> str:
    if not classifieur.TETES.exists():
        return "Mots-clés · classifieur non chargé"
    return "Classifieur configuré · disponibilité non vérifiée"


st.set_page_config(page_title="Noria · assistant bancaire", page_icon="N", layout="wide", initial_sidebar_state="expanded")
theme.injecter()

libelles = dict(clients.lister())
if "client" not in st.session_state:
    _initialiser(next(iter(libelles)))

# Navigation latérale discrète : elle contient les choix de démo, pas le contenu principal.
with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">n.</span><div><strong>noria</strong><small>La banque, en clair.</small></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Client de démonstration</div>', unsafe_allow_html=True)
    selection = st.selectbox("Client", list(libelles), index=list(libelles).index(st.session_state.client), format_func=libelles.get, label_visibility="collapsed")
    if selection != st.session_state.client:
        _initialiser(selection)
    if st.button("Nouvelle conversation", use_container_width=True):
        _initialiser(st.session_state.client)
    st.divider()
    st.markdown('<div class="section-label">Scénarios rapides</div>', unsafe_allow_html=True)
    for index, (label, message) in enumerate(MESSAGES_DEMO.get(st.session_state.client, [])):
        if message == "oui":
            continue  # L'accord se donne uniquement sur le récapitulatif actif.
        if st.button(label, key=f"scenario-{st.session_state.client}-{index}", use_container_width=True):
            _envoyer(message)
    st.divider()
    st.toggle("Mots simples", key="mots_simples", help="Adapte la formulation pour les personnes peu à l'aise en ligne.")
    moteur, detail_moteur = _statut_moteur()
    with st.expander("État du moteur"):
        st.caption(detail_moteur)
        st.caption(_statut_comprehension())
    if not llm.actif():
        st.caption("LLM : désactivé — réponses par gabarits")

client_id = st.session_state.client
profil = st.session_state.etat.profil_simule or clients.profil(client_id)
reponse = st.session_state.derniere

st.markdown('<div class="topbar"><span>VOTRE ESPACE CONSEIL</span><span>La Banque Postale × CGI <i> / </i> Démonstration</span></div>', unsafe_allow_html=True)

left, right = st.columns([2.25, 1], gap="large")
with left:
    st.markdown('<div class="conversation-title">Conversation <span>Privée · session de démonstration</span></div>', unsafe_allow_html=True)
    if not st.session_state.messages:
        st.markdown(f'<div class="welcome"><span class="eyebrow">UN PEU PLUS DE CLARTÉ</span><h1>Bonjour {escape(profil.get("prenom", ""))}.<br>Parlons de vos projets.</h1><p>Un achat à préparer, une question sur votre compte ?<br>On avance ensemble, une étape à la fois.</p></div>', unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="assistant" if message["role"] == "assistant" else "user"):
            st.markdown(message["content"])
    components.chiffres(reponse)
    if not st.session_state.messages:
        suggestions = [MESSAGES_DEMO[client_id][0], ("Un projet immobilier", "Je veux acheter un appartement"), ("Une question d’épargne", "Je voudrais mettre de côté")]
        suggestion_cols = st.columns(3)
        for index, (col, (titre, texte)) in enumerate(zip(suggestion_cols, suggestions)):
            with col:
                if st.button(titre + "  ↗", key=f"suggestion-{index}", use_container_width=True):
                    _envoyer(texte)
                    st.rerun()
    elif reponse and reponse.question:
        exemples = {
            "prix_bien": "250000, apport 25000", "apport": "25000",
            "horizon_mois": "Dans 2 ans", "montant_mensuel": "50 euros",
            "montant": "12000", "duree_mois": "48 mois",
        }
        exemple = exemples.get(reponse.question)
        if exemple and st.button(f"Exemple de démo : {exemple}", key="suite-demo"):
            _envoyer(exemple)
            st.rerun()
    question = st.chat_input("Écrivez votre demande…")
    if question:
        _envoyer(question)
        st.rerun()

with right:
    with st.container(border=True, key="profile"):
        components.profil(profil)
    if reponse and reponse.conseil:
        components.carte("Vos pistes", lambda: components.recommandations(reponse))
    if reponse:
        components.carte("Comprendre cette réponse", lambda: components.explication(reponse, classifieur), expanded=False)
        components.carte("Ressources utilisées", lambda: components.frugalite(reponse, st.session_state.reponses, resumer), expanded=False)
    else:
        st.markdown('<div class="promise"><span>01</span><div><strong>À votre mesure</strong><p>Votre situation guide chaque réponse.</p></div></div><div class="promise"><span>02</span><div><strong>Des choix expliqués</strong><p>Les raisons, les limites et les sources.</p></div></div><div class="promise"><span>03</span><div><strong>Le calcul juste nécessaire</strong><p>Une cascade qui privilégie la simplicité.</p></div></div>', unsafe_allow_html=True)

st.caption("Vous échangez avec un assistant automatique. Données fictives · Aucune opération bancaire réelle.")
