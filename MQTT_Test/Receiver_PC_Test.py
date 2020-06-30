import pika
import sys
import time
from Server_PC import *

class Receiver_PC:

    def run(self):
    
        self.Server_PC=Server_PC() 
    
        credentials = pika.PlainCredentials('the_user', 'the_pass')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.2', 5672 ,'/', credentials))

        channel = connection.channel()

        channel.exchange_declare(exchange='MegDeep.topic',exchange_type='topic', durable=True, auto_delete=False)

        channel.queue_declare(queue='MegDeep.temperature')

        channel.queue_bind(queue='MegDeep.temperature', exchange='MegDeep.topic', routing_key='12A.8.*.*.temperature')
    
        Data_Copy =  open('Data_PC.csv', 'w')
    
        Data_Copy.write("Date;Temperature_Value;Humidity_Value;\n")
        
        def Write_into_CSV(body):
            x = format(body).split("%")
            Data_Copy =  open('Data_PC.csv', 'a')
            Temp = float(x[1])
            Humidity = float(x[3])
            self.Server_PC.Reply_From_PC(Temp,Humidity)
            Data_Copy.write("%s;"%time.ctime())
            Data_Copy.write("%f;"%Temp)
            Data_Copy.write("%f;\n"%Humidity)
            Data_Copy.close()
    
        def callback(ch, method, properties, body):
            print('Received from PI: {}'.format(body))
            Write_into_CSV(body)


        channel.basic_consume(queue='MegDeep.temperature', on_message_callback=callback, auto_ack=True)

        print('Waiting for Messages from PI')

        channel.start_consuming()

    
receiver_PC = Receiver_PC()     
if __name__=='__main__':
    print ('Program is starting ... ')

    receiver_PC.run()
    
    sys.exit(0)