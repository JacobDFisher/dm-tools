import redis
from Relationship import Relationship, relTypes, FamilialRelationship

class Character(object):
    chars = dict()
    danglingRels = dict()
    def __init__(self, Id=None, name=None, save=True, depth=0):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        if Id == None and name is not None:
            Id = r.hget('name2Id:0', name)
        if Id == None and name is not None:
            with r.pipeline() as pipe:
                while 1:
                    try:
                        pipe.watch('numChars:0')
                        self.Id = int(pipe.get('numChars:0'))
                        pipe.incr('numChars:0')
                        pipe.execute()
                        break
                    except WatchError:
                        continue
                    finally:
                        pipe.reset()
            r.hset('character:0:'+str(self.Id), 'name', name)
            r.hsetnx('name2Id:0', name, str(self.Id))
        elif Id is not None:
            self.Id = Id
        else:
            return
        Character.chars[self.Id]=self
        self.traits={}
        if r.exists('character:0:'+str(self.Id)):
            traits = r.hgetall('character:0:'+str(self.Id))
            for trait in traits.keys():
                self.traits[trait.decode('utf-8')] = traits[trait].decode('utf-8')
        else:
            raise(Exception())
        #Set up traits here
        self.relationships = {}
        if r.exists('relationships:0:'+str(self.Id)):
            rels = r.smembers('relationships:0:'+str(self.Id))
            for rel in rels:
                myRels = {}
                if r.exists('relationship:0:'+str(self.Id)+':'+str(int(rel))):
                    relMems = r.hgetall('relationship:0:'+str(self.Id)+':'+str(int(rel)))
                    if not r.exists('relVal:0:'+str(self.Id)+':'+str(int(rel))):
                        r.hmset('relVal:0:'+str(self.Id)+':'+str(int(rel)), {key:0 for key in relMems})
                    relVals = r.hgetall('relVal:0:'+str(self.Id)+':'+str(int(rel)))
                    for rMem in relMems.keys():
                        myRels[rMem.decode('utf-8')] = (float(relMems[rMem]), float(relVals[rMem]))
                try:
                    self.relationships[int(rel)] = Relationship(myRels, max(myRels.values(), key=lambda x: x[0])[0], self, getById(int(rel), depth-1))
                except:
                    try:
                        Character.danglingRels[int(rel)][self.Id] = dict(myRels)
                    except:
                        Character.danglingRels[int(rel)] = {self.Id: dict(myRels)}
        if self.Id in Character.danglingRels:
            for relId in Character.danglingRels[self.Id]:
                try:
                    rel = getById(relId)
                    rel.relationships[self.Id] = Relationship(Character.danglingRels[self.Id][relId], max(Character.danglingRels[self.Id][relId].values(), key=lambda x: x[0])[0], rel, self)
                except:
                    pass
        if save:
            r.save()

    def __hash__(self):
        try:
            return hash(self.traits['name'])
        except:
            return hash(self.Id)

    def __str__(self):
        try:
            return self.traits['name']
        except:
            return str(self.Id)

    def addRelation(self, other, relation, recip=True):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.sadd('relationships:0:'+str(self.Id), str(other.Id))
        relImp = {key:value[0] for (key,value) in relation.items()}
        relVal = {key:value[1] for (key,value) in relation.items()}
        r.hmset('relationship:0:'+str(self.Id)+':'+str(other.Id), relImp)
        r.hmset('relVal:0:'+str(self.Id)+':'+str(other.Id), relVal)
        if other.Id in self.relationships:
            for key in relation:
                self.relationships[other.Id].rels[key] = relation[key]
                if relation[key][0] > self.relationships[other.Id].importance:
                    self.relationships[other.Id].importance = relation[key][0]
        else:
            self.relationships[other.Id] = Relationship(relation, max(relation.values(), key=lambda x: x[0])[0], self, other)
        if recip:
            for rel in relation:
                try:
                    relTypes[rel]['recip'](self, other)
                except:
                    continue

    def genGraph(self, maxDepth = 1, URL='/cgi-bin/CharacterPage.py', target='_self'):
        graphString = 'digraph '+str(self)+'graph {\n\t{rank=same; '+str(self)+' }\n'
        graphString += '\t'+str(self)+';\n'
        keys = self.relationships.keys()
        charList = [set([self.Id])]
        charSet = set([self.Id])
        for i in range(1, maxDepth+1):
            nextKeys = set()
            charList.append(set())
            for key in keys:
                charList[i].add(key)
                #Check this
                for k in getById(key).relationships.keys():
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
            graphString+='\t{rank=same; '+str(getById(first))
            for val in charList[i]:
                graphString+=', '+str(getById(val))
            graphString+='}\n'
            graphString+='\t'+str(getById(first))+';\n'
            for val in charList[i]:
                graphString+='\t'+str(getById(val))+';\n'
        for char in charSet:
            graphString+=str(getById(char))+'[URL="'+URL+'?id='+str(char)+'", target="'+target+'"];\n'
            for dest in getById(char).relationships:
                if dest in charSet:
                    if getById(char).relationships[dest].src == getById(char):
                        graphString+='\t'+getById(char).relationships[dest].graphGet()+';\n'
        graphString+='}\n'
        return (str(self)+'graph', bytes(graphString, 'utf-8'))

def getById(Id, depth=0):
    if Id in Character.chars:
        return Character.chars[Id]
    elif depth<0:
        raise(Exception("Max depth reached"))
    else:
        return Character(Id, depth=depth)

def getByName(name, depth=0):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    Id = int(r.hget('name2Id:0', name))
    return getById(Id, depth)