from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser

class Cart:

    def __init__(self):
        cartRoot = Element('Carts')

        for i in range(8):
            cartElement = SubElement(cartRoot, 'Cart')
            cartElement.set("cartNum", str(i))
            cartElement.set("name", "cart" + str(i))
            cartElement.set("isAssigned", str(False))
            cartElement.set("AssignedToDevice", "")

        XMLParser.getInstance().writeAndPretify(cartRoot, "Data/Carts.xml")
