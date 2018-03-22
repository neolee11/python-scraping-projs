import xml.etree.cElementTree as ET
import requests

from xml.dom import minidom
from lxml import html
from ILPubAct93To99Struct import ILPubAct93To99Struct
from ILPubAct90To92Struct import ILPubAct90To92Struct
from PublicAct import PublicAct

pubActXPathPattern = '//li//a'
pubActXPathPattern_PA91Group10 = 'strong/font'

pubAct93To99StructArray = [ILPubAct93To99Struct(99, 938), ILPubAct93To99Struct(98, 1175),
                           ILPubAct93To99Struct(97, 1173), ILPubAct93To99Struct(96, 1555),
                           ILPubAct93To99Struct(95, 1056), ILPubAct93To99Struct(94, 1113),
                           ILPubAct93To99Struct(93, 1102)]

pubAct90To92StructArray = [ILPubAct90To92Struct(92, 9), ILPubAct90To92Struct(91, 10), ILPubAct90To92Struct(90, 9)]

pubActList = []

def parsePage(page, extraUrlPart):
    tree = html.fromstring(page.content)
    pubActsEls = tree.xpath(pubActXPathPattern)
    for pubActEl in pubActsEls:
        text = pubActEl.text
        if text == None:
            subEls = pubActEl.xpath(pubActXPathPattern_PA91Group10)  # special treatment Public Act 91 Group 10 page
            text = subEls[0].text
            # print text
        pubAct = PublicAct(text, pubActEl.attrib['href'], extraUrlPart)
        pubActList.append(pubAct)

def getPageContent(url, extraUrlPart):
    page = requests.get(url)
    if page.status_code == 200:
       parsePage(page, extraUrlPart)
    else:
        print url + ' Invalid!'


for pubAct in pubAct93To99StructArray:
    url = pubAct.pubActUrl()
    getPageContent(url, '')

for pubAct in pubAct90To92StructArray:
    for currGroup in range(1, pubAct.maxGroup + 1):
        url = pubAct.currGroupPubActUrl(currGroup)
        extraUrlPart = 'pubact' + str(pubAct.id) + '/'
        getPageContent(url, extraUrlPart)


# write output
doc = ET.Element("Document")
ilPubActsEl = ET.SubElement(doc, "IllinoisPublicActs")


# ET.SubElement(ilPubActsEl, "PublicAct", name="blah").text = "some value1"
total = 0
for pubAct in pubActList:
    # pubAct.printSelf()
    paEl = ET.SubElement(ilPubActsEl, "PublicAct")
    ET.SubElement(paEl, "Name").text = pubAct.name
    ET.SubElement(paEl, "Url").text = pubAct.fullUrl
    ET.SubElement(paEl, "PubActFullStr").text = pubAct.PAFullStr
    ET.SubElement(paEl, "PubActShortGA").text = str(pubAct.PAShortGA)
    ET.SubElement(paEl, "PubActShortActNum").text = str(pubAct.PAShortActNum)
    total += 1

xmlstr = minidom.parseString(ET.tostring(doc)).toprettyxml(indent="   ")
with open("output.xml", "w") as f:
    f.write(xmlstr)

print "Total Public Acts: " + str(total)

# tree = ET.ElementTree(doc)
# tree.write("filename.xml", xml_declaration=True, encoding='utf-8')