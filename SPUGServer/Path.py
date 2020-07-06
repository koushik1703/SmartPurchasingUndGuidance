from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser

class Path:

    def __init__(self):
        pathRoot = Element('Paths')

        for x in range(5):
            for y in range(5):
                if y != 4:
                    pathElement = SubElement(pathRoot, 'Path')
                    pathElement.set("fromX", str(x))
                    pathElement.set("fromY", str(y))
                    pathElement.set("toX", str(x))
                    pathElement.set("toY", str(y + 1))
                    pathElement.set("isPathOccupied", str(False))

                    pathElement = SubElement(pathRoot, 'Path')
                    pathElement.set("fromX", str(x))
                    pathElement.set("fromY", str(y + 1))
                    pathElement.set("toX", str(x))
                    pathElement.set("toY", str(y))
                    pathElement.set("isPathOccupied", str(False))
                if x != 4:
                    pathElement = SubElement(pathRoot, 'Path')
                    pathElement.set("fromX", str(x))
                    pathElement.set("fromY", str(y))
                    pathElement.set("toX", str(x + 1))
                    pathElement.set("toY", str(y))
                    pathElement.set("isPathOccupied", str(False))

                    pathElement = SubElement(pathRoot, 'Path')
                    pathElement.set("fromX", str(x + 1))
                    pathElement.set("fromY", str(y))
                    pathElement.set("toX", str(x))
                    pathElement.set("toY", str(y))
                    pathElement.set("isPathOccupied", str(False))

        XMLParser.getInstance().writeAndPretify(pathRoot, "Data/Paths.xml")
