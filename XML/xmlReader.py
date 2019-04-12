"""
@author: Gabriel Torrandella
"""

import xml.etree.ElementTree as ET

documentTree = ET.parse("Banco.xml")

root = documentTree.getroot()
print(root.tag, root.attrib)

for i in root.iter('caja_ahorro'):
    print(i.tag, i.attrib)
for i in root.iter('cuenta_corriente'):
    print(i.tag, i.attrib)
