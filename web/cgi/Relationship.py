class Relationship(object):
    def __init__(self, rels, importance, src, dest):
        self.rels = rels
        self.importance = importance
        self.src = src
        self.dest = dest
        src.addRelation(dest, self)
        dest.addRelation(src, self)

    def __str__(self):
        return str(self.src)+'--('+str(self.rels[0])+','+str(self.importance)+')->'+str(self.dest)

    def graphGet(self, URL='/cgi-bin/getRel.py', target='relationship'):
        retStr = str(self.src)+'->'+str(self.dest)+' [URL="'+URL+'?src='+str(self.src)+'&dest='+str(self.dest)+'", target="'+target+'", penwidth='+str(max(1,2.5*self.importance))+', color="#'+format(int(255*max(-self.rels[0], 0)), '02x')+format(int(255*max(self.rels[0], 0)), '02x')+'00'+format(int(255*min(1,2.5*self.importance)), '02x')+'"'
        retStr +=']'
        return retStr

relTypes = {'Child': ('color="blue"',), 'Sibling': ('color="green"',), 'Spouse': ()}

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
