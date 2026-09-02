#!/usr/bin/env bash
# Build the talk decks (slides/talk_50min.pdf, slides/talk_20min.pdf).
#
# Same toolchain as the report PDF (build/make_report_pdf.sh): TinyTeX
# lualatex, TeX Gyre Heros with DejaVu Sans as the per-glyph fallback so
# the ʻokina renders. DejaVu Sans is installed into TEXMFHOME from
# matplotlib's bundled fonts on first run (mktexlsr is required or
# kpathsea never sees the new files). Figures come straight from
# report/figures/ — rebuild those first if the report changed.
set -euo pipefail
cd "$(dirname "$0")/../slides"

export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
command -v lualatex >/dev/null || { echo "lualatex not found (TinyTeX)"; exit 1; }

if ! kpsewhich DejaVuSans.ttf >/dev/null; then
    TH="$(kpsewhich -var-value TEXMFHOME)"
    SRC="$(python3 -c 'import matplotlib, os; print(os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf"))')"
    mkdir -p "$TH/fonts/truetype/dejavu"
    cp "$SRC"/DejaVuSans.ttf "$SRC"/DejaVuSans-Bold.ttf "$TH/fonts/truetype/dejavu/"
    mktexlsr >/dev/null
    luaotfload-tool --update --force >/dev/null
fi

for deck in talk_50min talk_20min talk_weer; do
    # twice: \inserttotalframenumber needs a second pass
    lualatex -interaction=nonstopmode "$deck.tex" >/dev/null
    lualatex -interaction=nonstopmode "$deck.tex" >/dev/null
    echo "wrote slides/$deck.pdf"
done
rm -f ./*.aux ./*.log ./*.nav ./*.out ./*.snm ./*.toc
