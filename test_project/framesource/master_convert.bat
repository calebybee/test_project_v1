@echo

set bookname=Access
set output=..\rst\
set root=..\docs\
set framedir=..\framesource\

:: save as html manually. 

:: process the html with regex prior to converting to RST. 

python loop_rst_regex.py

:: We're working in the current directory and sub dirs.
:: Run pandoc on all HTML files. 


for /R %framedir% %%f in (*.htm *.html) do pandoc --lua-filter=admonitions.lua -o %output%%%~nf.rst %%f --wrap=none

:: remove unwanted files
del /s /q *.css
:: del /s /q *.html // don't need the html when this script all works.


cd %output%

python postprocess_rst_regex.py 

cd %framedir%




GOTO :EOF

Done: save as HTML
Done: then remove all CSS
Done: then run regex on HTML


todo: write more regex
     bullet one and bullet 2 should look like: 

     * one 
     * one
       (line break)
         * two
         * two

todo: take a brief look at how to pass through lines through Pandoc
Done: then run pandoc and output to rst directory. 
Done: move rst to /rst/
todo: rename .html.rst to .rst)
todo: postprocess_rst_regex to work 
todo: post process regex

      fix title)
      
Done: the convert grid table to list tables. 
Done: then run another regex on rst
Done: then run Sphinx.
Done: invoke the code in ..\rst\buildocs.bat from this file. Do not open new window and CD back to original location. 
