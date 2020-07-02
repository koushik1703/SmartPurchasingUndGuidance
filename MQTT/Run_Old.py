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

#-------------------------------------------------------------
IR01 = 14
IR02 = 15
IR03 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR01,GPIO.IN)
GPIO.setup(IR02,GPIO.IN)
GPIO.setup(IR03,GPIO.IN)


#-------------------------------------------------------

class SPUG:
    def run(self):
    
        self.Ultrasonic=Ultrasonic()
        
        self.Pwm=Servo()
        
        credentials = pika.PlainCredentials('newuser1', 'password')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 5672 ,'/', credentials))

        channel = connection.channel()

        channel.exchange_declare(exchange='PC2Pi.topic',exchange_type='topic', durable=True, auto_delete=False)

        channel.queue_declare(queue='PC2Pi.Processed_Data')

        channel.queue_bind(queue='PC2Pi.Processed_Data', exchange='PC2Pi.topic', routing_key='Processed_Data')
        
        while True:
            self.LMR=0x00
            if GPIO.input(IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(IR03)==True:
                self.LMR=(self.LMR | 1)
                
            self.Pwm.setServoPwm('0',90)
            self.Pwm.setServoPwm('1',90)    
            distance = self.Ultrasonic.get_distance()
            IRSensor1 = (GPIO.input(IR01)==True)
            IRSensor2 = (GPIO.input(IR02)==True)
            IRSensor3 = (GPIO.input(IR03)==True)
            
            if distance > 10:
            
              if self.LMR==2:
                  PWM.setMotorModel(575,575,575,575)
              elif self.LMR==4:
                  PWM.setMotorModel(-1500,-1500,2500,2500)
              elif self.LMR==6:
                  PWM.setMotorModel(-2000,-2000,4000,4000)
              elif self.LMR==1:
                  PWM.setMotorModel(2500,2500,-1500,-1500)
              elif self.LMR==3:
                  PWM.setMotorModel(4000,4000,-2000,-2000)
              elif self.LMR==7:
                  pass
            
            else:
                PWM.setMotorModel(0,0,0,0)
                
            message1 = time.ctime() + " Distance to Obstacle: "+ str(distance)+ \
            "%" + "IR Sensor1: %"+ str(IRSensor1)+"%"+ "IR Sensor2: %"+ str(IRSensor2)+"%" \
             + "IR Sensor3: %"+ str(IRSensor3)+"%"
                
            channel.basic_publish(exchange = 'Pi2PC.topic',routing_key = 'Cart101.ShoppingMall.DistanceIRSensorVal',
                                  body = message1)
            
            print('Sent_1' + message1)
            time.sleep(timeout)
            
l_spug=SPUG()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    
    try:
        l_spug.run()
        
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)

