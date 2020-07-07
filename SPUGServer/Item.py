from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser
from random import randrange

class Item:

    def __init__(self):
        itemRoot = Element('Items')

        index = 0
        for i in range(5):
            for j in range(5):
                itemElement = SubElement(itemRoot, 'Item')
                itemElement.set("itemNum", str(index))
                itemElement.set("name", "item" + str(index))
                itemElement.set("itemX", str(i))
                itemElement.set("itemY", str(j))
                itemElement.set("count", str(randrange(500)))
                itemElement.set("cost", str(randrange(200)))
                itemElement.set("calorie", str(randrange(1000)))
                itemElement.set("fat", str(randrange(100)))
                itemElement.set("carbohydrate", str(randrange(10)))
                itemElement.set("protein", str(randrange(5)))
                itemElement.set("salt", str(randrange(10)))
                index = index + 1;

        XMLParser.getInstance().writeAndPretify(itemRoot, "Data/Items.xml")
