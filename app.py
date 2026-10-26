"""Interface Streamlit du prototype : conversation, profil, « pourquoi », « frugalité »."""

from __future__ import annotations

import streamlit as st

from src import llm
from src.assistant import reply
from src.conseiller import clients
from src.conseiller.catalogue import nom as nom_produit
from src.contrats import EtatConversation
from src.mesure import resumer

MESSAGES_DEMO = {
    "C01": ["J'ai perdu ma carte hier soir, je fais quoi ?", "oui"],
    "C02": ["Pourquoi j'ai payé 8 € de frais ce mois-ci ?"],
    "C03": ["Je voudrais mettre de côté pour mes enfants.", "Dans 10 ans, 100 euros par mois"],
    "C04": ["Je dois envoyer 500 € à mon fils.", "oui"],
    "C05": ["Je veux un crédit pour acheter une voiture.", "12000", "48 mois"],
    "C06": ["Votre appli ne marche jamais !"],
    "C07": ["Je veux acheter un appartement", "Autour de 250 000, et je peux mettre les 25 000"],
    "C08": ["Je voudrais mettre de côté", "Dans 2 ans", "50 euros", "C'est quoi un TAEG ?"],
}


def _nom(produit_id: str) -> str:
    try:
        return nom_produit(produit_id)
    except KeyError:
        return produit_id


def _reinitialiser(client_id: str) -> None:
    st.session_state.client = client_id
    st.session_state.etat = EtatConversation()
    st.session_state.messages = []
    st.session_state.derniere = None
    st.session_state.reponses = []


def _envoyer(texte: str) -> None:
    st.session_state.etat.mots_simples = st.session_state.get("mots_simples", False)
    st.session_state.messages.append({"role": "user", "content": texte})
    reponse, st.session_state.etat = reply(texte, st.session_state.client, st.session_state.etat)
    st.session_state.messages.append({"role": "assistant", "content": reponse.texte})
    st.session_state.derniere = reponse
    st.session_state.reponses.append(reponse)


def _frugalite_session(reponses) -> dict:
    """Totaux de la conversation : la preuve de frugalité au fil de la démo."""

    tours = len(reponses)
    sans_llm = sum(1 for r in reponses if r.appels_llm == 0)
    niveaux = {}
    for r in reponses:
        if r.comprehension.comprise:
            niveaux[r.comprehension.niveau] = niveaux.get(r.comprehension.niveau, 0) + 1
    return {
        "tours": tours,
        "sans_llm": sans_llm,
        "latence_ms": sum(resumer(r.trace)["latence_ms"] for r in reponses),
        "appels_llm": sum(r.appels_llm for r in reponses),
        "escalades": sum(1 for r in reponses if r.escalade),
        "niveaux": niveaux,
    }


st.set_page_config(page_title="Assistant bancaire frugal", page_icon="🏦", layout="wide")
st.title("Assistant bancaire frugal")
st.info("Vous échangez avec un assistant automatique. Il oriente ; un conseiller décide. "
        "Prototype : aucune opération bancaire réelle n'est exécutée.")

# ── Client : changer de client recommence la conversation ──
libelles = dict(clients.lister())
client_id = st.sidebar.selectbox("Client de démonstration", list(libelles), format_func=libelles.get)
if st.session_state.get("client") != client_id:
    _reinitialiser(client_id)
if st.sidebar.button("Nouvelle conversation"):
    _reinitialiser(client_id)

st.sidebar.toggle("Mots simples", key="mots_simples",
                  help="Automatique dès 70 ans ou pour un client peu à l'aise en ligne.")
if st.sidebar.toggle("Grand texte", key="grand_texte"):
    st.markdown("<style>[data-testid='stChatMessage'] p {font-size: 1.3rem; line-height: 1.6;}</style>",
                unsafe_allow_html=True)

st.sidebar.caption("Messages de démo")
for i, texte in enumerate(MESSAGES_DEMO.get(client_id, [])):
    if st.sidebar.button(texte, key=f"demo-{client_id}-{i}"):
        _envoyer(texte)
st.sidebar.caption("LLM : " + (f"activé ({llm.MODELE_FORMULATION})" if llm.actif() else "désactivé, gabarits"))

colonne_chat, colonne_panneaux = st.columns([3, 2])

with colonne_chat:
    question = st.chat_input("Écrivez votre demande bancaire…")
    if question:
        _envoyer(question)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

with colonne_panneaux:
    profil = clients.profil(client_id)
    with st.expander("Profil", expanded=True):
        for champ, libelle in (("age", "Âge"), ("metier", "Métier"), ("situation", "Situation"),
                               ("revenus_nets", "Revenus nets / mois"), ("epargne", "Épargne"),
                               ("mensualites_credits", "Crédits en cours / mois")):
            valeur = profil.get(champ)
            affiche = f"*{valeur}* (simulé)" if clients.est_simule(profil, champ) else f"{valeur}"
            st.markdown(f"**{libelle}** : {affiche}")

    reponse = st.session_state.derniere
    with st.expander("Pourquoi", expanded=True):
        if reponse is None:
            st.caption("Le raisonnement de la dernière réponse s'affiche ici.")
        else:
            c = reponse.comprehension
            if c.comprise:
                st.markdown(f"**Intention** : `{c.intention}` ({c.famille}) — compris par **{c.niveau}**")
            if reponse.question:
                st.markdown(f"**Information demandée** : `{reponse.question}`")
            if reponse.conseil:
                for p in reponse.conseil.propositions:
                    st.markdown(f"✅ **{_nom(p.produit_id)}** — " + " ".join(p.raisons))
                    if p.sources:
                        st.caption("Source : " + " ; ".join(dict.fromkeys(p.sources)))
                for e in reponse.conseil.ecartees:
                    st.markdown(f"❌ **{_nom(e.produit_id)}** — {e.raison}" + (f" `{e.regle}`" if e.regle else ""))
                for a in reponse.conseil.alertes:
                    st.warning(a)
            if reponse.action:
                etat_action = "exécutée" if reponse.action.resultat else "en attente de votre accord"
                st.markdown(f"**Action** : `{reponse.action.outil}` — {etat_action}")

    with st.expander("Frugalité", expanded=True):
        if reponse is not None:
            st.table([{"étape": e.nom, "modèle": e.modele or "—", "ms": round(e.latence_ms, 2),
                       "tokens": e.tokens} for e in reponse.trace])
            totaux = resumer(reponse.trace)
            st.markdown(f"**Ce tour** : {totaux['latence_ms']:.1f} ms — appels au LLM : "
                        f"**{int(totaux['appels_llm'])}** — escalade : {'oui' if reponse.escalade else 'non'}")
            session = _frugalite_session(st.session_state.reponses)
            niveaux = ", ".join(f"{n} : {k}" for n, k in session["niveaux"].items()) or "—"
            st.markdown(f"**Conversation** : {session['tours']} tours, dont **{session['sans_llm']} sans LLM** — "
                        f"{session['latence_ms']:.1f} ms au total — {session['appels_llm']} appel(s) au LLM, "
                        f"{session['escalades']} escalade(s) — compris par : {niveaux}")
