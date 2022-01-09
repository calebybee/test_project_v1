@echo

xcopy *html.rst *.rst

pause 

cls


goto :eof



for /r  %%i in (*.html.rst) do rename *.rst

for /r  %%i in (.) do @ren "%%i\*.html.rst" *O&ren "%%i\*.rst" *f

for /r  %%i in (*.html.rst) do @ren "%%i\*.rst" 

for /r (.) %F in (*.html.rst) do @for %G in ("%~nF") do @ren "%F" "%~nG"

:: for /r  %%i in (*.html.rst) do ren %%i *.rst

for %%F in (*.html.rst) do (
  set "name=%%F"
  ren "!name!" "!name:.rst!"
)
