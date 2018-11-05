import redis
from Relationship import Relationship, relTypes, FamilialRelationship

class Character(object):
    chars = dict()
    def __init__(self, Id=None, name=None, save=True):
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
        #Set up traits here
        self.relationships = {}
        if r.exists('relationships:0:'+str(self.Id)):
            rels = r.smembers('relationships:0:'+str(self.Id))
            for rel in rels:
                myRels = {}
                if r.exists('relationship:0:'+str(self.Id)+':'+str(int(rel))):
                    relMems = r.hgetall('relationship:0:'+str(self.Id)+':'+str(int(rel)))
                    for rMem in relMems.keys():
                        myRels[rMem.decode('utf-8')] = float(relMems[rMem])
                self.relationships[int(rel)] = Relationship(myRels, max(myRels.values()), self, Character.getById(int(rel)))
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
        r.hmset('relationship:0:'+str(self.Id)+':'+str(other.Id), relation)
        if other.Id in self.relationships:
            for key in relation:
                self.relationships[other.Id].rels[key] = relation[key]
                if relation[key] > self.relationships[other.Id].importance:
                    self.relationships[other.Id].importance = relation[key]
        else:
            self.relationships[other.Id] = Relationship(relation, max(relation.values()), self, other)
        if recip:
            for rel in relation:
                try:
                    relTypes[rel]['recip'](self, other)
                except:
                    continue

    def getById(Id):
        if Id in Character.chars:
            return Character.chars[Id]
        else:
            return Character(Id)

    def getByName(name):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        Id = r.hget('name2Id:0', name)
        return getCharById(Id)

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
                for k in Character.getById(key).relationships.keys():
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
            graphString+='\t{rank=same; '+str(Character.getById(first))
            for val in charList[i]:
                graphString+=', '+str(Character.getById(val))
            graphString+='}\n'
            graphString+='\t'+str(Character.getById(first))+';\n'
            for val in charList[i]:
                graphString+='\t'+str(Character.getById(val))+';\n'
        for char in charSet:
            graphString+=str(Character.getById(char))+'[URL="'+URL+'?id='+str(char)+'", target="'+target+'"];\n'
            for dest in Character.getById(char).relationships:
                if dest in charSet:
                    if Character.getById(char).relationships[dest].src == Character.getById(char):
                        graphString+='\t'+Character.getById(char).relationships[dest].graphGet()+';\n'
        graphString+='}\n'
        return (str(self)+'graph', bytes(graphString, 'utf-8'))
