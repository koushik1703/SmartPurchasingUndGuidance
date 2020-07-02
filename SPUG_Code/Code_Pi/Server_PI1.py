import time
from Motor import *
from Ultrasonic import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685

#MQTT Communication Requirements
import time
import pika
import numpy as np

class Server_PI:

    def run(self):
    
        self.Pwm=Servo()
    
        self.Pwm.setServoPwm('0',90)
        
        self.Pwm.setServoPwm('1',90)
        
        timeout = 0.5

        credentials = pika.PlainCredentials('newuser1', 'password')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 
                                              5672, '/', credentials))

        channel = connection.channel()

        channel.queue_declare(queue='Pi2PC.Data')

        channel.exchange_declare(exchange='Pi2PC.topic', exchange_type='topic', durable = True, auto_delete = False)

        while True:
	
            distance = self.Ultrasonic.get_distance()
            
            IRSensor1 = GPIO.input(IR01)
            
            IRSensor2 = GPIO.input(IR02)
            
            IRSensor3 = GPIO.input(IR03)
            
	        message_from_pi = time.ctime() + " Distance to Obstacle: %"+ str(distance)+"%" \
                     + "IR Sensor1: %"+ str(IRSensor1)+"%" + "IR Sensor2: %" \
                     + str(IRSensor2)+"%" + "IR Sensor3: %"+ str(IRSensor3)+"%"
    
	        channel.basic_publish(exchange = 'Pi2PC.topic', routing_key = 'Cart101.ShoppingMall.DistanceIRSensorVal', body = message_from_pi)
	
	        print('Sent from PI: ' + message1)
            
	        time.sleep(timeout)
            
            
Ser = Server_PI()      
if __name__=='__main__':

    print ('Program is running on PI ... ')

    Ser.run()
    
    sys.exit(0)
	