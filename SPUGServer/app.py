from flask import Flask
from flask_restful import Api
from Cart import Cart
from Item import Item
from Path import Path
import xml.etree.ElementTree as ElementTree
from ItemCount import ItemCount
from CartAssign import CartAssign
from CartUnAssign import CartUnAssign
from PathOccupied import IsPathOccupied
from MQTT import MQTT

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(CartAssign, '/getCart/<int:cartNum>/<deviceId>')
api.add_resource(ItemCount, '/getItemCount/<itemName>')
api.add_resource(CartUnAssign, '/giveCart/<int:cartNum>')
api.add_resource(IsPathOccupied, '/isPathOccupied/<int:fromX>/<int:fromY>/<int:toX>/<int:toY>')


if __name__ == '__main__':

    items = Item()
    carts = Cart()
    paths = Path()

    itemRoot = ElementTree.parse("Items.xml").getroot()
    cartRoot = ElementTree.parse("Carts.xml").getroot()
    pathRoot = ElementTree.parse("Paths.xml").getroot()

    mqtt = MQTT()

    app.run(host='0.0.0.0')
