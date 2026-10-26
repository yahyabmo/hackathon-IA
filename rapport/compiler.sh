#!/bin/sh
# Compile le rapport (main.tex -> main.pdf).
# -halt-on-error : jamais d'attente interactive ; une erreur remonte tout de suite.
# Trois passes : table des matières, liste des figures et références croisées
# ont besoin des trois.
set -e
cd "$(dirname "$0")"
command -v pdflatex >/dev/null || {
  echo "pdflatex absent. Installer :"
  echo "  sudo apt install texlive-latex-recommended texlive-latex-extra \\"
  echo "                   texlive-lang-french texlive-pictures texlive-fonts-recommended"
  exit 1
}
for i in 1 2 3; do
  if ! pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null 2>&1
  then
    echo "main : échec à la passe $i"
    grep -A5 '^!' main.log | head -30
    exit 1
  fi
done
[ -f main.pdf ] || { echo "main : aucun PDF produit"; exit 1; }
rm -f main.aux main.log main.out main.toc main.lof main.lot chapitres/*.aux
echo "main.pdf écrit — $(du -h main.pdf | cut -f1)"
