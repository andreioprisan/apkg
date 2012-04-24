# proof of concept

#todo: finish writer that can delete/update/insert nodes from existing XML
# not part of GSoC - past deadline implementation  

import xml.dom.minidom
from xml.dom.minidom import parseString


def get_xml_document(filename):
    return xml.dom.minidom.parse(filename)

def find_xml_element(xmlDoc, elementName):
    thisElement = None
    for eachElement in xmlDoc.childNodes:
        if eachElement.nodeType == eachElement.ELEMENT_NODE and eachElement.localName == elementName:
            thisElement = eachElement
            break
    return thisElement

# set up xml file
doc = get_xml_document("/Users/andrei/documents/workspace/apkg/pkg/devel/tools/autoconf/autoconf-2.62-1.xml")

# top element
root = doc.documentElement

# find build tag
buildContext = find_xml_element(doc, "build")

# create execute tag
executeElement = doc.createElementNS(None,'execute')

# add it in tree
root.appendChild(executeElement)

# create gnuconfig tag
gnuconfigElement = doc.createElementNS(None,'gnuconfig')

# create gnuconfig tag under execute tag
executeElement.appendChild(gnuconfigElement)

# create gnuconfig tag
paramElement1 = doc.createElementNS(None,'param')

# create gnuconfig tag under execute tag
gnuconfigElement.appendChild(paramElement1)

paramText1 = doc.createTextNode(u'--prefix=/usr')
paramElement1.firstChild.appendChild(paramText1)

paramText2 = doc.createTextNode(u'--with-lds')
paramElement2.firstChild.appendChild(paramText2)

        
        