import lxml.etree as ET
import os

for f in os.listdir():
    if '.svg' in f:
        
        svg = ET.parse(f)
        root = svg.getroot()

        for i, elem in enumerate(root[-1].iter()):
            if i > 1:
                if '}text' in elem.tag or ('}rect' in elem.tag and 'DeadZone' in elem.attrib['id']):
                    p = elem.getparent()
                    p.remove(elem)

        svg.write(str(f'edited_{f}'))
