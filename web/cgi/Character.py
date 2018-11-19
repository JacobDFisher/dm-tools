import redis
from RedisTools import nameBuilder as nb
from Role import Role
from Relationship import Relationship

#TODO Each relationship should be broken down like
# {Friend: 0.75, Sibling: 0.25} where the right number is an estimate of how important it is to see them in that way
# was percentage of time with them in that fashion
# Revamp Relationship

class Character(object):
    chars = dict()
    danglingRels = dict()
    def __init__(self, Id=None, name=None, save=False, depth=0):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.groups = {0:0}
        if Id == None and name is not None:
            Id = r.hget(nb('name2Id',0), name)
        #Create a new Character and add to db
        if Id == None and name is not None and save==True:
            with r.pipeline() as pipe:
                while True:
                    try:
                        pipe.watch(nb('numChars',0))
                        self.Id = int(pipe.get(nb('numChars', 0)))
                        pipe.incr(nb('numChars', 0))
                        pipe.execute()
                        break
                    except WatchError:
                        continue
                    finally:
                        pipe.reset()
            r.hset(nb('character', 0, self.Id), 'name', name)
            r.hsetnx(nb('name2Id', 0), name, str(self.Id))
        #Get character by Id
        elif Id is not None:
            self.Id = Id
        #Character doesn't exist, and we're not creating a new one
        else:
            raise(Exception())
        #DON'T SAVE ANYTHING UNTIL AFTER HERE#
        Character.chars[self.Id]=self
        self.traits={}
        self.impTraits={}
        #Load Char Groups from redis
        if not r.exists(nb('charGroups', 0, self.Id)):
            r.hset(nb('charGroups', 0, self.Id), 0, 0)

        #Load Char Traits from redis
        if r.exists(nb('character', 0, self.Id)):
            traits = r.hgetall(nb('character', 0, self.Id))
            for trait in traits.keys():
                if trait[:5] == b'role:':
                    self.traits[str(trait, 'utf-8')] = {}
                    roleTraits = r.hgetall(nb('charTraits', 0, self.Id, Role.getByName(str(trait[5:], 'utf-8')).Id))
                    if roleTraits is not None:
                        for roleTrait in roleTraits:
                            self.traits[str(trait, 'utf-8')][str(roleTrait, 'utf-8')] = float(roleTraits[roleTrait])
                else:
                    self.traits[str(trait, 'utf-8')] = str(traits[trait], 'utf-8')
        else:
            raise(Exception())

        #Load importance from redis
        if r.exists(nb('charImp', 0, self.Id)):
            traits = r.smembers(nb('charImp', 0, self.Id))
            for trait in traits:
                self.impTraits[str(trait, 'utf-8')] = {}
                roleTraits = r.hgetall(nb('impVal', 0, self.Id, Role.getByName(str(trait, 'utf-8')).Id))
                if roleTraits is not None:
                    for roleTrait in roleTraits:
                        self.impTraits[str(trait, 'utf-8')][str(roleTrait, 'utf-8')] = float(roleTraits[roleTrait])
        
        self.rels = {}
        if r.exists(nb('relationships', 0, self.Id)):
            rels = r.smembers(nb('relationships', 0, self.Id))
            for rel in rels:
                myRels = {}
                if r.exists(nb('relVal', 0, self.Id, rel)):
                    relVals = r.hgetall(nb('relVal', 0, self.Id, rel))
                    for rMem in relVals.keys():
                        myRels[str(rMem, 'utf-8')] = float(relVals[rMem])
                    try:
                        self.rels[int(rel)] = Relationship(self, Character.getById(int(rel), depth-1), myRels)
                    except Exception as e:
                        try:
                            Character.danglingRels[int(rel)][self.Id] = dict(myRels)
                        except:
                            Character.danglingRels[int(rel)] = {self.Id: dict(myRels)}
                if self.Id in Character.danglingRels:
                    for relId in Character.danglingRels[self.Id]:
                        try:
                            rel = Character.getById(relId)
                            rel.relationships[self.Id] = Relationship(rel, self, Character.danglingRels[self.Id][relId].values)
                        except:
                            pass
        if save:
            r.save()

    def __str__(self):
        try:
            return str(self.traits['name'])
        except:
            return str(self.Id)

    def addRole(self, dest, role, freq=1):
        try:
            self.rels[dest.Id].addRole(role, freq)
        except KeyError:
            self.rels[dest.Id] = Relationship(self, dest, {role: freq})
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.hset(nb('relVal', 0, self.Id, dest.Id), role, freq)

    def setImpTrait(self, role, trait, val):
        roleObject = Role.getByName(role)
        try:
            self.impTraits[role][trait] = val
        except KeyError:
            self.impTraits[role] = {trait:val}
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.sadd(nb('charImp', 0, self.Id), role)
        r.hset(nb('impVal', 0, self.Id, roleObject.Id), trait, val)

    def setTrait(self, role, trait, val):
        roleObject = Role.getByName(role)
        try:
            self.traits['role:'+role][trait] = val
        except KeyError:
            self.traits['role:'+role] = {trait:val}
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.hset(nb('character', 0, self.Id), 'role:'+role, 0)
        r.hset(nb('charTraits', 0, self.Id, roleObject.Id), trait, val)

    def getImpTraits(self, role=None):
        if role is not None:
            return self.impTraits.get(role, {})
        else:
            return self.impTraits

    def getTraits(self, role=None):
        if role is not None:
            return self.traits.get('role:'+role, {})
        else:
            return self.traits

    def getTrait(self, trait, role=None):
        if role is not None:
            try:
                return self.traits['role:'+role][trait]
            except:
                pass
        try:
            return self.traits[trait]
        except:
            return 0.0

    def relVal(self, dest, role=None):
        return self.rels[dest].getVal(role)

    @classmethod
    def getById(cls, Id, depth=0):
        if Id in cls.chars:
            return cls.chars[Id]
        elif depth<0:
            raise(Exception("Max depth reached"))
        else:
            return cls(Id, depth=depth)

    @classmethod
    def getByName(cls, name, depth=0):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        try:
            Id = int(r.hget('name2Id:0', name))
            return cls.getById(Id, depth)
        except Exception as e:
            print(type(e), e)
            return None
