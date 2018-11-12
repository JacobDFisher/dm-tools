#!/usr/bin/env python3
import cgi, cgitb
import Character

def main():
    form = cgi.FieldStorage()
    print("Content-Type: text/html")
    print()
    if 'src' not in form or 'dest' not in form or 'rel' not in form or ('relVal' not in form and 'importance' not in form):
        print('Error in args')
        return
    try:
        src = Character.getById(int(form['src'].value))
    except:
        src = Character.getByName(form['src'].value)
    try:
        dest = Character.getById(int(form['dest'].value))
    except:
        dest = Character.getByName(form['dest'].value)
    rel = form['rel'].value
    if 'importance' in form:
        imp = float(form['importance'].value)
    else:
        imp = src.relationships[dest.Id].rels[rel][0]
    if 'relVal' in form:
        relVal = float(form['relVal'].value)
    else:
        relVal = src.relationships[dest.Id].rels[rel][1]
    src.addRelation(dest, {rel: (imp, relVal)})

cgitb.enable(display=0, logdir="/var/dm-tools/web/logs")

main()
