import json
import threading
import xml.etree.ElementTree as ElementTree
from QueryConstructor import QueryConstructor
from XMLParsar import XMLParser
import time

import paho.mqtt.client as mqtt

class MQTT:

    def __init__(self):
        mqttIp = '192.168.0.102'
        MQTT.mqtt_subscriber = mqtt.Client('item tracking receiver')
        MQTT.mqtt_subscriber.on_message = MQTT.on_message
        MQTT.mqtt_subscriber.connect(mqttIp, 1883, 70)
        MQTT.mqtt_subscriber.subscribe('item/', 2)
        MQTT.mqtt_subscriber.subscribe('pointOccupy/', 2)
        MQTT.mqtt_subscriber.subscribe('pointUnoccupy/', 2)
        MQTT.mqtt_subscriber.subscribe('buyItemFromDevice/', 2)
        MQTT.mqtt_subscriber.subscribe('toBuyItem/', 2)

        MQTT.mqtt_publisher = mqtt.Client('Device update publisher')
        MQTT.mqtt_publisher.connect(mqttIp, 1883, 70)

        threadSubscriber = threading.Thread(target=self.startLoopingSubscriber)
        threadSubscriber.start()

        threadPublisher = threading.Thread(target=self.startLoopingPublisher)
        threadPublisher.start()

    def on_message(client, userdata, message):
        messageJson = json.loads(message.payload.decode())
        itemRoot = ElementTree.parse("Data/Items.xml").getroot()
        cartRoot = ElementTree.parse("Data/Carts.xml").getroot()
        pointRoot = ElementTree.parse("Data/Points.xml").getroot()

        if message.topic == 'item/':
            print("received item/")
            itemPurchasedX = messageJson["itemPurchasedX"]
            itemPurchasedY = messageJson["itemPurchasedY"]
            cartName = messageJson["cartName"]

            itemQuery = QueryConstructor.getInstance().constructWithTwoParameter("Item", "itemX", itemPurchasedX, "itemY", itemPurchasedY)

            cartQuery = QueryConstructor.getInstance().constructWithOneParameter("Cart", "name", cartName)
            deviceIdOfCart = cartRoot.find(cartQuery).get('AssignedToDevice')

            message = {"itemPurchased": itemRoot.find(itemQuery).get('name')}
            jmsg = json.dumps(message)
            MQTT.mqtt_publisher.publish('deviceUpdate/' + deviceIdOfCart + '/', jmsg, 2)
            print("device update published")

        if message.topic == 'pointOccupy/':
            x = messageJson["x"]
            y = messageJson["y"]

            pointQuery = QueryConstructor.getInstance().constructWithFourParameter("Point", "X", x, "Y", y)
            pointRoot.find(pointQuery).set("isPointOccupied", "True")
            XMLParser.getInstance().writeAndPretify(pointRoot, "Data/Points.xml")

        if message.topic == 'pointUnoccupy/':
            x = messageJson["x"]
            y = messageJson["y"]

            pointQuery = QueryConstructor.getInstance().constructWithFourParameter("Point", "X", x, "Y", y)
            pointRoot.find(pointQuery).set("isPointOccupied", "False")
            XMLParser.getInstance().writeAndPretify(pointRoot, "Data/Points.xml")

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

            if itemName == "over":
                for i in range(4):
                    for j in range(4):
                        print("point iterator")
                        pointQuery = QueryConstructor.getInstance().constructWithTwoParameter("Point", "X", str(i), "Y", str(j))
                        print(pointQuery)
                        if pointRoot.find(pointQuery).get("isPointOccupied") == "True":
                            print("point is occupied")
                            message = {"X": pointRoot.find(pointQuery).get("X"), "Y": pointRoot.find(pointQuery).get("Y")}
                            jmsg = json.dumps(message)
                            print(message)
                            MQTT.mqtt_publisher.publish('pointOccupied/'+ cartName + '/', jmsg, 2)
                            print("published")


                message = {"X": "-1", "Y": "-1"}
                jmsg = json.dumps(message)
                MQTT.mqtt_publisher.publish('pointOccupied/' + cartName + '/', jmsg, 2)

        if message.topic == 'toBuyItem/':
            toBuyItem = messageJson["toBuyItem"]
            deviceId = messageJson["deviceId"]
            itemName = messageJson["itemPurchased"]

            if toBuyItem == "YES":
                itemQuery = QueryConstructor.getInstance().constructWithOneParameter("Item", "name", itemName)
                currCount = int(itemRoot.find(itemQuery).get('count')) - 1;
                itemRoot.find(itemQuery).set('count', str(currCount))

            message = {"null": "null"}
            jmsg = json.dumps(message)
            cartQuery = QueryConstructor.getInstance().constructWithOneParameter("Cart", "AssignedToDevice", deviceId)
            MQTT.mqtt_publisher.publish('continue/' + cartRoot.find(cartQuery).get('cartNum') + '/', jmsg, 2)

            XMLParser.getInstance().writeAndPretify(itemRoot, "Data/Items.xml")


    def startLoopingSubscriber(self):
        MQTT.mqtt_subscriber.loop_forever()

    def startLoopingPublisher(self):
        MQTT.mqtt_publisher.loop_start()
