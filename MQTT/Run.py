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
    
        Data_Copy =  open('Data_PI.csv', 'w')
    
        Data_Copy.write("Date;Movement_Type;\n")
        
        while True:
        
            def Write_into_CSV(body):
                x = format(body).split("%")
                Data_Copy =  open('Data_PI.csv', 'a')
                Movement_Type = int(x[1])
                Data_Copy.write("%s;"%time.ctime())
                Data_Copy.write("%d;"%Movement_Type)
                Data_Copy.close()
                
                if(Movement_Type == 5):
                    PWM.setMotorModel(600,600,600,600)
                    
                elif(Movement_Type == 1):
                     PWM.setMotorModel(-2000,-2000,4000,4000)
                    
                elif(Movement_Type == 3):
                    PWM.setMotorModel(-1200,-1200,2000,2000)
                    
                elif(Movement_Type == 7):
                    PWM.setMotorModel(2000,2000,-1200,-1200)
                    
                elif(Movement_Type == 9):
                    PWM.setMotorModel(4000,4000,-2000,-2000)
                    
                elif(Movement_Type == 0):
                    PWM.setMotorModel(0,0,0,0)
    
            def callback(ch, method, properties, body):
                print('Received from PC: {}'.format(body))
                Write_into_CSV(body)

            channel.basic_consume(queue='PC2Pi.Processed_Data', on_message_callback=callback, auto_ack=True)

            print('Waiting for Messages from PC')

            channel.start_consuming()       
                
            
l_spug=SPUG()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    
    try:
        l_spug.run()
        
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)



