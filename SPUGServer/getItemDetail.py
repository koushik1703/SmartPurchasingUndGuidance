import json

from flask_restful import Resource
import xml.etree.ElementTree as ElementTree
from QueryConstructor import QueryConstructor

class getItemDetail(Resource):
    def get(self):
        itemRoot = ElementTree.parse("Data/Items.xml").getroot()

        response = ''

        for i in range(16):
            itemQuery = QueryConstructor.getInstance().constructWithOneParameter("Item", "name", 'item' + str(i))

            if i <15:
                response = response + itemRoot.find(itemQuery).get('count') + ', '
            else:
                response = response + itemRoot.find(itemQuery).get('count')

        return response, 200
