import json

from flask_restful import Resource
import xml.etree.ElementTree as ElementTree
from QueryConstructor import QueryConstructor

class GetCartDetail(Resource):
    def get(self):
        cartRoot = ElementTree.parse("Data/Carts.xml").getroot()

        countTrue = 0
        countFalse = 0

        for i in range(8):
            cartQuery = QueryConstructor.getInstance().constructWithOneParameter("Cart", "cartNum", str(i))

            if(cartRoot.find(cartQuery).get('isAssigned') == "True"):
                countTrue = countTrue + 1;
            else:
                countFalse = countFalse + 1;

        response = str(countTrue) + ', ' + str(countFalse)

        return response, 200
