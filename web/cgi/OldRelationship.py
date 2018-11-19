class Relationship(object):
    def __init__(self, rels, importance, src, dest):
        self.rels = rels
        self.importance = importance
        self.src = src
        self.dest = dest
        self.style = {}
        for key in sorted(self.rels, key=lambda x: self.rels[x][0]):
            try:
                self.style = relTypes[key]['style']
            except:
                continue
        #src.addRelation(dest, self)
        #dest.addRelation(src, self)

    def __str__(self):
        return str(self.src)+'--('+str(self.rels)+','+str(self.importance)+')->'+str(self.dest)

    def getVal(self):
        val = 0
        denom = 0
        for rel in self.rels:
            val += self.rels[rel][0]*self.rels[rel][1]
            denom += self.rels[rel][0]
        try:
            return val/denom
        except:
            return val

    def graphGet(self, URL='/cgi-bin/getRel.py', target='relationship', style=False):
        fullURL = URL+'?src='+str(self.src.Id)+'&dest='+str(self.dest.Id)+'&recip=True&vis=True&max=25'
        retStr = str(self.src)+'->'+str(self.dest)+' [len=2, edgeURL="'+fullURL+'", target="'+target+'", penwidth="'+str(max(1,2.5*self.importance))+'"'
        if style:
            for val in self.style:
                retStr+=', '+val+'="'+self.style[val]+'"'
            if 'color' not in self.style:
                retStr+=', color="#'+format(int(255*max(-self.getVal(), 0)), '02x')+format(int(255*max(self.getVal(), 0)), '02x')+'00'+format(int(255*min(1,2.5*self.importance)), '02x')+'"'
        else:
            retStr+=', color="#'+format(int(255*max(-self.getVal(), 0)), '02x')+format(int(255*max(self.getVal(), 0)), '02x')+'00'+format(int(255*min(1,2.5*self.importance)), '02x')+'"'
        retStr +=']'
        return retStr

    def getHTML(self, numRels=3, visible=False):
        retStr = '<p class="relView" style="cursor: pointer;">'+str(self.src)+'--('+str(round(self.importance,2))+','+str(round(self.getVal(),2))+')->'+str(self.dest)+'</p><ul data-vis='+str(visible*1)+'>'
        i = 0
        for key in sorted(self.rels, key=self.rels.get, reverse=True):
            if i>=numRels:
                retStr+='<li data-vis="hidden" style="display: none;">'
            else:
                retStr+='<li data-vis="visible" '+(not visible)*'style="display: none;"'+'>'
            retStr+=str(key)
            retStr+=': (<span style="cursor: pointer;" class="importance" data-src='+str(self.src.Id)
            retStr+=' data-dest='+str(self.dest.Id)
            retStr+=' data-type='+str(key)+'>'
            retStr+=str(self.rels[key][0])
            retStr+='</span>'
            retStr+='<input style="display: none; width: 5em;" type="text" class="importanceField"'
            retStr+='data-src='+str(self.src.Id)
            retStr+=' data-dest='+str(self.dest.Id)
            retStr+=' data-rel='+str(key)
            retStr+=' data-value='+str(self.rels[key][0])
            retStr+=' value='+str(self.rels[key][0])+' />, '
            retStr+='<span style="cursor: pointer;" class="relVal" data-src='+str(self.src.Id)
            retStr+=' data-dest='+str(self.dest.Id)
            retStr+=' data-type='+str(key)+'>'
            retStr+=str(self.rels[key][1])
            retStr+='</span>'
            retStr+='<input style="display: none; width: 5em;" type="text" class="relValField"'
            retStr+='data-src='+str(self.src.Id)
            retStr+=' data-dest='+str(self.dest.Id)
            retStr+=' data-rel='+str(key)
            retStr+=' data-value='+str(self.rels[key][1])
            retStr+=' value='+str(self.rels[key][1])+' />)</li>'
            i += 1
        retStr+='</ul>'
        return retStr

def recipChild(parent, child):
    child.addRelation(parent, {'Parent': relTypes['Parentd']['importance']}, False)
    for rel in parent.relationships:
        if 'Child' in parent.relationships[rel].rels and parent.relationships[rel].dest!=child:
            child.addRelation(parent.relationships[rel].dest, {'Sibling': relTypes['Sibling']['importance']})

def recipParent(child, parent):
    parent.addRelation(child, {'Child': relTypes['Child']['importance']}, False)
    for rel in parent.relationships:
        if 'Child' in parent.relationships[rel].rels and parent.relationships[rel].dest!=child:
            child.addRelation(parent.relationships[rel].dest, {'Sibling': relTypes['Sibling']['importance']})
            
def recipSib(sib1, sib2):
    sib2.addRelation(sib1, {'Sibling': relTypes['Sibling']['importance']}, False)

def recipSpouse(spouse1, spouse2):
    spouse2.addRelation(spouse1, {'Spouse': relTypes['Spouse']['importance']}, False)
    
relTypes = {'Child': {'style': {'color':'blue'}, 'recip': recipChild, 'importance': 0.75}, 'Sibling': {'style': {'color':'green'}, 'recip': recipSib, 'importance': 0.75}, 'Spouse': {'style':(), 'recip': recipSpouse, 'importance': 0.75}, 'Parent': {'style': {'color':'red'}, 'recip': recipParent, 'importance': 0.75}}

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
