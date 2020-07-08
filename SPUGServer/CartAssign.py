from flask_restful import Resource
import xml.etree.ElementTree as ElementTree
from XMLParsar import XMLParser

class CartAssign(Resource):
    def get(self, cartNum, deviceId):

        cartRoot = ElementTree.parse("Data/Carts.xml").getroot()
        cartQuery = ".//Cart[@cartNum='" + str(cartNum) + "']"
        if cartRoot.find(cartQuery).get('isAssigned') == "False":
            cartRoot.find(cartQuery).set('isAssigned', 'True')
            cartRoot.find(cartQuery).set('AssignedToDevice', str(deviceId))
            XMLParser.getInstance().writeAndPretify(cartRoot, "Data/Carts.xml")
            return 200
        else:
            return 404
