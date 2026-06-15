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

-- A black-marker redaction: `[withheld]{.redact}` → \redact{withheld} for the PDF (a solid black
-- bar, defined in assets/dossier-pdf.tex). For EPUB/HTML the span keeps class="redact" and the CSS
-- draws the bar — so nothing to do there. The hidden text stays in the source either way, so a
-- screen reader can still announce it; the eye only sees the strike.
function Span(el)
  if el.classes:includes("redact") and FORMAT:match("latex") then
    local txt = pandoc.utils.stringify(el)
    return {
      pandoc.RawInline("latex", "\\redact{"),
      pandoc.Str(txt),
      pandoc.RawInline("latex", "}"),
    }
  end
  return el
end
