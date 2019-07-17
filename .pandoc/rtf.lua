-- These are common functions used by all of the Lua writers

function read_address()
    local fh = assert(io.open("../../address.txt"))
    local txt = fh:read("*all")
    fh:close()
    return txt
end

function flatten_variables(metadata, variables)
    local rv = {}

    -- merge metadata with variables
    for k, v in pairs(metadata) do
        rv[k] = v
    end

    -- flatten the nested tables in variables
    for k, v in pairs(variables) do
        if type(v) == 'table' then
            for innerK, innerV in pairs(v) do
                rv[innerK] = innerV
            end
        else
            rv[k] = v
        end
    end

    return rv
end

-- Character escaping
local function escape(s, in_attribute)
  return s:gsub("[\\{}\t]",
    function(x)
      if x == '\\' then
        return '\\\\'
      elseif x == '{' then
        return '\\\'7b'
      elseif x == '}' then
        return '\\\'7d'
      elseif x == "\t" then
        return "\\tab"
      else
        return x
      end
    end)
end

-- Soft break is for breaks within the source document itself
function SoftBreak()
    return "\n"
end

-- Blocksep is used to separate block elements.
function Blocksep()
  return "\n"
end

-- This function is called once for the whole document. Parameters:
-- body is a string, metadata is a table, variables is a table.
-- One could use some kind of templating
-- system here; this just gives you a simple standalone HTML file.
function Doc(body, metadata, variables)
    local buffer = {}
    local function add(s)
      table.insert(buffer, s)
    end

    variables = flatten_variables(metadata, variables)

    assert(variables['author'], "no author name provided")
    assert(variables['title'], "no title provided")
    assert(variables['lastname'], "no last name provided")

    -- rtf header
    add("{\\rtf1\\ansi\\deff0")
    add("{\\fonttbl{\\f0\\fnil Courier New;}}")

    -- add('{\\sl240\\slmult1}')
    
    -- info block
    add('{\\info')
    add("{\\title " .. variables['title'] .. "}")
    add("{\\author " .. variables['author'] .. "}")
    add("}")

    -- page headers
    if variables['running-title'] then
        add("{\\header\\pard\\qr\\plain\\f0 " .. variables['lastname'] .. " / " .. variables['running-title']:upper() .. " / \\chpgn\\par\\titlepg}")
    else
        io.stderr:write(string.format("WARNING: No running-title defined\n"))
        add("{\\header\\pard\\qr\\plain\\f0 " .. variables['lastname'] .. " / \\chpgn\\par}")
    end
    add("\\margl1440\\margr1440\\margt1440\\margb1440")

    -- wordcount
    if variables['wordcount'] then
        add("{\\pard\\f0\\fs24\\qr " .. variables['wordcount'] .. "  words \\line Disposable Copy \\par}")
    else
        io.stderr:write(string.format("WARNING: No wordcount defined\n"))
    end

    -- address
    add(HeaderBlock(variables['author'] .. "\n" .. read_address()))

    -- title and author
    add(HeaderBlock("\\qc\\li0\\fi0\\sb4320\\sa1440 " .. metadata['title']:upper() .. "\\line\nby " .. variables['author']))

    
    add(body)

    add(Para("\\fi0\\qc ###"))
    add("}")

    return table.concat(buffer, "\n")

end

-- The functions that follow render corresponding pandoc elements.
-- s is always a string, attr is always a table of attributes, and
-- items is always an array of strings (the items in a list).
-- Comments indicate the types of other variables.

function Str(s)
  return escape(s)
end

function Space()
  return " "
end

function LineBreak()
  return "\\line"
end

function Emph(s)
  return "{\\i " .. s .. "}"
end

function Strong(s)
  return "{\\b " .. s .. "}"
end

function Subscript(s)
  return "{\\sub " .. s .. "}"
end

function Superscript(s)
  return "{\\super " .. s .. "}"
end

function SmallCaps(s)
  return '{\\scaps ' .. s .. '}'
end

function Strikeout(s)
  return '{\\strike ' .. s .. '}'
end

-- TODO: unimplemented
-- function Link(s, src, tit)
--   return "<a href='" .. escape(src,true) .. "' title='" ..
--          escape(tit,true) .. "'>" .. s .. "</a>"
-- end

-- TODO: unimplemented
-- function Image(s, src, tit)
--  return "<img src='" .. escape(src,true) .. "' title='" ..
--          escape(tit,true) .. "'/>"
-- end

-- TODO: unimplemented
-- function Code(s, attr)
--   return "<code" .. attributes(attr) .. ">" .. escape(s) .. "</code>"
-- end

-- TODO: unimplemented
-- function InlineMath(s)
--   return "\\(" .. escape(s) .. "\\)"
-- end

-- TODO: unimplemented
-- function DisplayMath(s)
--   return "\\[" .. escape(s) .. "\\]"
-- end

function Note(s)
    return "{\\super\\chftn}{\\footnote\\pard\\plain\\chftn " .. s .. " \\par}"
end

function Span(s, attr)
    return Plain(s)
end

function Plain(s)
  return s
end

function Para(s)
  return "{\\pard\\f0\\fs24\\fi720\\sa60\\sl600\\li0 " .. s .. " \\par}"
end

-- lev is an integer, the header level. s is a string, attr the attributes
-- note that we INVERT the normal section hierarchy here for convenience
-- level 1 = chapter
-- level 2 = part
local chapterNumber = 0
local partNumber = 0
function Header(lev, s, attr)
    prologueTag  = "Prologue: "
    epilogueTag = "Epilogue: "

    if lev == 1 then -- chapters
        if (string.sub(s, 1, string.len(prologueTag)) == prologueTag) then
            s = s.sub(s, string.len(prologueTag) + 1)
            return Para("\\fi0\\li0\\pagebb\\sb4320\\sa1440\\qc PROLOGUE \\line\n" .. s:upper())
        elseif (string.sub(s, 1, string.len(epilogueTag)) == epilogueTag) then
            s = s.sub(s, string.len(epilogueTag) + 1)
            return Para("\\fi0\\li0\\pagebb\\sb4320\\sa1440\\qc EPILOGUE \\line\n" .. s:upper())
        else
            chapterNumber = chapterNumber + 1
            return Para("\\fi0\\li0\\pagebb\\sb4320\\sa1440\\qc CHAPTER " .. chapterNumber .. "\\line\n" .. s:upper())
        end
    elseif lev == 2 then -- part
        partNumber = partNumber + 1
        return Para("\\fi0\\li0\\pagebb\\pageba\\sb4320\\qc PART " .. partNumber .. "\\line\n" .. s:upper())
    else
        io.stderr:write("UNSUPPORTED header level " .. lev)
    end
end

function DoubleQuoted(s)
  return "\"" .. s .. "\""
end

function SingleQuoted(s)
  return "'" .. s .. "'"
end

function BlockQuote(s)
    return Para("\\li1440\\ri1440\\fi480 " .. s)
end

-- we use horizontal rules for scene breaks, and render them as such
function HorizontalRule()
    return Para("\\qc #")
end

-- The header block is single-spaced
function HeaderBlock(s, attr)
  return Para("\\sl240\\slmult1\\fi0 " .. s:gsub("\n", "\\line\n"):gsub(" ", "\\~"))
  
end

function CodeBlock(s, attr)
    return Para("\\fi0 " .. s:gsub("\n", "\\line\n"):gsub(" ", "\\~"))
end

-- TODO: unimplemented
-- function BulletList(items)
--   local buffer = {}
--   for _, item in pairs(items) do
--     table.insert(buffer, "<li>" .. item .. "</li>")
--   end
--   return "<ul>\n" .. table.concat(buffer, "\n") .. "\n</ul>"
-- end

-- TODO: unimplemented
-- function OrderedList(items)
--   local buffer = {}
--   for _, item in pairs(items) do
--     table.insert(buffer, "<li>" .. item .. "</li>")
--   end
--   return "<ol>\n" .. table.concat(buffer, "\n") .. "\n</ol>"
-- end

-- TODO: unimplemented
-- Revisit association list STackValue instance.
-- function DefinitionList(items)
--   local buffer = {}
--   for _,item in pairs(items) do
--     for k, v in pairs(item) do
--       table.insert(buffer,"<dt>" .. k .. "</dt>\n<dd>" ..
--                         table.concat(v,"</dd>\n<dd>") .. "</dd>")
--     end
--   end
--   return "<dl>\n" .. table.concat(buffer, "\n") .. "\n</dl>"
-- end

-- TODO: unimplemented
-- Caption is a string, aligns is an array of strings,
-- widths is an array of floats, headers is an array of
-- strings, rows is an array of arrays of strings.
-- function Table(caption, aligns, widths, headers, rows)
-- end

function Div(s, attr)
  return Para(s)
end

-- Block comments (don't render)
function RawBlock(s)
    return ""
end

-- Inline comments (don't render)
function RawInline(s)
    return ""
end

-- The following code will produce runtime warnings when you haven't defined
-- all of the functions you need for the custom writer, so it's useful
-- to include when you're working on a writer.
local meta = {}
meta.__index =
  function(_, key)
    io.stderr:write(string.format("WARNING: Undefined function '%s'\n",key))
    return function() return "" end
  end
setmetatable(_G, meta)

function main()
    Doc("test", {}, {})
end
