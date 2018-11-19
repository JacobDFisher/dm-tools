#!/usr/bin/env python3
import cgi, cgitb
from Character import Character

def relGetHTML(rel, numRels=3, numRoles=3, visible=False):
    retStr = '<p class="relView" style="cursor: pointer;">'+str(rel.src)+'-- '+str(round(rel.getVal(),2))+' ->'+str(rel.dest)+'</p><ul data-vis='+str(visible*1)+'>'
    i = 0
    for key in sorted(rel.rels, key=rel.rels.get, reverse=True):
        if i>=numRels:
            retStr+='<li class="roleView" data-vis="hidden" style="display: none;">'
        else:
            retStr+='<li data-vis="visible" '+(not visible)*'style="display: none;"'+'><span style="cursor: pointer;" class="roleView">'
        retStr+=str(key)
        retStr+=': '
        retStr+='<span class="relVal" data-src='+str(rel.src.Id)
        retStr+=' data-dest='+str(rel.dest.Id)
        retStr+=' data-type='+str(key)+'>'
        retStr+=str(rel.rels[key])
        retStr+='*'
        retStr+=str(rel.getVal(key))
        retStr+='</span></span><ul data-vis='+str(visible*1)+'>'
        j=0
        for trait in sorted(rel.src.getImpTraits(key), key=lambda x: abs(rel.src.getImpTraits(key)[x]), reverse=True):
            if j>=numRels:
                retStr+='<li data-vis="hidden" style="display: none;">'
            else:
                retStr+='<li data-vis="visible" '+(not visible)*'style="display: none;"'+'>'
            retStr+=str(trait)
            retStr+=': '
            retStr+='<span>'
            retStr+=str(rel.src.getImpTraits(key)[trait])
            retStr+='*'
            retStr+=str(rel.dest.getTrait(trait, key))
            retStr+='</span></li>'
            j+=1
        retStr+='</ul></li>'
        i += 1
    retStr+='</ul>'
    return retStr

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
            for rel in src.rels:
                if 'inOnly' not in form:
                    print('<div>'+relGetHTML(src.rels[rel])+'</div>')
                if 'outOnly' not in form:
                    print('<div>'+relGetHTML(Character.getById(rel).rels[int(form['src'].value)])+'</div>')
                #print('<p>'+str(src.relationships[rel])+'</p>')
                #print('<p>'+str(Character.Character.chars[rel].relationships[int(form['src'].value)]))
        except Exception as e:
            print(e)
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
