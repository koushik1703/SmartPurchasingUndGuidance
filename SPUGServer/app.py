from flask import Flask
from flask_restful import Resource, Api
from Cart import Cart
from Item import Item

carts = []
items = []
app = Flask(__name__)
api = Api(app)

class cartAssign(Resource):
    def get(self, cartNum):
        return carts[cartNum].assign()

class itemCount(Resource):
    def get(self, itemNum):
        return {items[itemNum].name : items[itemNum].count}, 200

class cartUnAssign(Resource):
    def get(self, cartNum):
        return carts[cartNum].unassign()

@app.route('/')
def hello_world():
    return 'Hello World!'

api.add_resource(cartAssign, '/getCart/<int:cartNum>')
api.add_resource(itemCount, '/getItemCount/<int:itemNum>')
api.add_resource(cartUnAssign, '/giveCart/<int:cartNum>')


if __name__ == '__main__':
    for cartNum in range(20):
        carts.append(Cart(cartNum))

    for itemNum in range(30):
        itemName = "item" + str(itemNum)
        items.append(Item(itemNum, itemName, 500))

    app.run(host='0.0.0.0')
