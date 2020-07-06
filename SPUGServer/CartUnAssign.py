from flask_restful import Resource
import xml.etree.ElementTree as ElementTree
from XMLParsar import XMLParser

class CartUnAssign(Resource):
    def get(self, cartNum):
        cartRoot = ElementTree.parse("Data/Carts.xml").getroot()
        cartQuery = ".//Cart[@cartNum='" + str(cartNum) + "']"
        cartRoot.find(cartQuery).set('isAssigned', 'False')
        cartRoot.find(cartQuery).set('AssignedToDevice', '')
        XMLParser.getInstance().writeAndPretify(cartRoot, "Carts.xml")
        return 200