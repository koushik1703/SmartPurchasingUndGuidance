import paho.mqtt.client as mqtt
import threading

class Item:
    def __init__(self, itemNum, name, count):
        self.itemNum = itemNum
        self.name = name
        self.count = count
        self.subscribe_to_changes()

    def on_message(self):
        self.count -= 1;

    def subscribe_to_changes(self):
        self.mqtt_subsriber = mqtt.Client(self.name)
        self.mqtt_subsriber.on_message = self.on_message
        self.mqtt_subsriber.connect('127.0.0.1', 1883, 70)
        self.mqtt_subsriber.subscribe('item/' + str(self.itemNum), qos=2)
        self.thread = threading.Thread(target=self.startLooping)
        self.thread.start()

    def startLooping(self):
        self.mqtt_subsriber.loop_forever()