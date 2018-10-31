from Relationship import Relationship, relTypes, FamilialRelationship

class Character(object):
    chars = dict()
    def __init__(self, name):
        self.name = name
        self.relationships = {}
        Character.chars[name]=self
        self.traits=set()

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def addRelation(self, other, relation):
        try:
            reList = self.relationships[other]
        except:
            reList = []
            self.relationships[other] = reList
        reList.append(relation)

    def printRelations(self):
        for rel in self.relationships:
            for x in self.relationships[rel]:
                print(x)

    def genGraph(self, maxDepth = 1, URL='/cgi-bin/CharacterPage.py', target='_self'):
        graphString = 'digraph '+self.name+'graph {\n\t{rank=same; '+self.name+' }\n'
        graphString += '\t'+self.name+';\n'
        keys = self.relationships.keys()
        charList = [set([self])]
        charSet = set([self])
        for i in range(1, maxDepth+1):
            nextKeys = set()
            charList.append(set())
            for key in keys:
                charList[i].add(key)
                #Check this
                for k in key.relationships.keys():
                    nextKeys.add(k)
            charList[i].difference_update(charSet)
            charSet.update(charList[i])
            nextKeys.difference_update(charSet)
            keys = nextKeys
        for i in range(1, maxDepth+1):
            try:
                first = charList[i].pop()
            except:
                break
            graphString+='\t{rank=same; '+first.name
            for val in charList[i]:
                graphString+=', '+val.name
            graphString+='}\n'
            graphString+='\t'+first.name+';\n'
            for val in charList[i]:
                graphString+='\t'+val.name+';\n'
        for char in charSet:
            graphString+=str(char)+'[URL="'+URL+'?name='+str(char)+'", target="'+target+'"];'
            for dest in char.relationships:
                if dest in charSet:
                    for rel in char.relationships[dest]:
                        if rel.src == char:
                            graphString+='\t'+rel.graphGet()+';\n'
        graphString+='}\n'
        #print(graphString)
        return (self.name+'graph', bytes(graphString, 'utf-8'))
        

a = Character('Alice')
b = Character('Bob')
c = Character('Cait')
d = Character('David')
e = Character('Emily')
f = Character('Francis')
g = Character('Gertrude')
h = Character('Harold')
i = Character('Ingrid')
j = Character('Jacob')

FamilialRelationship('Spouse', a, b)
FamilialRelationship('Spouse', b, a)
FamilialRelationship('Child', a, c)
FamilialRelationship('Child', b, c)

FamilialRelationship('Spouse', d, e)
FamilialRelationship('Spouse', e, d)
FamilialRelationship('Child', d, f)
FamilialRelationship('Child', e, f)

FamilialRelationship('Spouse', c, f)
FamilialRelationship('Spouse', f, c)
FamilialRelationship('Child', c, g)
FamilialRelationship('Child', f, g)
FamilialRelationship('Child', c, h)
FamilialRelationship('Child', f, h)
FamilialRelationship('Sibling', g, h)
FamilialRelationship('Sibling', h, g)

FamilialRelationship('Child', e, i)
FamilialRelationship('Child', d, i)

FamilialRelationship('Sibling', f, i)
FamilialRelationship('Sibling', i, f)

Relationship((0,[]), 1, j, a)
Relationship((-1,[]), 0.5, j, b)
Relationship((1,[]), 1, j, c)
Relationship((0,[]), 0.01, j, d)
