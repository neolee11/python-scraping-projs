class ILPubAct93To99Struct:
    def __init__(self, id, max):
        self.id = id
        self.max = max
    def pubActUrl(self):
        return 'http://www.ilga.gov/legislation/publicacts/grplist.asp?GA=' + str(self.id) + '&Min=0001&Max=' + str(self.max)
    def printSelf(self):
        print self.id
        print self.max