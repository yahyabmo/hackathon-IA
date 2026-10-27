"""Composants d'affichage : aucun composant ne contient de logique métier."""

from __future__ import annotations

from typing import Any, Callable
from html import escape

import streamlit as st

from ..conseiller import clients, catalogue
from ..converser.formuler import nom_produit


def carte(titre: str, contenu: Callable[[], None], *, expanded: bool = True) -> None:
    with st.expander(titre, expanded=expanded):
        contenu()


def profil(profil_client: dict[str, Any]) -> None:
    prenom = profil_client.get("prenom", "Client")
    initiale = prenom[:1].upper()
    st.markdown(
        f'<div style="display:flex;gap:.75rem;align-items:center;margin-bottom:1rem">'
        f'<div class="avatar">{initiale}</div><div><div class="mini-label">Profil de démonstration</div>'
        f'<div class="profile-name">{prenom}</div><div class="profile-meta">{profil_client.get("metier", "")}'
        f' · {profil_client.get("age", "?")} ans</div></div></div>', unsafe_allow_html=True)
    champs = (("revenus_nets", "Revenus / mois"), ("epargne", "Épargne"),
              ("mensualites_credits", "Crédits / mois"), ("solde", "Solde courant"))
    cols = st.columns(2)
    for index, (champ, label) in enumerate(champs):
        valeur = profil_client.get(champ)
        affichage = "Inconnu" if valeur is None else f"{valeur:,.2f} €".replace(",", " ").replace(".", ",")
        simule = clients.est_simule(profil_client, champ)
        with cols[index % 2]:
            st.markdown(f'<div class="stat-caption">{label}</div><div class="stat-value">{affichage}</div>'
                        f'{"<div class=\"stat-caption\">Donnée simulée</div>" if simule else ""}',
                        unsafe_allow_html=True)
    cartes = profil_client.get("cartes", [])
    if cartes:
        st.markdown('<div class="section-label" style="margin-top:1rem">État des moyens de paiement</div>', unsafe_allow_html=True)
        for carte_item in cartes:
            statut = carte_item.get("statut", "inconnu")
            classe = "tag-alert" if statut == "opposition" else "tag"
            st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:.35rem 0;'
                        f'border-bottom:1px solid #edf1ee;font-size:.78rem"><span>{carte_item.get("id", "Carte")}</span>'
                        f'<span class="tag {classe}">{statut}</span></div>', unsafe_allow_html=True)


def recommandations(reponse: Any) -> None:
    conseil = reponse.conseil if reponse else None
    if not conseil:
        st.markdown('<div class="card-note">Les recommandations apparaîtront après votre première demande.</div>', unsafe_allow_html=True)
        return
    if conseil.manque:
        st.markdown('<span class="tag tag-warm">Information nécessaire</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-note" style="margin-top:.45rem">Il manque encore : <strong>{", ".join(conseil.manque)}</strong>.</div>', unsafe_allow_html=True)
    for proposition in conseil.propositions:
        if proposition.produit_id == "rdv_conseiller":
            continue
        raison = proposition.raisons[0] if proposition.raisons else "Orientation conditionnelle."
        st.markdown(f'<div class="recommendation"><strong>{nom_produit(proposition.produit_id)}</strong>'
                    f'<p>{raison}</p></div>', unsafe_allow_html=True)
    if conseil.ecartees:
        st.markdown('<div class="section-label" style="margin-top:1rem">Écartés par les règles</div>', unsafe_allow_html=True)
        for ecart in conseil.ecartees:
            st.markdown(f'<div class="exclusion"><strong>{nom_produit(ecart.produit_id)}</strong>'
                        f'<p>{ecart.raison}</p></div>', unsafe_allow_html=True)
    if conseil.alertes:
        with st.expander(f"Limites et précautions · {len(conseil.alertes)}"):
            for alerte in conseil.alertes:
                st.write(alerte)


def chiffres(reponse: Any) -> None:
    """Affiche seulement les montants déjà calculés et validés par M3."""
    if not reponse or not reponse.conseil:
        return
    faits = reponse.conseil.faits
    if "mensualite" not in faits:
        return
    with st.container(border=True, key="estimation"):
        st.caption("VOTRE SIMULATION · INDICATIVE")
        colonnes = st.columns(3)
        for col, (label, valeur) in zip(colonnes, [
            ("À financer", f"{faits['besoin']:,.0f} €".replace(",", " ")),
            ("Mensualité", f"{faits['mensualite']:,.2f} €".replace(",", " ").replace(".", ",")),
            ("Taux d’effort", f"{faits['taux_effort'] * 100:.1f} %".replace(".", ",")),
        ]):
            col.metric(label, valeur)
        st.caption("Assurance incluse dans le calcul." if faits.get("assurance_connue") else "Hors assurance non renseignée. Cette estimation ne constitue pas un accord de prêt.")


def explication(reponse: Any, classifieur: Any) -> None:
    if not reponse:
        st.markdown('<div class="card-note">La chaîne de décision apparaîtra ici après le premier échange.</div>', unsafe_allow_html=True)
        return
    c = reponse.comprehension
    if c.comprise:
        st.markdown(f'<div class="metric-row"><span>Intention</span><span>{c.intention}</span></div>'
                    f'<div class="metric-row"><span>Étape</span><span>{c.niveau}</span></div>', unsafe_allow_html=True)
        if c.confiance:
            st.markdown(f'<div class="metric-row"><span>Confiance</span><span>{c.confiance:.2f}</span></div>', unsafe_allow_html=True)
    if reponse.question:
        st.markdown(f'<div class="action-box" style="margin-top:.7rem"><div class="action-title">Question en cours</div>'
                    f'<div class="action-copy">{reponse.question}</div></div>', unsafe_allow_html=True)
    if reponse.conseil:
        for hypothese in reponse.conseil.faits.get("hypotheses", []):
            st.markdown(f'<div class="card-note" style="margin-top:.5rem">Hypothèse · {hypothese}</div>', unsafe_allow_html=True)
        sources = reponse.conseil.faits.get("sources_produits", {})
        if sources:
            st.markdown('<div class="section-label" style="margin-top:1rem">Sources</div>', unsafe_allow_html=True)
            for product_id, source in sources.items():
                try:
                    fiche = catalogue.produit("credit_immobilier" if product_id == "credit_immobilier_30_ans" else product_id)
                    date = fiche.get("releve_le", "date non précisée")
                except KeyError:
                    date = "date non précisée"
                lien = (f'<a href="{escape(source, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(nom_produit(product_id))} ↗</a>'
                        if source.startswith("https://") else escape(source))
                st.markdown(f'<div class="source-line">{lien}<br>Relevé le {escape(date)}</div>', unsafe_allow_html=True)


def frugalite(reponse: Any, reponses: list[Any], resumer: Callable) -> None:
    if not reponse:
        st.markdown('<div class="card-note">Aucune mesure sur cette conversation.</div>', unsafe_allow_html=True)
        return
    total = resumer(reponse.trace)
    for label, value in (("Latence de ce tour", f"{total['latence_ms']:.1f} ms"),
                         ("Appels LLM", str(int(total["appels_llm"]))),
                         ("Tokens mesurés", str(int(total["tokens"]))),
                         ("Tours sans LLM", f"{sum(r.appels_llm == 0 for r in reponses)} / {len(reponses)}")):
        st.markdown(f'<div class="metric-row"><span>{label}</span><span>{value}</span></div>', unsafe_allow_html=True)
    if not total["appels_llm"]:
        st.markdown('<div class="card-note" style="margin-top:.65rem">Ce tour a été traité par la cascade locale et ses gabarits.</div>', unsafe_allow_html=True)
    for etape in reponse.trace:
        if etape.modele:
            st.caption(f"{etape.nom} · {etape.modele} · {etape.latence_ms:.1f} ms")
    st.caption("Énergie : non mesurée pour ce tour.")
