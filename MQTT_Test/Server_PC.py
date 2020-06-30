import time
import pika
import numpy as np
import sys

class Server_PC:
    def Reply_From_PC(self,Temp,Humidity):

        credentials = pika.PlainCredentials('the_user', 'the_pass')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.2', 5672, '/', credentials))

        channel = connection.channel()

        channel.queue_declare(queue='Processed.Data')

        channel.exchange_declare(exchange='Processed.topic', exchange_type='topic', durable = True, auto_delete = False)
        
        if(Temp > 6.0 and Humidity > 6.0):

            msg = time.ctime() + " Temperature: %" + str(Temp) + "%" + " Humidity: %" + str(Humidity) + "%"
    
            channel.basic_publish(exchange = 'Processed.topic', routing_key = 'Processed_Data', body = msg)
	
            print('Sent from PC: ' + msg)
        
    def run(self):
        print ('Program is running on PC ... ')
            
            
server_PC = Server_PC()      
if __name__=='__main__':

    server_PC.run()
    
    sys.exit(0)
	