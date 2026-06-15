-- Wrap a Div with class "dossier" in \begin{dossier}...\end{dossier} for LaTeX/PDF output,
-- so the Courier-Prime `dossier` environment (assets/dossier-pdf.tex) actually applies.
-- For non-LaTeX writers (EPUB/HTML) the Div is left untouched (CSS .dossier handles it).
function Div(el)
  if el.classes:includes("dossier") and FORMAT:match("latex") then
    local open  = pandoc.RawBlock("latex", "\\begin{dossier}")
    local close = pandoc.RawBlock("latex", "\\end{dossier}")
    local blocks = el.content
    table.insert(blocks, 1, open)
    table.insert(blocks, close)
    return blocks
  end
  return el
end
