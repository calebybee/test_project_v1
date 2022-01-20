-- List to loop through for various RST admonitions we want to parse as rst-specific, instead of default pandoc containers
admonitions = {"attention", "caution", "danger", "error", "hint", "important", "note", "tip", "warning", "admonition"}

function Div (div)
    for i,admonition in ipairs(admonitions) do
        if div.classes:includes(admonition) then
            div.classes:filter(function (x) return x ~= admonition end)
            div.content:remove(2)
            div.content:remove(1)
            return {
                div
            }
        end
    end
end