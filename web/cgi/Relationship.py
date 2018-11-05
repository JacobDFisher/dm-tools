class Relationship(object):
    def __init__(self, rels, importance, src, dest):
        self.rels = rels
        self.importance = importance
        self.src = src
        self.dest = dest
        self.style = ()
        for key in self.rels:
            try:
                self.style = relTypes[key]['style']
            except:
                continue
        #src.addRelation(dest, self)
        #dest.addRelation(src, self)

    def __str__(self):
        return str(self.src)+'--('+str(self.rels)+','+str(self.importance)+')->'+str(self.dest)

    def graphGet(self, URL='/cgi-bin/getRel.py', target='relationship'):
        retStr = str(self.src)+'->'+str(self.dest)+' [URL="'+URL+'?src='+str(self.src.Id)+'&dest='+str(self.dest.Id)+'", target="'+target+'", penwidth="'+str(max(1,2.5*self.importance))+'"'#+', color="#'+format(int(255*max(-self.rels[0], 0)), '02x')+format(int(255*max(self.rels[0], 0)), '02x')+'00'+format(int(255*min(1,2.5*self.importance)), '02x')+'"'
        for val in self.style:
            retStr+=', '+val
        retStr +=']'
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
    
relTypes = {'Child': {'style': ('color="blue"',), 'recip': recipChild, 'importance': 0.75}, 'Sibling': {'style': ('color="green"',), 'recip': recipSib}, 'Spouse': {'style':(), 'recip': recipSpouse}, 'Parent': {'style': ('color="red"',), 'recip': recipParent}}

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
