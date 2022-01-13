function Div(element)
    if element.classes:includes('not-in-format') and
    element.classes:find_if(function (x) return FORMAT:match(x) end) then
        return {}
    end
end