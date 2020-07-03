from xml.etree.ElementTree import  Element, SubElement
from XMLParsar import XMLParser

class Cart:

    def __init__(self):
        cartRoot = Element('Carts')

        for i in range(20):
            cartElement = SubElement(cartRoot, 'Cart')
            cartElement.set("cartNum", str(i))
            cartElement.set("name", "cart" + str(i))
            cartElement.set("isAssigned", str(False))


        XMLParser.getInstance().writeAndPretify(cartRoot, "Carts.xml")