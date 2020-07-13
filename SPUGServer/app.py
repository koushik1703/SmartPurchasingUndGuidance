from flask import Flask, send_from_directory, Response
from flask_restful import Api
from Cart import Cart
from Item import Item
from Point import Point
import xml.etree.ElementTree as ElementTree
from ItemCount import ItemCount
from CartAssign import CartAssign
from CartUnAssign import CartUnAssign
from MQTT import MQTT
from flask_cors import CORS
from getItemDetail import getItemDetail
from GetCartDetail import GetCartDetail

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

@app.route('/admin/item.html')
def send_itemhtml():
    return send_from_directory('', 'item.html')

@app.route('/admin/cart.html')
def send_carthtml():
    return send_from_directory('', 'cart.html')

@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(CartAssign, '/getCart/<int:cartNum>/<deviceId>')
api.add_resource(ItemCount, '/getItemCount/<itemName>')
api.add_resource(CartUnAssign, '/giveCart/<int:cartNum>')
api.add_resource(getItemDetail, '/getDetail')
api.add_resource(GetCartDetail, '/getcartDetail')


if __name__ == '__main__':

    items = Item()
    carts = Cart()
    points = Point()

    itemRoot = ElementTree.parse("Data/Items.xml").getroot()
    cartRoot = ElementTree.parse("Data/Carts.xml").getroot()
    pointRoot = ElementTree.parse("Data/Points.xml").getroot()

    mqtt = MQTT()

    app.run(host='0.0.0.0')
