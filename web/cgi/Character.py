from Relationship import Relationship, relTypes

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

Relationship('Spouse', a, b)
Relationship('Spouse', b, a)
Relationship('Child', a, c)
Relationship('Child', b, c)

Relationship('Spouse', d, e)
Relationship('Spouse', e, d)
Relationship('Child', d, f)
Relationship('Child', e, f)

Relationship('Spouse', c, f)
Relationship('Spouse', f, c)
Relationship('Child', c, g)
Relationship('Child', f, g)
Relationship('Child', c, h)
Relationship('Child', f, h)
Relationship('Sibling', g, h)
Relationship('Sibling', h, g)

Relationship('Child', e, i)
Relationship('Child', d, i)

Relationship('Sibling', f, i)
Relationship('Sibling', i, f)
