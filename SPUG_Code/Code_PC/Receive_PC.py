import pika
import sys
import time
from Working import *
from firebase import firebase
import datetime


# Create the connection to our Firebase database - don't forget to change the URL!
FBConn = firebase.FirebaseApplication('https://spug-ca0fe.firebaseio.com/', None)

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
        
        self.Server_PC1.Initialize_Values()
    
        def Write_into_CSV(body):
            x = format(body).split("%")
            Data_Copy =  open('Data_Rec_Pi.csv', 'a')
            Distance = int(x[1])
            IR_Left = int(x[3])
            IR_Mid = int(x[5])
            IR_Right = int(x[7])
            self.Server_PC1.Reply_From_PC(Distance,IR_Left,IR_Mid,IR_Right)
            Data_Copy.write("%s;%d;%d;%d;%d;\n"%(time.ctime(),Distance,IR_Left,IR_Mid,IR_Right))
            Data_Copy.close()
            
            # Create a dictionary to store the data before sending to the database
            data_to_upload = {
               'Time' : time.ctime(),
               'Distance' :  Distance,
               'IR_Left' :   IR_Left,
               'IR_Mid' :   IR_Mid, 
               'IR_Right' :   IR_Right               
            }
            #Post the data to the appropriate folder/branch within your database
            result = FBConn.post('/SPUG_PI2PC_Data/',data_to_upload)
            
            
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