-- Center standalone images in the PDF build.
-- implicit_figures is disabled (see make_report_pdf.sh), so the italic
-- caption paragraphs in the source remain the sole captions — matching the
-- GitHub rendering — and the alt text stays out of the page.
function Para(el)
  if #el.content == 1 and el.content[1].t == "Image" then
    return {
      pandoc.RawBlock("latex", "\\begin{center}"),
      pandoc.Para(el.content),
      pandoc.RawBlock("latex", "\\end{center}"),
    }
  end
end
