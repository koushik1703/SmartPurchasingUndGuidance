import time
import pika
import numpy as np
import sys

class Server_PC1:

    def Initialize_Values(self):
        #Itial position 
        self.x_init = 0
        self.y_init = 0
    
        #Destination Position
        self.x_des = 3
        self.y_des = 3

        #Intemediate Position
        self.l_x = self.x_init
        self.l_y = self.y_init
    
        self.Orientation = "North"
    
        self.Moved_Straight_New = 0
        self.Moved_Straight_Old = 0
    
        self.Moved_Left_New = 0
        self.Moved_Left_Old = 0
    
        self.Moved_Right_New = 0
        self.Moved_Right_Old = 0
    
        self.Total_Moves = 0
        self.Target_Reached = 0
        
        self.Junction = 0

    def Set_destnation_position(self,x_destination,y_destnation):
        self.x_des = x_destination
        self.y_des = y_destnation
    
    def Mov_According_To_Specified_position(self):       
            
        if(self.Orientation == "North"):
        
            if((self.y_des - self.l_y) > 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.x_des - self.l_x) > 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.x_des - self.l_x) < 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.y_des - self.l_y) < 0):
                if(self.l_x > 0):
                    self.Moved_Left_New = self.Moved_Left_Old + 1
                    ret = 1 #Left
                else:
                    self.Moved_Right_New = Moved_Righ_Old + 1
                    ret = 9 #Right
                    
            elif((self.y_des == self.l_y) and (self.x_des == self.l_x)):
                self.Target_Reached = 1
                ret = 0 #Stop
                    
                    
        elif(self.Orientation == "South"):
        
            if((self.y_des - self.l_y) < 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.x_des - self.l_x) < 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.x_des - self.l_x) > 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.y_des - self.l_y) > 0):
                if(self.l_x > 0):
                    self.Moved_Right_New = self.Moved_Right_Old + 1
                    ret = 9 #Left
                else:
                    self.Moved_Left_New = self.Moved_Left_Old + 1
                    ret = 9 #Right 
                    
            elif((self.y_des == self.l_y) and (self.x_des == self.l_x)):
                self.Target_Reached = 1
                ret = 0 #Stop
                
                    
        elif(self.Orientation == "East"):
        
            if((self.x_des - self.l_x) > 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.y_des - self.l_y) > 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.y_des - self.l_y) < 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.x_des - self.l_x) < 0):
                if(self.l_y > 0):
                    self.Moved_Left_New = self.Moved_Left_Old + 1
                    ret = 1 #Left
                else:
                    self.Moved_Right_New = Moved_Righ_Old + 1
                    ret = 9 #Right 
                    
            elif((self.y_des == self.l_y) and (self.x_des == self.l_x)):
                self.Target_Reached = 1
                ret = 0 #Stop
                
                    
        elif(self.Orientation == "West"):
        
            if((self.x_des - self.l_x) < 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.y_des - self.l_y) > 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.y_des - self.l_y) < 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.x_des - self.l_x) > 0):
                if(self.l_y > 0):
                    self.Moved_Right_New = self.Moved_Right_Old + 1
                    ret = 1 #Left
                else:
                    self.Moved_Left_New = self.Moved_Left_Old + 1
                    ret = 9 #Right 
            
            elif((self.y_des == self.l_y) and (self.x_des == self.l_x)):
                self.Target_Reached = 1
                ret = 0 #Stop
                
                
                
        #Code for updating the co-ordinates        
        if(self.Moved_Straight_New != self.Moved_Straight_Old):
            if(self.Orientation == "North"):
                self.l_x = self.l_x
                self.l_y = self.l_y + 1
                
            elif(self.Orientation == "South"):
                self.l_x = self.l_x
                self.l_y = self.l_y - 1
                
            elif(self.Orientation == "East"):
                self.l_x = self.l_x + 1
                self.l_y = self.l_y
                
            elif(self.Orientation == "West"):
                self.l_x = self.l_x - 1
                self.l_y = self.l_y
                
                
        elif(self.Moved_Left_New != self.Moved_Left_Old):
            if(self.Orientation == "North"):
                self.l_x = self.l_x - 1
                self.l_y = self.l_y
                self.Orientation = 'West'
                
            elif(self.Orientation == "South"):
                self.l_x = self.l_x + 1
                self.l_y = self.l_y
                self.Orientation = 'East'
                
            elif(self.Orientation == "East"):
                self.l_x = self.l_x
                self.l_y = self.l_y + 1
                self.Orientation = 'North'
                
            elif(self.Orientation == "West"):
                self.l_x = self.l_x
                self.l_y = self.l_y - 1
                self.Orientation = 'South'
                
        elif(self.Moved_Right_New != self.Moved_Right_Old):
            if(self.Orientation == "North"):
                self.l_x = self.l_x + 1
                self.l_y = self.l_y
                self.Orientation = 'East'
                
            elif(self.Orientation == "South"):
                self.l_x = self.l_x - 1
                self.l_y = self.l_y
                self.Orientation = 'West'
                
            elif(self.Orientation == "East"):
                self.l_x = self.l_x
                self.l_y = self.l_y - 1
                self.Orientation = 'South'
                
            elif(self.Orientation == "West"):
                self.l_x = self.l_x
                self.l_y = self.l_y + 1
                self.Orientation = 'North'
                
        self.Moved_Straight_New = self.Moved_Straight_Old
        self.Moved_Left_New = self.Moved_Left_Old
        self.Moved_Right_New = self.Moved_Right_Old
        
        if(ret != 0):
            self.Total_Moves = self.Total_Moves + 1
        
        print("Orientation - %s"%self.Orientation)
        print("X Coordinate - %d "%self.l_x)
        print("Y Coordinate - %d "%self.l_y)
        print("Total Moves - %d "%self.Total_Moves)
        
        #Return Value from the Calculations        
        return int(ret)
    
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
                self.Junction = 0 #Clear the Junction Variable
                
            elif((IR_Left == 1) and (IR_Mid == 0) and (IR_Right == 0)):
                self.Move = 3 #Take Slight Left
                
            elif((IR_Left == 1) and (IR_Mid == 1) and (IR_Right == 0)):
                self.Move = 3 #Take Slight Left
               
            elif((IR_Left == 0) and (IR_Mid == 0) and (IR_Right == 1)):
                self.Move = 7 #Take Slight Right
                
            elif((IR_Left == 0) and (IR_Mid == 1) and (IR_Right == 1)):
                self.Move = 7 #Take Slight Right
                
            elif((IR_Mid == 1) and (IR_Left == 1) and (IR_Right == 1)):
                if(self.Junction == 0):
                    self.Move = self.Mov_According_To_Specified_position()
                self.Junction = 1
     
            else:
                pass         
                    
        else:
        
            self.Move = 0 #Stop Movement
            
        msg = time.ctime() + " Movement: %" + str(self.Move) + "%" + " Orientation: %" + str(self.Move) + "%"\
                           + " X Coordinate: %" + str(self.l_x) + "%" \
                           + " Y Coordinate: %" + str(self.l_y) + "%" \
                           + " Total Moves: %" + str(self.Total_Moves) + "%"	
    
        channel.basic_publish(exchange = 'PC2Pi.topic', routing_key = 'Processed_Data', body = msg)
        
        #print('Sent from PC: ' + msg)
        
    def run(self):
        print ('Program is running on PC ... ')
        #Initialize the values
        self.Node_Passed = 0
            
            
server_pc = Server_PC1()      
if __name__=='__main__':

    server_pc.run()
    
    sys.exit(0)