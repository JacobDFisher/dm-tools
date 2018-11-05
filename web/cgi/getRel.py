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
            src = Character.Character(int(form['src'].value))
            for rel in src.relationships:
                print(src.relationships[rel].getHTML())
                print(Character.Character.chars[rel].relationships[int(form['src'].value)].getHTML())
                #print('<p>'+str(src.relationships[rel])+'</p>')
                #print('<p>'+str(Character.Character.chars[rel].relationships[int(form['src'].value)]))
        except:
            pass
    else:
        try:
            src = Character.Character(int(form['src'].value))
            dest = Character.Character.chars[int(form['dest'].value)]
            #print('<p>'+str(src.relationships[dest.Id])+'</p>')
            print(src.relationships[dest.Id].getHTML())
        except:
            pass
    print('</body></html>')

cgitb.enable(display=0, logdir="/home/jacob/Desktop/992/web/logs")

main()
