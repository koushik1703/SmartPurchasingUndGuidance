from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser
import random

class Point:

    def __init__(self):
        pointRoot = Element('Points')

        for x in range(5):
            for y in range(5):

                pointElement = SubElement(pointRoot, 'Point')
                pointElement.set("X", str(x))
                pointElement.set("Y", str(y))
                pointElement.set("isPointOccupied", str(random.choice([True, False])))

        XMLParser.getInstance().writeAndPretify(pointRoot, "Data/Points.xml")
