import time
import paho.mqtt.client as mqtt
import json
import threading
from random import randrange

class PublisherSimulation:
    def __init__(self, interval, name):
        self.interval = interval
        self.name = name

    def execute(self):
        self.mqttPublisher = mqtt.Client('item tracking')
        self.mqttPublisher.connect('192.168.137.1', 1883, 70)
        self.thread = threading.Thread(target=self.startLooping)
        self.thread.start()

    def startLooping(self):
        self.mqttPublisher.loop_start()
        while True:
            message = { "itemPurchasedX" : str(randrange(5)), "itemPurchasedY" : str(randrange(5)), "cartName" : self.name}
            jmsg = json.dumps(message)
            self.mqttPublisher.publish('item/', jmsg, 2)
            time.sleep(self.interval)


if __name__ == '__main__':
    for cart in range(20):
        PublisherSimulation(randrange(20), "cart" + str(cart)).execute()