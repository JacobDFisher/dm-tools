#!/usr/bin/env python3
import cgi, cgitb
import Character

def main():
    form = cgi.FieldStorage()
    print("Content-Type: text/html")
    print()
    print('<!DOCTYPE html>')
    print('<html><head>')
    print('<title>Page Title</title>')
    print('</head>')
    print('<body>')
    if 'src' not in form:
        print('<H1>Error</H1>')
        print('<p>Please fill out src field</p>')
        print('</body></html>')
        return
    if 'dest' not in form:
        try:
            src = Character.Character.chars[form['src'].value]
            for rels in src.relationships:
                for rel in src.relationships[rels]:
                    print('<p>'+str(rel)+'</p>')
        except:
            pass
    else:
        try:
            src = Character.Character.chars[form['src'].value]
            dest = Character.Character.chars[form['dest'].value]
            rels = src.relationships[dest]
            for rel in rels:
                print('<p>'+str(rel)+'</p>')
        except:
            pass
    print('</body></html>')

cgitb.enable(display=0, logdir="/home/jacob/Desktop/992/web/logs")

main()
