from flask import Flask
from flask_restful import Api
from Cart import Cart
from Item import Item
from Point import Point
import xml.etree.ElementTree as ElementTree
from ItemCount import ItemCount
from CartAssign import CartAssign
from CartUnAssign import CartUnAssign
from MQTT import MQTT

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(CartAssign, '/getCart/<int:cartNum>/<deviceId>')
api.add_resource(ItemCount, '/getItemCount/<itemName>')
api.add_resource(CartUnAssign, '/giveCart/<int:cartNum>')


if __name__ == '__main__':

    items = Item()
    carts = Cart()
    points = Point()

    itemRoot = ElementTree.parse("Data/Items.xml").getroot()
    cartRoot = ElementTree.parse("Data/Carts.xml").getroot()
    pointRoot = ElementTree.parse("Data/Points.xml").getroot()

    mqtt = MQTT()

    app.run(host='0.0.0.0')
