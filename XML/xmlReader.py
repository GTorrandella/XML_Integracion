"""
@author: Gabriel Torrandella
"""
import sys
import xml.etree.ElementTree as ET
import xmlschema
from RedisManager.manager import Manager

print(__name__)

"""
documentTree = ET.parse("Banco.xml")

root = documentTree.getroot()
print(root.tag, root.attrib)

for child in root:
    print(child.tag, child.attrib, child.text)
    for c2 in child:
        print(c2.tag, c2.attrib, c2.text)        
        for c3 in c2:
            print(c3.tag, c3.attrib, c3.text)        
            for c4 in c3:
                print(c4.tag, c4.attrib, c4.text)

"""
print(sys.argv)