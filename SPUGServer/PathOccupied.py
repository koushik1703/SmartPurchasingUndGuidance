from flask_restful import Resource
import xml.etree.ElementTree as ElementTree
from QueryConstructor import QueryConstructor

class IsPathOccupied(Resource):
    def get(self, fromX, fromY, toX, toY):
        pathRoot = ElementTree.parse("Data/Paths.xml").getroot()
        pathQuery = QueryConstructor.getInstance().constructWithFourParameter("Path", "fromX", fromX, "fromY", fromY, "toX", toX, "toY", toY)
        if pathRoot.find(pathQuery).get("isPathOccupied") == "False":
            return 200
        else:
            return 404
