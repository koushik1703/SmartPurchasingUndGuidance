
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

#-----------------------IR Sesor Initilaization---------------------------------
IR01 = 14
IR02 = 15
IR03 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR01,GPIO.IN)
GPIO.setup(IR02,GPIO.IN)
GPIO.setup(IR03,GPIO.IN)

#----------------Main Class---------------------------------------

class SPUG:

    def Initialize_Values(self):
        #Itial position 
        self.x_init = 0
        self.y_init = 0
    
        #Destination Position
        self.x_des = 3
        self.y_des = 3

        #Intemediate Position
        self.l_x = 0
        self.l_y = 0
    
        self.Orientation = "North"
        
        self.Cart_Number = "Cart_12"
    
        self.Moved_Straight_New = 0
        self.Moved_Straight_Old = 0
    
        self.Moved_Left_New = 0
        self.Moved_Left_Old = 0
    
        self.Moved_Right_New = 0
        self.Moved_Right_Old = 0
    
        self.Total_Moves = 0
        self.Target_Reached = 0
        
        self.Junction = 0
        
        self.IntialJunction = 0

    def Set_destnation_position(self,x_destination,y_destnation):
        self.x_des = x_destination
        self.y_des = y_destnation
        
        self.Target_Reached = 0
        
    def Get_curent_position(self):
        return self.l_x, self.l_y
        
    def Is_DestinTion_Reached(self):
        return self.Target_Reached
    
    def Mov_According_To_Specified_position(self): 

        self.x_init = self.l_x   
        self.y_init = self.l_y
          
        #Do not update the coordinates for the first junction           
        if(self.IntialJunction != 0):
            
            Coordinates_Updated = 0
                
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
                    
                Coordinates_Updated = 1
                                
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
                    
                Coordinates_Updated = 1
                
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
                    
                Coordinates_Updated = 1
         
         
            if(Coordinates_Updated != 0):
                self.Total_Moves = self.Total_Moves + 1
                
            self.Moved_Straight_New = self.Moved_Straight_Old
            self.Moved_Left_New = self.Moved_Left_Old
            self.Moved_Right_New = self.Moved_Right_Old
                
          
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
                ret = 0 #Stop
                
                    
        elif(self.Orientation == "East"):
        
            if((self.x_des - self.l_x) > 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.y_des - self.l_y) < 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.y_des - self.l_y) > 0):
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
                ret = 0 #Stop
                
        #Set the inital junction value to 1        
        self.IntialJunction = 1
            
        #Update if the target is reached         
        if((self.y_des == self.l_y) and (self.x_des == self.l_x)):
            self.Target_Reached = 1
        else:
            self.Target_Reached = 0
        
        print("Orientation - %s"%self.Orientation)
        print("X Coordinate - %d "%self.l_x)
        print("Y Coordinate - %d "%self.l_y)
        print("Destination Reached - %d "%self.Target_Reached)
        print("Total Moves - %d "%self.Total_Moves)
        
        #----------------------------------------Send MQTT Message----------------------------------------------------------------------
        credentials = pika.PlainCredentials('newuser1', 'password')

        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 5672 ,'/', credentials))

        channel = connection.channel()
        
        channel.exchange_declare(exchange='pathOccupy.topic',exchange_type='topic', durable=True, auto_delete=False)

        channel.queue_declare(queue='pathOccupy.Coordinates.Cart12')

        channel.queue_bind(queue='pathOccupy.Coordinates.Cart12', exchange='pathOccupy.topic', routing_key='Current_Coordinates.Cart12')
            
        msg1 = time.ctime() \
                  + "fromx"+ "%" + str(self.l_x) + "%" \
                  + "fromy"+ "%" + str(self.l_y) + "%" \
                  + "tox"  + "%" + str(self.x_des) + "%" \
                  + "toy"  + "%" + str(self.y_des) + "%"  
    
        channel.basic_publish(exchange = 'pathOccupy.topic', routing_key = 'Path_Occupy_Coordinates.Cart12', body = msg1)
            
            
        print("Occupy message Sent from Pi :" +msg1)
        #---------------------------------------------------------------------------------------------------------------------                    
        
        #Return Value from the Calculations        
        return int(ret)
        
    def Move_Cart(self,l_Movement_Type):
        
        if(l_Movement_Type == 5):
            PWM.setMotorModel(600,600,600,600)
                    
        elif(l_Movement_Type == 1):
            PWM.setMotorModel(-2000,-2000,4000,4000)
                    
        elif(l_Movement_Type == 3):
            PWM.setMotorModel(-1200,-1200,2000,2000)
                    
        elif(l_Movement_Type == 7):
            PWM.setMotorModel(2000,2000,-1200,-1200)
                    
        elif(l_Movement_Type == 9):
            PWM.setMotorModel(4000,4000,-2000,-2000)
                    
        elif(l_Movement_Type == 0):
            PWM.setMotorModel(0,0,0,0)
        
    def Run_Cart12(self):
    
        #------------------------------------------Ultrasonic sensor and Servo Motor Class
        self.Ultrasonic=Ultrasonic()
        
        self.Pwm=Servo()
        
        self.Junction = 0

        #--------------------------------------------------------------------------------------
        while True:
        
            self.Movement_Type = 0
        
            Distance = self.Ultrasonic.get_distance()
            
            IR_Left = GPIO.input(IR01)
            
            IR_Mid = GPIO.input(IR02)
            
            IR_Right = GPIO.input(IR03)
        
        
            if(Distance > 25.0):
                if((IR_Left == 0) and (IR_Mid == 1) and (IR_Right == 0)):
                    self.Movement_Type = 5 #Move Forward
                    self.Junction = 0 #Clear the Junction Variable
                
                elif((IR_Left == 1) and (IR_Mid == 0) and (IR_Right == 0)):
                    self.Movement_Type = 3 #Take Slight Left
                
                elif((IR_Left == 1) and (IR_Mid == 1) and (IR_Right == 0)):
                    self.Movement_Type = 3 #Take Slight Left
               
                elif((IR_Left == 0) and (IR_Mid == 0) and (IR_Right == 1)):
                    self.Movement_Type = 7 #Take Slight Right
                
                elif((IR_Left == 0) and (IR_Mid == 1) and (IR_Right == 1)):
                    self.Movement_Type = 7 #Take Slight Right
                
                elif((IR_Mid == 1) and (IR_Left == 1) and (IR_Right == 1)):
                    if(self.Junction == 0):
                        self.Movement_Type = self.Mov_According_To_Specified_position()
                    self.Junction = 1
     
                else:
                    pass         
                    
            else:
                self.Movement_Type = 0 #Stop Movement

            #Actuate the motors to move cart to the specific Coordinate
            self.Move_Cart(self.Movement_Type)
            
            
            if(self.Is_DestinTion_Reached()):
                #--------------------------------------MQTT Communication Parameters--------------------------------------
                credentials = pika.PlainCredentials('newuser1', 'password')

                connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.12', 5672 ,'/', credentials))

                channel = connection.channel()
                
                channel.exchange_declare(exchange='pathUnoccupy.topic',exchange_type='topic', durable=True, auto_delete=False)

                channel.queue_declare(queue='pathUnoccupy.Coordinates.Cart12')

                channel.queue_bind(queue='pathUnoccupy.Coordinates.Cart12', exchange='pathUnoccupy.topic', routing_key='Current_Coordinates.Cart12')
            
                msg2 = time.ctime() \
                          + "fromx"+ "%" + str(self.x_init) + "%" \
                          + "fromy"+ "%" + str(self.y_init) + "%" \
                          + "tox"  + "%" + str(self.x_des) + "%" \
                          + "toy"  + "%" + str(self.y_des) + "%"  
    
                channel.basic_publish(exchange = 'pathUnoccupy.topic', routing_key = 'Path_Occupy_Coordinates.Cart12', body = msg2)
            
                print("Un Occupy Message Sent from Pi :" +msg2)
                #--------------------------------------------------------------------------------------------------------------------- 
                break
            
            time.sleep(0.2)
        
l_spug=SPUG()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    
    try:
        l_spug.Initialize_Values()
        l_spug.Run_Cart12()
        
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)

