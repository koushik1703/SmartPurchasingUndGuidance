import json
import threading
import xml.etree.ElementTree as ElementTree
from QueryConstructor import QueryConstructor
from XMLParsar import XMLParser

import paho.mqtt.client as mqtt

class MQTT:

    def __init__(self):
        MQTT.mqtt_subscriber = mqtt.Client('item tracking receiver')
        MQTT.mqtt_subscriber.on_message = MQTT.on_message
        MQTT.mqtt_subscriber.connect('192.168.137.1', 1883, 70)
        MQTT.mqtt_subscriber.subscribe('item/', 2)
        MQTT.mqtt_subscriber.subscribe('pathOccupy/', 2)
        MQTT.mqtt_subscriber.subscribe('pathUnoccupy/', 2)
        MQTT.mqtt_subscriber.subscribe('buyItemFromDevice/', 2)

        MQTT.mqtt_publisher = mqtt.Client('Device update publisher')
        MQTT.mqtt_publisher.connect('192.168.137.1', 1883, 70)

        threadSubscriber = threading.Thread(target=self.startLoopingSubscriber)
        threadSubscriber.start()

        threadPublisher = threading.Thread(target=self.startLoopingPublisher)
        threadPublisher.start()

    def on_message(client, userdata, message):
        messageJson = json.loads(message.payload.decode())
        itemRoot = ElementTree.parse("Items.xml").getroot()
        cartRoot = ElementTree.parse("Carts.xml").getroot()
        pathRoot = ElementTree.parse("Paths.xml").getroot()
        if message.topic == 'item/':
            itemPurchasedX = messageJson["itemPurchasedX"]
            itemPurchasedY = messageJson["itemPurchasedY"]
            cartName = messageJson["cartName"]

            itemQuery = QueryConstructor.getInstance().constructWithTwoParameter("Item", "itemX", itemPurchasedX, "itemY", itemPurchasedY)
            currCount = int(itemRoot.find(itemQuery).get('count')) - 1
            costOfItem = itemRoot.find(itemQuery).get('cost')
            itemRoot.find(itemQuery).set('count', str(currCount))

            cartQuery = QueryConstructor.getInstance().constructWithOneParameter("Cart", "name", cartName)
            deviceIdOfCart = cartRoot.find(cartQuery).get('AssignedToDevice')

            message = {"itemPurchased": itemRoot.find(itemQuery).get('name'), "cost": costOfItem}
            jmsg = json.dumps(message)
            MQTT.mqtt_publisher.publish('deviceUpdate/' + deviceIdOfCart + '/', jmsg, 2)

            XMLParser.getInstance().writeAndPretify(itemRoot, "Items.xml")

        if message.topic == 'pathOccupy/':
            fromX = messageJson["fromx"]
            fromY = messageJson["fromy"]
            toX = messageJson["tox"]
            toY = messageJson["toy"]

            pathQuery = QueryConstructor.getInstance().constructWithFourParameter("Path", "fromX", fromX, "fromY", fromY, "toX", toX, "toY", toY)
            pathRoot.find(pathQuery).set("isPathOccupied", "True")
            pathQuery = QueryConstructor.getInstance().constructWithFourParameter("Path", "toX", toX, "toY", toY, "fromX", fromX, "fromY", fromY)
            pathRoot.find(pathQuery).set("isPathOccupied", "True")
            XMLParser.getInstance().writeAndPretify(pathRoot, "Paths.xml")

        if message.topic == 'pathUnoccupy/':
            fromX = messageJson["fromx"]
            fromY = messageJson["fromy"]
            toX = messageJson["tox"]
            toY = messageJson["toy"]

            pathQuery = QueryConstructor.getInstance().constructWithFourParameter("Path", "fromX", fromX, "fromY", fromY, "toX", toX, "toY", toY)
            pathRoot.find(pathQuery).set("isPathOccupied", "False")
            pathQuery = QueryConstructor.getInstance().constructWithFourParameter("Path", "toX", toX, "toY", toY, "fromX", fromX, "fromY", fromY)
            pathRoot.find(pathQuery).set("isPathOccupied", "False")
            XMLParser.getInstance().writeAndPretify(pathRoot, "Paths.xml")

        if message.topic == 'buyItemFromDevice/':
            itemName = messageJson["itemName"]
            deviceId = messageJson["deviceId"]

            if itemName == "over":
                itemX = "-1"
                itemY = "-1"
            else:
                itemQuery = QueryConstructor.getInstance().constructWithOneParameter("Item", "name", itemName)
                itemX = itemRoot.find(itemQuery).get("itemX")
                itemY = itemRoot.find(itemQuery).get("itemY")

            cartQuery = QueryConstructor.getInstance().constructWithOneParameter("Cart", "AssignedToDevice", deviceId)

            cartName = cartRoot.find(cartQuery).get('cartNum')
            message = {"itemX": itemX, "itemY": itemY}
            jmsg = json.dumps(message)
            MQTT.mqtt_publisher.publish('buyItemFromServer/' + cartName + '/', jmsg, 2)

    def startLoopingSubscriber(self):
        MQTT.mqtt_subscriber.loop_forever()

    def startLoopingPublisher(self):
        MQTT.mqtt_publisher.loop_start()