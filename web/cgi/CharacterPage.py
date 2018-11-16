#!/usr/bin/env python3
import cgi, cgitb
from subprocess import Popen, PIPE, STDOUT
import Character
import redis
import re

def main():
    form = cgi.FieldStorage()
    print("Content-Type: text/html")
    print()
    print('<!DOCTYPE html>')
    print('<html><head>')
    print('<title>')
    if 'maxDepth' in form:
        depth = int(form['maxDepth'].value)
    else:
        depth = 1
    if 'id' not in form:
        print('Character List')
    else:
        char = Character.getById(int(form['id'].value), depth=depth)
        print(str(char))
    print('</title>')
    print('<style>')
    #print('[height="100%"] {height: 100%;}')
    print('* {box-sizing: border-box;} .column {float: left; width: 50%; padding: 10px;} html,body {height:100%} #RelationshipOverlay {Z-INDEX: 301; position: absolute; top: 10%; left: 10%; height: 80%; width: 80%; visibility: hidden; background-color: white; border} #RelationshipUnderlay {Z-INDEX: 300; position: fixed; background-color: black; width: 100%; height: 100%; visibility: hidden; top: 0px; left: 0px; opacity: 0.7;}')
    print('</style></head>')
    print('<body>')
    if 'id' not in form:
        print('<h2>Character List</h2>')
        print('<table style="width:100%">')
        print('<tr><th>Name</th></tr>')
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        numChars = int(r.get('numChars:0'))
        for char in range(numChars):
            name = r.hget('character:0:'+str(char), 'name').decode('utf-8')
            print('<tr><td><a href="/cgi-bin/CharacterPage.py?id='+str(char)+'" target="_self">'+name+'</a></td></tr>')
        print('</table></body></html>')
        return
    #try:
        #char=Character.Character.chars[form['name'].value]
    #except:
    #    print('<H1>Error</H1>')
    #    print('<p>Character not found</p>')
    #    print('</body></html>')
    #    return
    graphBytes = char.genGraph(maxDepth=depth)
    p = Popen(['fdp', '-Tpng', '-o', '../img/'+graphBytes[0]+'.png', '-Tcmapx'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    data = p.communicate(input=graphBytes[1])
    p.wait()
    print('<h2>'+str(char)+'</h2>')
    print('<div class="column" style="height:100%;">')
    print('<h3>'+str(char)+'\'s Traits</h3>')
    for trait in char.traits:
        print('<p>'+str(trait)+': '+str(char.traits[trait])+'</p>')
    print('</div>')
    print('<div class="column" style="height:100%;">')
    print('<IMG SRC="/img/'+graphBytes[0]+'.png" USEMAP="#'+graphBytes[0]+'" />')
    print('<br /><a class="showRels" href="/cgi-bin/getRel.py?src='+form['id'].value+'">Show All Relationships</a>')
    print('<a class="showRels" href="/cgi-bin/getRel.py?src='+form['id'].value+'&inOnly=1">Show Incoming</a>')
    print('<a class="showRels" href="/cgi-bin/getRel.py?src='+form['id'].value+'&outOnly=1">Show Outgoing</a>')
    print(re.sub('id="edge', 'class="graphEdge" id="edge',str(data[0], 'utf-8')))
    #print('<p>'+graphBytes[1].decode('utf-8')+'</p>')
    print('<p>'+str(data[1], 'utf-8')+'</p>')
    print('<object id="relationship" style="height:100%; width:100%" name=relationship data="/cgi-bin/getRel.py?&src='+form['id'].value+'"></object>')
    print('</div>')
    print('<div id="RelationshipUnderlay" style="cursor: pointer;"></div>')
    print('<div id="RelationshipOverlay"></div>')
    print('<script src="/test.js"></script>')
    print('</body></html>')
    return

cgitb.enable(display=0, logdir="/var/dm-tools/web/logs")

main()
        
