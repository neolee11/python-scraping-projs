class PublicAct:
    # OLDER GA SHOULD HAVE extraUrlParts
    def __init__(self, content, childUrl, extraUrlParts):

        content = content.replace(u'\xa0', u' ')
        splitPattern = '    '  # 4 spaces
        if extraUrlParts:
            splitPattern = '   '  # 3 spaces
        tokens = content.split(splitPattern)

        self.name = tokens[-1].title()
        baseUrl = 'http://www.ilga.gov/legislation/publicacts/'
        fullUrl = baseUrl + extraUrlParts + childUrl
        self.fullUrl = fullUrl

        self.PAFullStr = tokens[0]

        PAStrParts = tokens[0].split(' ')  # To Get 92-0291 from Public Act 92-0291
        PAParts = PAStrParts[-1].split('-')
        self.PAShortGA = int(PAParts[0])
        self.PAShortActNum = int(PAParts[1])
    # def getFullUrl(self):
    #     return self.fullUrl
    def printSelf(self):
        print self.fullUrl
        print self.name
        print self.PAFullStr
        print self.PAShortGA
        print self.PAShortActNum
    def publicmMethod(self):
        print 'public method'
        self.__testPrivate()
    def __testPrivate(self):
        print 'private method'