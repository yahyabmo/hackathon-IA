"""Démo de secours : rejoue le script de démonstration et en produit un document LaTeX.

Si la démo en direct échoue devant le jury, ce document montre, scène par
scène, ce que l'assistant répond, pourquoi (intention, règles, produits proposés
et écartés) et ce que ça coûte (étapes, appels au LLM). Les textes et les
mesures sont ceux du vrai pipeline, au moment de la génération.

Usage, depuis la racine du dépôt :
    python -m eval.demo_secours                    # écrit rapport/demo-secours.tex
    (cd rapport && pdflatex demo-secours.tex)      # puis compile le PDF
"""

from __future__ import annotations

import platform
from datetime import datetime
from pathlib import Path

from src import llm
from src.assistant import reply
from src.comprendre import classifieur
from src.conseiller import clients
from src.converser.formuler import nom_produit
from src.contrats import EtatConversation, Reponse
from src.mesure import resumer

SORTIE = Path(__file__).resolve().parents[1] / "rapport" / "demo-secours.tex"

SCENES: list[tuple[str, str, list[str], str]] = [
    ("Le test de l'école : l'aiguilleur change de niveau à chaque message", "C01",
     ["J'ai perdu ma carte et je veux faire un virement.", "oui", "c'est pour mon papa",
      "Je peux retirer de mon PEL avant 4 ans ?", "100000000", "mais ma carte ?"],
     "Deux demandes (la carte d'abord), une réponse libre (niveau 1), une question ouverte (niveau 2, "
     "puis reprise), un montant invraisemblable, un renvoi au contexte."),
    ("Sans mot-clé : le classifieur comprend", "C01",
     ["Ma carte ne marche plus au distributeur"],
     "Aucun mot-clé ne conclut : e5-small reconnaît la famille, entraîné sans traduction."),
    ("L'appartement : questionner, calculer, expliquer", "C07",
     ["Je veux acheter un appartement", "Autour de 250 000, et je peux mettre les 25 000",
      "Et avec un bien à 200 000 ?", "pourquoi ?"],
     "Les revenus ne sont pas redemandés ; projet non retenu, chiffré et sourcé, recalculé ; "
     "« pourquoi ? » : le niveau 2 explique le conseil depuis la simulation."),
    ("Même phrase, deux clients : Sophie", "C03",
     ["Je voudrais mettre de côté pour mes enfants.", "Dans 10 ans, 100 euros par mois"],
     "Pour ses enfants : Livret A, Livret Jeune pour l'aîné ; LDDS et LEP écartés."),
    ("Même phrase, deux clients : Lucas", "C08",
     ["Je voudrais mettre de côté", "Dans 10 ans, 100 euros par mois"],
     "Pour lui, 20 ans : le Livret Jeune passe en premier."),
    ("Les frais de Marc : expliquer, inclure", "C02",
     ["Pourquoi j'ai payé 8 € de frais ce mois-ci ?"],
     "Sans accès au compte : la cause fréquente, le plafond légal, l'offre clientèle fragile."),
    ("Julie, mécontente : passer la main", "C06",
     ["Votre appli ne marche jamais !"],
     "Pas de justification : excuses, puis le chemin vers un conseiller et la réclamation."),
    ("Paul, 68 ans : pas à pas, en mots simples", "C04",
     ["Je dois envoyer 500 € à mon fils."],
     "Mots simples automatiques ; le chatbot guide vers l'espace bancaire sécurisé."),
    ("Le jargon, même mal écrit", "C08",
     ["C'est quoi le TEAG ?"],
     "Fiche du glossaire retrouvée malgré la faute de frappe, sans LLM."),
]

_ECHAPPEMENTS = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$", "&": r"\&", "#": r"\#",
    "^": r"\^{}", "_": r"\_", "%": r"\%", "~": r"\textasciitilde{}", "€": r"\texteuro{}",
    "\u202f": r"\,", "\u00a0": "~", "•": r"\textbullet{}", "≤": r"$\leq$", "≥": r"$\geq$",
    "→": r"$\rightarrow$", "…": r"\dots{}", "’": "'",
}


def tex(texte: str) -> str:
    """Échappe un texte pour LaTeX ; les paragraphes deviennent des \\par."""

    sortie = "".join(_ECHAPPEMENTS.get(c, c) for c in texte)
    return sortie.replace("\n\n", r"\par ").replace("\n", " ")


def _pourquoi(reponse: Reponse) -> list[str]:
    lignes = [f"\\textbf{{Niveau {reponse.niveau}}} : {tex(reponse.raison_niveau)}"]
    c = reponse.comprehension
    if c.comprise:
        lignes.append(f"Intention \\texttt{{{tex(c.intention)}}}, comprise par {tex(c.niveau)}")
    if reponse.question:
        lignes.append(f"Information demandée : \\texttt{{{tex(reponse.question)}}}")
    if reponse.conseil:
        lignes += [f"Proposé : {tex(nom_produit(p.produit_id))} --- {tex(' '.join(p.raisons))}"
                   for p in reponse.conseil.propositions]
        lignes += [f"Écarté : {tex(nom_produit(e.produit_id))} --- {tex(e.raison)}"
                   + (f" (\\texttt{{{tex(e.regle)}}})" if e.regle else "") for e in reponse.conseil.ecartees]
        lignes += [f"Alerte : {tex(a)}" for a in reponse.conseil.alertes]
        lignes += [f"Hypothèse : {tex(h)}" for h in reponse.conseil.faits.get("hypotheses", [])]
    lignes += [f"Source [{n}] : {tex(s['titre'])} ({tex(s['source'])}), score {s['score']:.3f}".replace(".", ",", 1)
               for n, s in enumerate(reponse.sources, start=1)]
    return lignes


def _ms(valeur: float, decimales: int = 1) -> str:
    return f"{valeur:.{decimales}f}".replace(".", ",") + "~ms"


def _frugalite(reponse: Reponse) -> str:
    etapes = ", ".join(f"{tex(e.nom)} {_ms(e.latence_ms)}" for e in reponse.trace)
    return f"{etapes} --- appels au LLM : {reponse.appels_llm}"


def generer() -> str:
    classifieur.prechauffer()  # comme l'interface au démarrage : le chargement n'est pas un tour
    morceaux, toutes = [], []
    for titre, client, messages, idee in SCENES:
        profil = clients.profil(client)
        etat = EtatConversation()
        morceaux.append(f"\\section{{{tex(titre)}}}\n\\textit{{{tex(profil['prenom'])}, "
                        f"{profil['age']} ans, {tex(profil['metier'])} ({client}).}} {tex(idee)}\n")
        for message in messages:
            reponse, etat = reply(message, client, etat)
            toutes.append(reponse)
            pourquoi = "".join(f"\\item {l}\n" for l in _pourquoi(reponse))
            morceaux.append(
                f"\\begin{{client}}{tex(message)}\\end{{client}}\n"
                f"\\begin{{assistant}}{tex(reponse.texte)}\\end{{assistant}}\n"
                + (f"\\begin{{pourquoi}}\n\\begin{{itemize}}\n{pourquoi}\\end{{itemize}}\n\\end{{pourquoi}}\n" if pourquoi else "")
                + f"\\frugal{{{_frugalite(reponse)}}}\n"
            )
    sans_llm = sum(1 for r in toutes if r.appels_llm == 0)
    total_ms = sum(resumer(r.trace)["latence_ms"] for r in toutes)
    mode = (f"aiguilleur, niveau 1 : \\texttt{{{tex(llm.MODELE_NIVEAU1)}}}, niveau 2 : \\texttt{{{tex(llm.MODELE_NIVEAU2)}}}"
            if llm.actif() else "aiguilleur sans LLM (niveau 0, et RAG en extrait)")
    par_niveau = ", ".join(f"niveau {n} : {sum(1 for r in toutes if r.niveau == n)}" for n in (0, 1, 2))
    bilan = (f"\\section*{{Bilan}}\n{len(toutes)} tours de conversation, dont \\textbf{{{sans_llm} sans aucun "
             f"appel au LLM}} ; {_ms(total_ms)} de calcul au total, soit {_ms(total_ms / len(toutes), 2)} par "
             f"tour en moyenne ; {sum(r.appels_llm for r in toutes)} appel(s) au LLM ; "
             f"{sum(1 for r in toutes if r.escalade)} escalade ; {par_niveau}. Mode : {mode}.\n")
    entete = (f"Généré le {datetime.now():%d/%m/%Y à %H h %M} sur {tex(platform.node())} "
              f"({tex(platform.processor() or platform.machine())}), mode : {mode}.")
    return GABARIT.replace("%ENTETE%", entete).replace("%CORPS%", bilan + "\n".join(morceaux))


GABARIT = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage{textcomp}\usepackage[french]{babel}
\usepackage{lmodern}\usepackage[top=2cm,bottom=2cm,left=2.2cm,right=2.1cm]{geometry}
\usepackage{microtype}\usepackage{xcolor}\usepackage{enumitem}\usepackage{titlesec}
\usepackage[most]{tcolorbox}\usepackage{hyperref}
\definecolor{mainblue}{RGB}{28,74,102}\definecolor{darkgray}{RGB}{62,62,66}
\definecolor{ent}{RGB}{221,236,247}\definecolor{ext}{RGB}{250,233,207}\definecolor{mod}{RGB}{238,238,242}
\titleformat{\section}{\large\bfseries\color{mainblue}}{\thesection}{0.6em}{}
\setlist[itemize]{leftmargin=1.2em,itemsep=0.05em,topsep=0.1em}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.3em}
\newtcolorbox{client}{colback=ext!60,colframe=ext!60!black,boxrule=0.4pt,arc=1.5mm,left=2mm,right=2mm,
  top=0.8mm,bottom=0.8mm,width=0.78\textwidth,enlarge left by=0.22\textwidth,
  fontupper=\small,title={Client},fonttitle=\scriptsize\bfseries,coltitle=darkgray,colbacktitle=ext!60}
\newtcolorbox{assistant}{colback=ent,colframe=mainblue!60,boxrule=0.4pt,arc=1.5mm,left=2mm,right=2mm,
  top=0.8mm,bottom=0.8mm,width=0.85\textwidth,fontupper=\small,
  title={Assistant},fonttitle=\scriptsize\bfseries,coltitle=white,colbacktitle=mainblue!80}
\newtcolorbox{pourquoi}{colback=mod,colframe=mod,boxrule=0pt,arc=1mm,left=2mm,right=2mm,top=0.5mm,
  bottom=0.5mm,fontupper=\scriptsize,title={Pourquoi},fonttitle=\scriptsize\bfseries,coltitle=darkgray,
  colbacktitle=mod}
\newcommand{\frugal}[1]{{\scriptsize\color{darkgray}\textbf{Frugalité} : #1}\par\medskip}
\begin{document}
{\LARGE\bfseries\color{mainblue} Démo de secours\par}
{\large Assistant bancaire frugal --- le script de la démonstration, rejoué par le vrai pipeline\par}
{\small\color{darkgray} %ENTETE%\par}
\medskip
%CORPS%
\end{document}
"""


if __name__ == "__main__":
    SORTIE.write_text(generer(), encoding="utf-8")
    print(f"écrit : {SORTIE}")
