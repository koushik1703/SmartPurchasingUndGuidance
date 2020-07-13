import time
from Motor import *
from Ultrasonic import *
from Buzzer import *
import RPi.GPIO as GPIO
from Led import *
from PCA9685 import PCA9685
import json
import paho.mqtt.client as mqtt #import the client1

#Google Firebase Requirements
from firebase import firebase
import datetime

#MQTT Communication Requirements
import time
import numpy as np

#-----------------------IR Sesor Initilaization---------------------------------
IR01 = 14
IR02 = 15
IR03 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR01,GPIO.IN)
GPIO.setup(IR02,GPIO.IN)
GPIO.setup(IR03,GPIO.IN)

#--------------------------Google Firebase link
# Create the connection to our Firebase database - don't forget to change the URL!
FBConn = firebase.FirebaseApplication('https://spug-ca0fe.firebaseio.com/', None)

#----------------Main Class---------------------------------------

class SPUG:

    def Initialize_Values(self):
        
        #Itial position 
        self.x_init = 0
        self.y_init = 0
    
        #Product Location Positions
        self.x_pro_des = 3   #Test Initialization
        self.y_pro_des = 3   #Test Initialization
        
        #Intermediate Destination Positions
        self.x_inter_des = 3  #Test Initialization
        self.y_inter_des = 3  #Test Initialization

        #Local Position of the SPUG
        self.l_x = 0
        self.l_y = 0
    
        #SPUG Starts at Coordinate [0 ,0] facing North
        self.Orientation = "North"
        
        #SPUG Number
        self.Cart_Number = 4
    
        #Variable to calculate the Position of SPUG after movement
        self.Moved_Straight_New = 0
        self.Moved_Straight_Old = 0
        
        self.Moved_Reverse_New = 0
        self.Moved_Reverse_Old = 0
    
        self.Moved_Left_New = 0
        self.Moved_Left_Old = 0
    
        self.Moved_Right_New = 0
        self.Moved_Right_Old = 0
    
        #Total moves made by SPUG
        self.Total_Moves = 0
        
        #Intermediate Position Reached by SPUG
        self.Inter_Target_Reached = 0
        
        #Product Location Reached by SPUG
        self.Product_Des_Reached = 0
        
        #SPUG presesnt at junction
        self.Junction = 0
        
        #SPUG at [0 ,0] coordinate: 
        # 0 - Present at [0,0] coordinate 
        # 1 - Not pressent at [0,0] coordinate
        self.IntialJunction = 0

    #Function to set the intermediate coordinates to navigate SPUG
    def Set_intermediate_destnation_position(self,x_destination,y_destnation):
        self.x_inter_des = x_destination
        self.y_inter_des = y_destnation
        
        self.Inter_Target_Reached = 0

    #Function to set the Product locations to message the server if the product location is reached  
    def Set_product_destnation_position(self,x_destination,y_destnation):
        self.x_pro_des = x_destination
        self.y_pro_des = y_destnation
        
        self.Product_Des_Reached = 0
        
    #Function to get the current coordinates of SPUG
    def Get_curent_position(self):
        return self.l_x, self.l_y
        
    #Function to get if Intermediate position is reached
    def Is_Intermediate_DestinTion_Reached(self):
        return self.Inter_Target_Reached

    #Function to get if Product location is reached
    def Is_Product_DestinTion_Reached(self):
        return self.Product_Des_Reached
    
    #Function to update the coordinates and get the direction to move
    def Mov_According_To_Specified_position(self): 

        #Intial Position Before Movement
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
                                
            elif(self.Moved_Reverse_New != self.Moved_Reverse_Old):
                if(self.Orientation == "North"):
                    self.l_x = self.l_x
                    self.l_y = self.l_y - 1
                
                elif(self.Orientation == "South"):
                    self.l_x = self.l_x
                    self.l_y = self.l_y + 1
                
                elif(self.Orientation == "East"):
                    self.l_x = self.l_x - 1
                    self.l_y = self.l_y
                
                elif(self.Orientation == "West"):
                    self.l_x = self.l_x + 1
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
            self.Moved_Reverse_New = self.Moved_Reverse_Old
            self.Moved_Left_New = self.Moved_Left_Old
            self.Moved_Right_New = self.Moved_Right_Old
                
          
        #Calculate the next move  
        if(self.Orientation == "North"):    
            if((self.y_inter_des - self.l_y) > 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.x_inter_des - self.l_x) > 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.x_inter_des - self.l_x) < 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.y_inter_des - self.l_y) < 0):
                self.Moved_Reverse_New = self.Moved_Reverse_Old + 1
                ret = 11 #Reverse

            elif((self.y_inter_des == self.l_y) and (self.x_inter_des == self.l_x)):
                ret = 0 #Stop
                    
                    
        elif(self.Orientation == "South"):  
            if((self.y_inter_des - self.l_y) < 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.x_inter_des - self.l_x) < 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.x_inter_des - self.l_x) > 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.y_inter_des - self.l_y) > 0):
                self.Moved_Reverse_New = self.Moved_Reverse_Old + 1
                ret = 11 #Reverse
                    
            elif((self.y_inter_des == self.l_y) and (self.x_inter_des == self.l_x)):
                ret = 0 #Stop
                
                    
        elif(self.Orientation == "East"):  
            if((self.x_inter_des - self.l_x) > 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.y_inter_des - self.l_y) < 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.y_inter_des - self.l_y) > 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.x_inter_des - self.l_x) < 0):
                self.Moved_Reverse_New = self.Moved_Reverse_Old + 1
                ret = 11 #Reverse
                    
            elif((self.y_inter_des == self.l_y) and (self.x_inter_des == self.l_x)):
                ret = 0 #Stop
                
                    
        elif(self.Orientation == "West"): 
            if((self.x_inter_des - self.l_x) < 0):
                self.Moved_Straight_New = self.Moved_Straight_Old + 1
                ret = 5 #Straight
                
            elif((self.y_inter_des - self.l_y) > 0):
                self.Moved_Right_New = self.Moved_Right_Old + 1
                ret = 9 #Right
                
            elif((self.y_inter_des - self.l_y) < 0):
                self.Moved_Left_New = self.Moved_Left_Old + 1
                ret = 1 #Left
                
            elif((self.x_inter_des - self.l_x) > 0):
                self.Moved_Reverse_New = self.Moved_Reverse_Old + 1
                ret = 11 #Reverse
            
            elif((self.y_inter_des == self.l_y) and (self.x_inter_des == self.l_x)):
                ret = 0 #Stop
                
        #Set the inital junction value to 1        
        self.IntialJunction = 1
            
        #Update if the intermediate position is reached         
        if((self.y_inter_des == self.l_y) and (self.x_inter_des == self.l_x)):
            self.Inter_Target_Reached = 1
        else:
            self.Inter_Target_Reached = 0
            
        #Update if the product location coordinate is reached         
        if((self.y_pro_des == self.l_y) and (self.x_pro_des == self.l_x)):
            self.Product_Des_Reached = 1
        else:
            self.Product_Des_Reached = 0
        #------------------------------------------------------------------------------------------------------------------------
        
        #--------------------Print data for debugging-------------------------------------------------------------------------
        print("Orientation - %s"%self.Orientation)
        print("X Coordinate - %d "%self.l_x)
        print("Y Coordinate - %d "%self.l_y)
        print("Intermediate Destination Reached - %d "%self.Inter_Target_Reached)
        print("Product Destination Reached - %d "%self.Product_Des_Reached)
        print("Total Moves - %d "%self.Total_Moves)
        #------------------------------------------------------------------------------------------------------------------------
        
        #----------------------Write data into Google Firebase Cloud Database-------------------------------------------------
        # Create a dictionary to store the data before sending to the database
        data_to_upload = {
           'Time' : time.ctime(),
           'Current X Coordinate'     : self.l_x,
           'Current Y Coordinate'     : self.l_y,
           'Intermed Destination X'   : self.x_inter_des, 
           'Intermed Destination Y'   : self.y_inter_des, 
           'Product Destination X'    : self.x_pro_des, 
           'Product Destination Y'    : self.y_pro_des, 
           'Movement'                 : ret,   
           'Orientation'              : self.Orientation,
           'Intermed Destination Reached': self.Inter_Target_Reached,
           'Product Destination Reached': self.Product_Des_Reached,
           'Total Moves'              : self.Total_Moves 
            }
        #Post the data to the appropriate folder/branch within your database
        result = FBConn.post('/Cart4/SPUG_PI2PC_Coordinates_Data/',data_to_upload)
        #------------------------------------------------------------------------------------------------------------------------
        
        #----------------------------------------Send MQTT Path Occupy Message-------------------------------------------------
        client = mqtt.Client("RaspBerry_PI_1") #create new instance
        
        client.connect('192.168.1.9', 1883, 70) #connect to broker
        
        client.loop_start()
            
        message1 = {"X" : str(self.x_inter_des), "Y" : str(str(self.y_inter_des))}    
            
        msg1 = json.dumps(message1)
        
        client.publish("pointOccupy/",msg1, 2)
        
        time.sleep(0.1)
            
        print("Point Occupy message Sent from Pi :" +time.ctime() +" " +msg1)
        #------------------------------------------------------------------------------------------------------------------------

        #----------------------------------------Send MQTT Path Un-Occupy Message-------------------------------------------------
        if(self.Is_Intermediate_DestinTion_Reached()):             
            client = mqtt.Client("RaspBerry_PI_2") #create new instance
        
            client.connect('192.168.1.9', 1883, 70) #connect to broker
        
            client.loop_start()
            
            message2 = { "X" : str(self.x_inter_des), "Y" : str(str(self.y_inter_des))}   
            
            msg2 = json.dumps(message2)
        
            client.publish("pointUnoccupy/",msg2, 2)
            
            time.sleep(0.1)
            
            print("Point Un-Occupy message Sent from Pi :" +time.ctime() +" " +msg2)
        #------------------------------------------------------------------------------------------------------------------------- 
        
        #----------------------------------------Send MQTT Item Purchased Message-------------------------------------------------
        if(self.Is_Product_DestinTion_Reached()):
            client = mqtt.Client("RaspBerry_PI_3") #create new instance
        
            client.connect('192.168.1.9', 1883, 70) #connect to broker
        
            client.loop_start()
            
            message3 = { "itemPurchasedX" : str(self.l_x), "itemPurchasedY" : str(self.l_y), \
                         "cartName" : "cart"+str(self.Cart_Number)}    
            
            msg3 = json.dumps(message3)
        
            client.publish("item/",msg3, 2)
            
            time.sleep(0.1)
            
            print("Item Purchased message Sent from Pi :" +time.ctime() +" " +msg3)
            
            self.LED.ledIndex(0xFF,0,0,0) # Switch off all LED's
            self.Buzzer.run('1')
            time.sleep(0.5)
            self.Buzzer.run('0')
        #---------------------------------------------------------------------------------------------------------------------         
        
        #Return Value from the Calculations        
        return int(ret)
        
    def Move_Cart(self,l_Movement_Type):
        
        if(l_Movement_Type == 5):
            self.LED.ledIndex(0xFF,0,0,0)        #Turn Off
            self.LED.ledIndex(0xF0,0,255,0)      #Green
            #PWM.setMotorModel(800,800,800,800)
            #time.sleep(0.1)
            #PWM.setMotorModel(0,0,0,0)
                    
        elif(l_Movement_Type == 1):
            self.LED.ledIndex(0xFF,0,0,0)        #Turn Off
            self.LED.ledIndex(0x3C,0,255,0)      #Green
            #PWM.setMotorModel(-2000,-2000,4000,4000)
            #time.sleep(0.2)
                    
        elif(l_Movement_Type == 3):
            self.LED.ledIndex(0xFF,0,0,0)        #Turn Off
            self.LED.ledIndex(0x3C,0,0,0)      #Green
            #PWM.setMotorModel(-1200,-1200,2000,2000)
            #time.sleep(0.2)
                    
        elif(l_Movement_Type == 7):
            self.LED.ledIndex(0xFF,0,0,0)        #Turn Off
            self.LED.ledIndex(0xC3,0,0,0)      #Green
            #PWM.setMotorModel(2000,2000,-1200,-1200)
            #time.sleep(0.2)
                    
        elif(l_Movement_Type == 9):
            self.LED.ledIndex(0xFF,0,0,0)        #Turn Off
            self.LED.ledIndex(0xC3,0,255,0)      #Green
            #PWM.setMotorModel(4000,4000,-2000,-2000)
            #time.sleep(0.5)
            
        elif(l_Movement_Type == 11):
            self.LED.ledIndex(0xFF,0,0,0)        #Turn Off
            self.LED.ledIndex(0x0F,0,255,0)      #Green
            #PWM.setMotorModel(-600,-600,-600,-600)
                    
        elif(l_Movement_Type == 0):
            time.sleep(0.001)
            #PWM.setMotorModel(0,0,0,0)
        
    def Run_Cart4(self):
    
        #------------------------------------------Ultrasonic sensor and Servo Motor Class
        self.Ultrasonic=Ultrasonic()
        
        self.LED=Led()
        
        self.Buzzer=Buzzer()
        
        self.Junction = 0

        #--------------------------------------------------------------------------------------
        while True:
        
            self.Movement_Type = 0
        
            Distance = self.Ultrasonic.get_distance()
            
            IR_Left = GPIO.input(IR01)
            
            IR_Mid = GPIO.input(IR02)
            
            IR_Right = GPIO.input(IR03)
        
        
            if(Distance > 5.0):
                
                if((IR_Left == 0) and (IR_Mid == 1) and (IR_Right == 0)):
                    if(self.Moved_Reverse_New != self.Moved_Reverse_Old):
                        self.Movement_Type = 11 #Move Reverse
                    else:
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
                self.LED.ledIndex(0x20,255,125,0)      #Orange
                self.LED.ledIndex(0x40,255,125,0)      #Orange
                time.sleep(1)
                self.LED.ledIndex(0x60,0,0,0)

            #Actuate the motors to move cart to the specific Coordinate
            self.Move_Cart(self.Movement_Type)
            
            
            if(self.Is_Intermediate_DestinTion_Reached()):
                break
        
l_spug=SPUG()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    
    try:
        l_spug.Initialize_Values()
        l_spug.Run_Cart4()
        
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)

