import os
import re

# To insert a variable within a string or regex, pass f before the quotes:
# f"stringtofind {variable} ."
# rf'{first_var}'
title_wrapper = "******************************************************"

work_dir = os.path.dirname(os.path.realpath(__file__))

for file_name in os.listdir(work_dir):
    # if the file name ends with htm, can change to xml or other extension
    if file_name.endswith((".htm",".html")):
        absolute_path = os.path.join(work_dir, file_name)

        with open(absolute_path, 'r+', encoding="utf-8") as f:

            a_tag = f.read()
            # doesn't cover enough cases: a_tag = re.sub(r'<A\sNAME=\"pgfId-\d+\"></A>', '', a_tag)
            a_tag = re.sub(r'<A NAME=(.*)></A>', '', a_tag)
            a_tag = re.sub(r'<A NAME=\"marker-\d+\"></A>', '', a_tag)
            a_tag = re.sub(r'<P CLASS=\"FM1Head\">\s*(.*)\s*</P>', rf'{title_wrapper}\n\1\n{title_wrapper}\n\n', a_tag)            
            a_tag = re.sub(r'<H4 CLASS=\"FM1Head\">\n([a-zA-Z0-9 ]*)</H4>', rf'{title_wrapper}\n\1\n{title_wrapper}\n\n', a_tag)
            # a_tag = re.sub(r'<H1 CLASS="FM2Head-Top">', '<h1>', a_tag)
            a_tag = re.sub(r'<H1 CLASS=\"FM2Head-Top\">([\s\S]*?)</H1>', r'<h1>\1\n</h1>', a_tag)
            # a_tag = re.sub(r'<H1 CLASS="FM2Head">', '<h1>', a_tag)
            a_tag = re.sub(r'<H1 CLASS=\"FM2Head\">([\s\S]*?)</H1>', r'<h1>\1\n</h1>', a_tag)          
            # a_tag = re.sub(r'<H2 CLASS="FM3Head-Top">', '<h2>', a_tag)
            a_tag = re.sub(r'<H2 CLASS=\"FM3Head-Top\">([\s\S]*?)</H2>', r'<h2>\1\n</h2>', a_tag)
            # a_tag = re.sub(r'<H2 CLASS="FM3Head">', '<h2>', a_tag)
            a_tag = re.sub(r'<H2 CLASS=\"FM3Head\">([\s\S]*?)</H2>', r'<h2>\1\n</h2>', a_tag)
            # a_tag = re.sub(r'<H3 CLASS=\"FM4Head-NoTOC\">', '<h3>', a_tag)
            a_tag = re.sub(r'<H3 CLASS=\"FM4Head-NoTOC\">([\s\S]*?)</H3>', r'<h3>\1\n</h3>', a_tag)
            a_tag = re.sub(r'<DIV>', '', a_tag)
            a_tag = re.sub(r'</DIV>', '', a_tag)
            a_tag = re.sub(r'<EM CLASS=\"Courier\">\n', '<EM CLASS=\"Courier\">', a_tag)
            a_tag = re.sub(r'<EM CLASS=\"Courier\">(.*)</EM>', r'<code>\1</code>', a_tag)
            # Remove smart double quotes
            a_tag = re.sub(r'[\u201C\u201D\u201E\u201F\u2033\u2036]', r'\"', a_tag)
            # Remove smart single quotes
            a_tag = re.sub(r'[\u2018\u2019\u201A\u201B\u2032\u2035]', "'", a_tag)

            a_tag = re.sub(r'<P CLASS=\"CodeReference\">\n(.*)</P>', r'\1', a_tag)
            # Would like to include \n<P CLASS=\"CodeReference\"> in the find, but it doesn't work
            a_tag = re.sub(r'<h3>\n(Syntax)(.*)</h3>', r'<b>\1</b>\n\n\n<pre>', a_tag)    
            a_tag = re.sub(r'<h3>\n(Example)( )<\/h3>', r'<b>\1</b>\n\n\n<pre>', a_tag) 
            a_tag = re.sub(r'<h3>\n(Returns)( )*<\/h3>', r'<b>\1</b>\n\n\n<pre> ', a_tag) 
            # Need to use a negative look ahead and add </pre> when the next line does not start with <P CLASS=\"CodeReference\">
            a_tag = re.sub(r'', r'', a_tag) 
            ################## Table cleanup
            # This works when the preceding text is a code example
            a_tag = re.sub(r'<h3>\n(Properties)( )*</h3>', r'</pre>\n\n<b>\1</b>\n', a_tag) 
            a_tag = re.sub(r'<H5 CLASS=\"TableAnchor\">\n&nbsp;</H5>', r'', a_tag) 
            # Note styles
            a_tag = re.sub(r'<P CLASS=\"Note\">([\s\S]*?)</P>', r'<div CLASS="note">\1</div>', a_tag)
            a_tag = re.sub(r'<P CLASS=\"NoteIndent\">([\s\S]*?)</P>', r'<div CLASS="warning">\1</div>', a_tag)
            a_tag = re.sub(r'<P CLASS=\"NoteTip\">([\s\S]*?)</P>', r'<div CLASS="tip">\1</div>', a_tag)
            a_tag = re.sub(r'<P CLASS=\"NoteCaution\">([\s\S]*?)</P>', r'<div CLASS="caution">\1</div>', a_tag)

            # Bullet Styles
            a_tag = re.sub(r'(?s)</LI>\s*<UL>(.*?)\s*</UL>', r'<UL>\1\n\t\t</UL>\n\t\t</LI>', a_tag)


            f.seek(0)
            f.write(a_tag)
            f.truncate()
