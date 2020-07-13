from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser
import random
from random import randrange

class Point:

    def __init__(self):
        pointRoot = Element('Points')

        for x in range(4):
            for y in range(4):

                pointElement = SubElement(pointRoot, 'Point')
                pointElement.set("X", str(x))
                pointElement.set("Y", str(y))
                randomNumber = randrange(16)
                if(randomNumber >= 3):
                    pointElement.set("isPointOccupied", str(False))
                else:
                    pointElement.set("isPointOccupied", str(True))

        XMLParser.getInstance().writeAndPretify(pointRoot, "Data/Points.xml")
