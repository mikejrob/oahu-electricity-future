#!/usr/bin/env bash
# Build report/DRAFT_v7_full.pdf from the markdown source.
#
# Requirements (all present on the koa login nodes):
#   - pandoc >= 3.1.10          (module load tools/Pandoc/3.6.2)
#   - TinyTeX with lualatex     (~/.TinyTeX/bin/x86_64-linux)
#   - DejaVu Serif visible to luaotfload — the per-glyph fallback for the
#     code points TeX Gyre Pagella lacks (the ʻokina above all, plus
#     sub/superscript digits, Greek, and arrows). The script installs it
#     into TEXMFHOME from matplotlib's bundled fonts on first run; the
#     mktexlsr step is required or kpathsea never sees the new files.
#
# Design notes:
#   - implicit_figures is disabled and tex_math_dollars is disabled: the
#     italic caption paragraphs in the source are the sole figure captions
#     (matching the GitHub rendering), and dollar amounts in the text can
#     never be misread as TeX math.
#   - The YAML `note:` field becomes the PDF abstract; the markdown source
#     is not modified.
set -euo pipefail
cd "$(dirname "$0")/.."

command -v pandoc >/dev/null 2>&1 || module load tools/Pandoc/3.6.2
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
command -v lualatex >/dev/null || { echo "lualatex not found (TinyTeX)"; exit 1; }

if ! kpsewhich DejaVuSerif.ttf >/dev/null; then
    TH="$(kpsewhich -var-value TEXMFHOME)"
    SRC="$(python3 -c 'import matplotlib, os; print(os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf"))')"
    mkdir -p "$TH/fonts/truetype/dejavu"
    cp "$SRC"/DejaVuSerif.ttf "$SRC"/DejaVuSerif-Bold.ttf "$TH/fonts/truetype/dejavu/"
    mktexlsr >/dev/null
    luaotfload-tool --update --force >/dev/null
fi

tmp=$(mktemp --suffix=.md)
trap 'rm -f "$tmp"' EXIT
sed '0,/^note:/s//abstract:/' report/DRAFT_v7_full.md > "$tmp"

pandoc "$tmp" \
    -f markdown-implicit_figures-tex_math_dollars \
    --resource-path=report \
    --pdf-engine=lualatex \
    --lua-filter=build/pdf_center_images.lua \
    --lua-filter=build/pdf_breaks.lua \
    -H build/report_pdf_header.tex \
    --toc --toc-depth=3 \
    -V mainfont=texgyrepagella \
    -V mainfontoptions="Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,ItalicFont=*-italic,BoldItalicFont=*-bolditalic" \
    -V mainfontfallback="DejaVu Serif:mode=node;" \
    -V geometry:margin=1.1in \
    -V fontsize=11pt \
    -V colorlinks=true \
    -o report/DRAFT_v7_full.pdf

echo "wrote report/DRAFT_v7_full.pdf"
