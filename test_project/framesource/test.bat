set output=..\rst\
set framedir=..\framesource\

for /R %framedir% %%f in (*.htm *.html) do pandoc --lua-filter=not-in-format.lua -o %output%%%~nf.rst %%f --wrap=none
