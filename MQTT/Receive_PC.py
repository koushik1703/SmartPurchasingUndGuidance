import pika
import sys
import time
from Server_PC1 import *

class Receiver_PC:

    def run(self):
    
        self.Server_PC1=Server_PC1() 

        credentials = pika.PlainCredentials('newuser1', 'password')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 5672 ,'/', credentials))

        channel = connection.channel()

        channel.exchange_declare(exchange='Pi2PC.topic',exchange_type='topic', durable=True, auto_delete=False)

        channel.queue_declare(queue='Pi2PC.Raw_Data')

        channel.queue_bind(queue='Pi2PC.Raw_Data', exchange='Pi2PC.topic', routing_key='Cart101.ShoppingMall.*')

        Data_Copy =  open('Data_Rec_Pi.csv', 'w')
        
        Data_Copy.write("Date;Distance to Obstacle;IR Sensor Left;IR Sensor Middle;IR Sensor Right;\n")
    
        def Write_into_CSV(body):
            x = format(body).split("%")
            Data_Copy =  open('Data_Rec_Pi.csv', 'a')
            Distance = int(x[1])
            IR_Left = int(x[3])
            IR_Mid = int(x[5])
            IR_Right = int(x[7])
            self.Server_PC1.Reply_From_PC(Distance,IR_Left,IR_Mid,IR_Right)
            Data_Copy.write("%s;"%time.ctime())
            Data_Copy.write("%d;"%Distance)
            Data_Copy.write("%d;"%IR_Left)
            Data_Copy.write("%d;"%IR_Mid)
            Data_Copy.write("%d;\n"%IR_Right)
            Data_Copy.close()
    
        def callback(ch, method, properties, body):
            print('Received: {}'.format(body))
            Write_into_CSV(body)
    

        channel.basic_consume(queue='Pi2PC.Raw_Data', on_message_callback=callback, auto_ack=True)

        print('Waiting for Messages from PI')

        channel.start_consuming()
    
    
receiver_PC = Receiver_PC() 
if __name__=='__main__':

    print ('Program is running on PC ... ')

    receiver_PC.run()
    
    sys.exit(0)