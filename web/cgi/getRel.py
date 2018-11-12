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
    if 'max' in form:
        maxCount = int(form['max'].value)
    else:
        maxCount = 3
    if 'vis' in form:
        vis = True
    else:
        vis = False
    if 'src' not in form:
        print('<H1>Error</H1>')
        print('<p>Please fill out src field</p>')
        print('</body></html>')
        return
    print('<h3>Relationships are given in (importance, feelings) format.</h3>')
    if 'dest' not in form:
        try:
            src = Character.getById(int(form['src'].value), depth=1)
            for rel in src.relationships:
                if 'inOnly' not in form:
                    print('<div>'+src.relationships[rel].getHTML(maxCount, vis)+'</div>')
                if 'outOnly' not in form:
                    print('<div>'+Character.getById(rel).relationships[int(form['src'].value)].getHTML(maxCount, vis)+'</div>')
                #print('<p>'+str(src.relationships[rel])+'</p>')
                #print('<p>'+str(Character.Character.chars[rel].relationships[int(form['src'].value)]))
        except:
            pass
    else:
        try:
            src = Character.getById(int(form['src'].value))
            dest = Character.getById(int(form['dest'].value))
            if 'recip' in form:
                print('<div>'+src.relationships[dest.Id].getHTML(maxCount, vis)+'</div>')
                print('<div>'+dest.relationships[src.Id].getHTML(maxCount, vis)+'</div>')
            else:
                #print('<p>'+str(src.relationships[dest.Id])+'</p>')
                print('<div>'+src.relationships[dest.Id].getHTML(maxCount, vis)+'</div>')
                print('<div>'+dest.relationships[src.Id].getHTML(maxCount, vis)+'</div>')
        except:
            pass
    print('<script src="/rels.js"></script>')
    print('</body></html>')

cgitb.enable(display=0, logdir="/var/dm-tools/web/logs")

main()
