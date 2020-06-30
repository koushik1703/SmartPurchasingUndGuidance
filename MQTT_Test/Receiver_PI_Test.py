import pika
import sys
import time

class Receiver_PI:
    def run(self):
    
        credentials = pika.PlainCredentials('the_user', 'the_pass')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.2', 5672 ,'/', credentials))

        channel = connection.channel()

        channel.exchange_declare(exchange='Processed.topic',exchange_type='topic', durable=True, auto_delete=False)

        channel.queue_declare(queue='Processed.Data')

        channel.queue_bind(queue='Processed.Data', exchange='Processed.topic', routing_key='Processed_Data')
    
        Data_Copy =  open('Data_PI.csv', 'w')
    
        Data_Copy.write("Date;Humidity_Value_Processed;Humidity_Value_Processed;\n")
        
        def Write_into_CSV(body):
            x = format(body).split("%")
            Data_Copy =  open('Data_PI.csv', 'a')
            Temp = float(x[1])
            Humidity = float(x[3])
            Data_Copy.write("%s;"%time.ctime())
            Data_Copy.write("%f;"%Temp)
            Data_Copy.write("%f;\n"%Humidity)
            Data_Copy.close()
    
        def callback(ch, method, properties, body):
            print('Received from PC: {}'.format(body))
            Write_into_CSV(body)


        channel.basic_consume(queue='Processed.Data', on_message_callback=callback, auto_ack=True)

        print('Waiting for Messages from PC')

        channel.start_consuming()

    
receiver_PI = Receiver_PI()     
if __name__=='__main__':
    print ('Program is starting ... ')

    receiver_PI.run()
    
    sys.exit(0)