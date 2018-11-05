class Relationship(object):
    def __init__(self, rels, importance, src, dest):
        self.rels = rels
        self.importance = importance
        self.src = src
        self.dest = dest
        self.style = {}
        for key in self.rels:
            try:
                self.style = relTypes[key]['style']
            except:
                continue
        #src.addRelation(dest, self)
        #dest.addRelation(src, self)

    def __str__(self):
        return str(self.src)+'--('+str(self.rels)+','+str(self.importance)+')->'+str(self.dest)

    def getVal(self):
        return 0

    def graphGet(self, URL='/cgi-bin/getRel.py', target='relationship'):
        fullURL = URL+'?src='+str(self.src.Id)+'&dest='+str(self.dest.Id)
        retStr = str(self.src)+'->'+str(self.dest)+' [len=1, edgeURL="'+fullURL+'", target="'+target+'", penwidth="'+str(max(1,2.5*self.importance))+'"'
        for val in self.style:
            retStr+=', '+val+'="'+self.style[val]+'"'
        if 'color' not in self.style:
            retStr+=', color="#'+format(int(255*max(-self.getVal(), 0)), '02x')+format(int(255*max(self.getVal(), 0)), '02x')+'00'+format(int(255*min(1,2.5*self.importance)), '02x')+'"'
        retStr +=']'
        return retStr

    def getHTML(self, numRels=3):
        retStr = '<div><p>'+str(self.src)+'--('+str(self.getVal())+','+str(self.importance)+')->'+str(self.dest)+'</p><ul>'
        i = 0
        for key in sorted(self.rels, key=self.rels.get, reverse=True):
            if i>=numRels:
                retStr+='<li hidden>'
            else:
                retStr+='<li>'
            retStr+=str(key)+': <span class="importance", data-src="'+str(self.src.Id)+'", data-dest="'+str(self.dest.Id)+'", data-type="'+str(key)+'">'+str(self.rels[key])+'</span></li>'
        retStr+='</ul></div>'
        return retStr

def recipChild(parent, child):
    child.addRelation(parent, {'Parent': 0.75}, False)
    for rel in parent.relationships:
        if 'Child' in parent.relationships[rel].rels and parent.relationships[rel].dest!=child:
            child.addRelation(parent.relationships[rel].dest, {'Sibling': 0.75})

def recipParent(child, parent):
    parent.addRelation(child, {'Child': 0.75}, False)
    for rel in parent.relationships:
        if 'Child' in parent.relationships[rel].rels and parent.relationships[rel].dest!=child:
            child.addRelation(parent.relationships[rel].dest, {'Sibling': 0.75})
            
def recipSib(sib1, sib2):
    sib2.addRelation(sib1, {'Sibling': 0.75}, False)

def recipSpouse(spouse1, spouse2):
    spouse2.addRelation(spouse1, {'Spouse': 0.75}, False)
    
relTypes = {'Child': {'style': {'color':'blue'}, 'recip': recipChild, 'importance': 0.75}, 'Sibling': {'style': {'color':'green'}, 'recip': recipSib}, 'Spouse': {'style':(), 'recip': recipSpouse}, 'Parent': {'style': {'color':'red'}, 'recip': recipParent}}

class FamilialRelationship(Relationship):
    def __init__(self, relType, src, dest):
        self.relType=relType
        self.src = src
        self.dest = dest
        src.addRelation(dest, self)
        dest.addRelation(src, self)

    def __str__(self):
        return str(self.src)+'--'+self.relType+'->'+str(self.dest)

    def graphGet(self, URL='/cgi-bin/getRel.py', target='relationship'):
        retStr = str(self.src)+'->'+str(self.dest)+' [URL="'+URL+'?src='+str(self.src)+'&dest='+str(self.dest)+'", target="'+target+'"'
        try:
            if len(relTypes[self.relType]) > 0:
                for val in relTypes[self.relType]:
                    retStr+=', '+val
        except:
            pass
        retStr+=']'
        return retStr
