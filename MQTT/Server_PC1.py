import time
import pika
import numpy as np
import sys

Stop = 0
Take_Left = 0
Take_Right = 0
X_Coor = 0
Y_Coor = 0
Prev_Turn = 0

class Server_PC1:
    def Reply_From_PC(self,Distance, IR_Left, IR_Mid, IR_Right):
    
        self.Move = 0
        
        self.Node_Passed = 0

        credentials = pika.PlainCredentials('newuser1', 'password')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 5672, '/', credentials))

        channel = connection.channel()

        channel.queue_declare(queue='PC2Pi.Processed_Data')

        channel.exchange_declare(exchange='PC2Pi.topic', exchange_type='topic', durable = True, auto_delete = False)
        
        if(Distance > 25.0):
            if((IR_Left == 0) and (IR_Mid == 1) and (IR_Right == 0)):
                self.Move = 5 #Move Forward
                
            elif((IR_Left == 1) and (IR_Mid == 0) and (IR_Right == 0)):
                self.Move = 3 #Take Slight Left
                
            elif((IR_Left == 1) and (IR_Mid == 1) and (IR_Right == 0)):
                self.Node_Passed = self.Node_Passed + 1
                if(Take_Left):
                    self.Move = 1 #Take Fast Left
                else:
                    self.Move = 5 #Move Forward
               
            elif((IR_Left == 0) and (IR_Mid == 0) and (IR_Right == 1)):
                self.Move = 7 #Take Slight Right
                
            elif((IR_Left == 0) and (IR_Mid == 1) and (IR_Right == 1)):
                self.Node_Passed = self.Node_Passed + 1
                if(Take_Right):
                    self.Move = 9 #Take Fast Right
                else:
                    self.Move = 5 #Move Forward
                
            elif((IR_Mid == 1) and (IR_Left == 1) and (IR_Right == 1)):
                self.Node_Passed = self.Node_Passed + 1
                if(Stop):
                    self.Move = 0 #Take Fast Right
                elif(Take_Left):
                    self.Move = 1 #Take Fast Right
                elif(Take_Right):
                    self.Move = 9 #Take Fast Right
                else:
                    self.Move = 5 #Move Forward
                    
            else:
                pass
                    
                    
        else:
        
            self.Move = 0 #Stop Movement
            
        msg = time.ctime() + " Movement: %" + str(self.Move) + "%"    
    
        channel.basic_publish(exchange = 'PC2Pi.topic', routing_key = 'Processed_Data', body = msg)
	
        print('Sent from PC: ' + msg)
        
    def run(self):
        print ('Program is running on PC ... ')
        #Initialize the values
        self.Node_Passed = 0
            
            
server_pc = Server_PC1()      
if __name__=='__main__':

    server_pc.run()
    
    sys.exit(0)
	