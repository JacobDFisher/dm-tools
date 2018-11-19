import redis
from RedisTools import nameBuilder as nb

class Role(object):
    roles = {}
    def __init__(self, name='', save=False):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.name = name
        try:
            self.Id = int(r.hget(nb('role2Id', 0), self.name))
        except TypeError as e:
            #print(type(e), e)
            if not save:
                raise(Exception('Role {:s} does not exist'.format(name)))
            with r.pipeline() as pipe:
                while True:
                    try:
                        pipe.watch(nb('numRoles', 0))
                        self.Id = int(pipe.get(nb('numRoles', 0)))
                        pipe.incr(nb('numRoles', 0))
                        pipe.execute()
                        break
                    except WatchError:
                        continue
                    finally:
                        pipe.reset()
            if self.name != '':
                r.hsetnx(nb('role2Id', 0), self.name, str(self.Id))
        Role.roles[self.name] = self
        if save:
            r.save()

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def getByName(cls, name):
        if name in cls.roles:
            return cls.roles[name]
        else:
            return cls(name, False)        

    @classmethod
    def new(cls, name):
        return cls(name, True)

    @classmethod
    def pop(cls, name):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.hdel(nb('role2Id', 0), name)
        try:
            del(cls.roles[name])
            cls.roles.pop(name)
        except:
            pass
            

def main():
    Role(name='Everyone')
    Role(name='Parent')
    Role(name='Child')
    Role(name='Sibling')
    Role(name='Older Sibling')
    Role(name='Younger Sibling')
    Role(name='Spouse')
    Role(name='Student')
    Role(name='Teacher')
    Role(name='Housemate')
    Role(name='Acquaintance')
    Role(name='Friend')
    Role(name='Merchant')
    Role(name='Noble')
    Role(name='Employer')
    Role(name='Employee')


