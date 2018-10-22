#!/usr/bin/env python3
import cgi, cgitb
from subprocess import Popen, PIPE, STDOUT
import Character

def main():
    form = cgi.FieldStorage()
    print("Content-Type: text/html")
    print()
    print('<DOCTYPE html>')
    print('<html><head>')
    print('<title>')
    if 'name' not in form:
        print('Character List')
    else:
        print(form['name'].value)
    print('</title>')
    print('<style>')
    print('* {box-sizing: border-box;} .column {float: left; width: 50%; padding: 10px;} html,body {height:100%}')
    print('</style></head>')
    print('<body>')
    if 'name' not in form:
        print('<h2>Character List</h2>')
        print('<table style="width:100%">')
        print('<tr><th>Name</th></tr>')
        for char in sorted(Character.Character.chars):
            print('<tr><td><a href="/cgi-bin/CharacterPage.py?name='+char+'" target="_self">'+char+'</a></td></tr>')
        print('</table></body></html>')
        return
    try:
        char=Character.Character.chars[form['name'].value]
    except:
        print('<H1>Error</H1>')
        print('<p>Character not found</p>')
        print('</body></html>')
        return
    if 'maxDepth' in form:
        graphBytes = char.genGraph(maxDepth = int(form['maxDepth'].value))
    else:
        graphBytes = char.genGraph()
    p = Popen(['circo', '-Tpng', '-o', '../img/'+graphBytes[0]+'.png', '-Tcmapx'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    data = p.communicate(input=graphBytes[1])
    p.wait()
    print('<h2>'+str(char)+'</h2>')
    print('<div class="column" height="100%" width="100%">')
    print('<h3>'+str(char)+'\'s Traits</h3>')
    for trait in char.traits:
        print('<p>'+str(trait)+'</p>')
    print('</div>')
    print('<div class="column" height="100%" width="100%">')
    print('<IMG SRC="/img/'+graphBytes[0]+'.png" USEMAP="#'+graphBytes[0]+'" />')
    print(str(data[0], 'utf-8'))
    print('<p>'+str(data[1], 'utf-8')+'</p>')
    print('<iframe height="100%" width="100%" name=relationship src="/cgi-bin/getRel.py?src='+form['name'].value+'"></iframe>')
    print('</body></html>')
    return

cgitb.enable(display=0, logdir="/home/jacob/Desktop/992/web/logs")

main()
        
