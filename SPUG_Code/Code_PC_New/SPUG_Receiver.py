import pika
import sys
import time
from firebase import firebase
import datetime


# Create the connection to our Firebase database - don't forget to change the URL!
FBConn = firebase.FirebaseApplication('https://spug-ca0fe.firebaseio.com/', None)

class Receiver_PC:

    def run(self):

        credentials = pika.PlainCredentials('newuser1', 'password')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 5672 ,'/', credentials))

        channel = connection.channel()

        channel.exchange_declare(exchange='Pi2PC.topic',exchange_type='topic', durable=True, auto_delete=False)

        channel.queue_declare(queue='Pi2PC.Coordinates.Cart12')

        channel.queue_bind(queue='Pi2PC.Coordinates.Cart12', exchange='Pi2PC.topic', routing_key='Current_Coordinates.Cart12')

        Data_Copy =  open('Coordinates_Data_Recieved_From_Pi.csv', 'w')
        
        Data_Copy.write("Date;Current X Coordinate;Current Y Coordinate; \
                                               Destination X Coordinate;Destination X Coordinate;\
                                               Movement;Orientation;Destination Reached;Total Moves\n")
    
        def Write_into_CSV(body):
            x = format(body).split("%")
            Data_Copy =  open('Data_Rec_Pi.csv', 'a')
            Cur_X = int(x[1])
            Cur_Y = int(x[3])
            Des_X = int(x[5])
            Des_Y = int(x[7])
            Mov = int(x[9])
            Ori = x[11]
            Des_Rec = int(x[13])
            Moves = int(x[15])
            Data_Copy.write("%s;%d;%d;%d;%d;%d;%s;%d;%d\n"%(time.ctime(),Cur_X,Cur_Y,Des_X,Des_Y,Mov,Ori,Des_Rec,Moves))
            Data_Copy.close()
            
            # Create a dictionary to store the data before sending to the database
            data_to_upload = {
               'Time' : time.ctime(),
               'Current X Coordinate'     : Cur_X,
               'Current Y Coordinate'     : Cur_Y,
               'Destination X Coordinate' : Des_X, 
               'Destination Y Coordinate' : Des_Y, 
               'Movement'                 : Mov,   
               'Orientation'              : Ori,
               'Destination Reached'      : Des_Rec,
               'Total Moves'              : Moves 
            }
            #Post the data to the appropriate folder/branch within your database
            result = FBConn.post('/SPUG_PI2PC_Coordinates_Data/',data_to_upload)
            
            
        def callback(ch, method, properties, body):
            print('Received: {}'.format(body))
            Write_into_CSV(body)
    

        channel.basic_consume(queue='Pi2PC.Coordinates.Cart12', on_message_callback=callback, auto_ack=True)

        print('Waiting for Messages from PI')

        channel.start_consuming()
    
    
receiver_PC = Receiver_PC() 
if __name__=='__main__':

    print ('Program is running on PC ... ')

    receiver_PC.run()
    
    sys.exit(0)