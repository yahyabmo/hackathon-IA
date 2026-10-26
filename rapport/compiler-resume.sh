#!/bin/sh
# Compile la version résumée (main-resume.tex -> main-resume.pdf).
# -halt-on-error : jamais d'attente interactive ; une erreur remonte tout de suite.
# Deux passes suffisent : pas de table des matières, seulement les liens.
set -e
cd "$(dirname "$0")"
command -v pdflatex >/dev/null || {
  echo "pdflatex absent. Installer :"
  echo "  sudo apt install texlive-latex-recommended texlive-latex-extra \\"
  echo "                   texlive-lang-french texlive-pictures texlive-fonts-recommended"
  exit 1
}
for i in 1 2; do
  if ! pdflatex -interaction=nonstopmode -halt-on-error main-resume.tex >/dev/null 2>&1
  then
    echo "main-resume : échec à la passe $i"
    grep -A5 '^!' main-resume.log | head -30
    exit 1
  fi
done
[ -f main-resume.pdf ] || { echo "main-resume : aucun PDF produit"; exit 1; }
rm -f main-resume.aux main-resume.log main-resume.out
echo "main-resume.pdf écrit — $(du -h main-resume.pdf | cut -f1)"
