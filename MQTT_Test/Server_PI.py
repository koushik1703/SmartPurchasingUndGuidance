import time
import pika
import numpy as np
import sys

class Server_PI:
    def run(self):
    
        port = 7
        
        timeout = 3

        credentials = pika.PlainCredentials('the_user', 'the_pass')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.2', 5672, '/', credentials))

        channel = connection.channel()

        channel.queue_declare(queue='MegDeep.temperature')

        channel.exchange_declare(exchange='MegDeep.topic', exchange_type='topic', durable = True, auto_delete = False)

        while True:
	
	        [temperature, humidity] = [np.random.rand()*10, np.random.rand()*10]
	        message1 = time.ctime() + " Temperature: %" + str(temperature) + "%" + " Humidity: %" + str(humidity) + "%"
    
	        channel.basic_publish(exchange = 'MegDeep.topic', routing_key = '12A.8.DeepyaRoom.corner.temperature', body = message1)
	
	        print('Sent from PI: ' + message1)
            
	        time.sleep(timeout)
            
            
Ser = Server_PI()      
if __name__=='__main__':

    print ('Program is running on PI ... ')

    Ser.run()
    
    sys.exit(0)
	