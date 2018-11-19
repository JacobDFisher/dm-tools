class Relationship(object):
    def __init__(self, src, dest, roles):
        self.rels = dict(roles)
        self.src = src
        self.dest = dest

    def addRole(self, role, freq):
        self.rels[role] = freq

    def getFreq(self, role=None):
        if role is None:
            return max(self.rels.values())
        else:
            return self.rels[role]

    def getVal(self, role=None):
        retVal = 0
        if role is None:
            for rol in self.rels:
                retVal += self.rels[rol]*self.getVal(rol) # Frequency*Value
        else:
            denom = 0
            if role in self.rels:
                srcImp = self.src.getImpTraits(role)
                for trait in srcImp:
                    denom += srcImp[trait]
                    retVal += srcImp[trait]*self.dest.getTrait(trait, role) #Try a trait specific to the role
                try:
                    retVal /= denom
                except:
                    retVal = 0
        return retVal
                
