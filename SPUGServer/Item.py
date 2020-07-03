from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser

class Item:

    def __init__(self):
        itemRoot = Element('Items')

        for i in range(20):
            itemElement = SubElement(itemRoot, 'Item')
            itemElement.set("itemNum", str(i))
            itemElement.set("name", "item" + str(i))
            itemElement.set("count", str(500))

        XMLParser.getInstance().writeAndPretify(itemRoot, "Items.xml")
