class ILPubAct90To92Struct:
    def __init__(self, id, maxGroup):
        self.id = id
        self.maxGroup = maxGroup
    def basePubActUrl(self):
        return 'http://www.ilga.gov/legislation/publicacts/pubact' + str(self.id) + '/pa' + str(self.id) + 'group'
    def currGroupPubActUrl(self, currGroup):
        return self.basePubActUrl() + str(currGroup) + '.html'
    def printSelf(self):
        print self.id
        print self.maxGroup