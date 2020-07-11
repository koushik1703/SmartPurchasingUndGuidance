from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser
from random import randrange

class Item:

    def __init__(self):
        itemRoot = Element('Items')

        index = 0
        for i in range(4):
            for j in range(4):
                itemElement = SubElement(itemRoot, 'Item')
                itemElement.set("itemNum", str(index))
                itemElement.set("name", "item" + str(index))
                itemElement.set("itemX", str(i))
                itemElement.set("itemY", str(j))
                itemElement.set("count", str(randrange(100)))
                index = index + 1;

        XMLParser.getInstance().writeAndPretify(itemRoot, "Data/Items.xml")
