from flask_restful import Resource
import xml.etree.ElementTree as ElementTree
from XMLParsar import XMLParser
from QueryConstructor import QueryConstructor

class CartUnAssign(Resource):
    def get(self, cartNum):
        cartRoot = ElementTree.parse("Data/Carts.xml").getroot()
        cartQuery = QueryConstructor.getInstance().constructWithOneParameter("Cart", "cartNum", str(cartNum))
        cartRoot.find(cartQuery).set('isAssigned', 'False')
        cartRoot.find(cartQuery).set('AssignedToDevice', '')
        XMLParser.getInstance().writeAndPretify(cartRoot, "Data/Carts.xml")
        return 200
