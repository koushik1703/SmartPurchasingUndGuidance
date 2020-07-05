from flask_restful import Resource
import xml.etree.ElementTree as ElementTree
from QueryConstructor import QueryConstructor

class ItemCount(Resource):
    def get(self, itemName):
        itemRoot = ElementTree.parse("Items.xml").getroot()
        itemQuery = QueryConstructor.getInstance().constructWithOneParameter("Item", "name", itemName)
        int(itemRoot.find(itemQuery).get('count'))
        return {itemRoot.find(itemQuery).get('name') : itemRoot.find(itemQuery).get('count')}, 200