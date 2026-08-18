-- Line-break opportunities for the PDF build (make_report_pdf.sh).
-- Two overflow sources in the source markdown cannot break by default in
-- LaTeX: file paths in inline code (\texttt boxes) and long slash-joined
-- tokens in plain text (docs/SOLVER_NOTES.md, x1.00/x1.05/x1.10). Insert
-- \allowbreak after / and _ in both. Only path-like code strings are
-- touched; anything with LaTeX-special characters is left to pandoc.

local function breakable_tt(s)
  -- safe set only: letters, digits, _ / . - =
  if not s:match("^[%w_%./%-=]+$") then return nil end
  local out = s:gsub("_", "\\_\\allowbreak "):gsub("/", "/\\allowbreak ")
  return "\\texttt{" .. out .. "}"
end

function Code(el)
  if FORMAT ~= "latex" then return nil end
  if el.text:find("[/_]") then
    local tex = breakable_tt(el.text)
    if tex then return pandoc.RawInline("latex", tex) end
  end
end

function Meta(m)
  if FORMAT ~= "latex" then return nil end
  -- metadata is not filtered by default; the abstract (YAML note:) carries
  -- docs/... paths that need the same break opportunities
  if m.abstract then
    m.abstract = m.abstract:walk({ Str = Str, Code = Code })
  end
  -- "Name, *Affiliation*" author entries overflow the centered title block;
  -- set the affiliation on its own line
  if m.author then
    for _, a in ipairs(m.author) do
      for i = #a, 2, -1 do
        if a[i].t == "Emph" and a[i - 1].t == "Space" then
          a[i - 1] = pandoc.LineBreak()
          if i >= 3 and a[i - 2].t == "Str" then
            a[i - 2].text = a[i - 2].text:gsub(",$", "")
          end
          break
        end
      end
    end
  end
  return m
end

function Str(el)
  if FORMAT ~= "latex" then return nil end
  -- long plain tokens containing a slash: docs/HARD_CELLS.md, 0-15/15-20/...
  -- (pieces re-enter the writer as Str, so LaTeX escaping still applies)
  if #el.text >= 16 and el.text:find("/") then
    local parts = {}
    for piece, slash in el.text:gmatch("([^/]*)(/?)") do
      if piece ~= "" then table.insert(parts, pandoc.Str(piece)) end
      if slash == "/" then
        table.insert(parts, pandoc.Str("/"))
        table.insert(parts, pandoc.RawInline("latex", "\\allowbreak "))
      end
    end
    if #parts > 1 then return parts end
  end
end
