from xml.etree.ElementTree import tostring
import lxml.etree as ETree

class XMLParser:

    xmlParsar = None

    def getInstance():
        if XMLParser.xmlParsar == None:
            XMLParser.xmlParsar = XMLParser()

        return XMLParser.xmlParsar

    def writeAndPretify(self, root, filename):
        itemFile = open(filename, "w")
        itemFile.write(str(tostring(root).decode("utf-8")))
        itemFile.close()

        fileContent = ETree.parse(filename)
        itemFile = open(filename, "w")
        itemFile.write(str(ETree.tostring(fileContent, pretty_print=True).decode("utf-8")))
        itemFile.close()
