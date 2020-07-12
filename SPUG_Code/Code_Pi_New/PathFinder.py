from itertools import permutations
import json
import paho.mqtt.client as mqtt

from PDDL_Generator import *
from SPUG_Run import *

class Shortest_Path:

    def Distance(self, point1, point2):
        return (abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]))
        #return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

    def Total_distance(self, points):
        l_TotalDistance = sum([self.Distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])
        Dist_To_Origin = self.Distance(points[0],points[-1])
        return (l_TotalDistance + Dist_To_Origin)

    def Travelling_salesman(self, points, start=None):
        if start is None:
            start = points[0]     
        self.tsp_path = min([perm for perm in permutations(points) if perm[0] == start], key=self.Total_distance)
        
        return self.tsp_path

    def Optimized_Travelling_salesman(self, points, start=None):
        if start is None:
            start = points[0]
        must_visit = points
        self.opt_tsp_path = [start]
        must_visit.remove(start)
        while must_visit:
            nearest = min(must_visit, key=lambda x: self.Distance(self.opt_tsp_path[-1], x))
            self.opt_tsp_path.append(nearest)
            must_visit.remove(nearest)
        
        return self.opt_tsp_path


    def Main(self):
        
        self.SPUG_Run=SPUG()
        
        self.PDDL_Generator=PDDL_Generator()
        
        Points_New = [[0, 0]]
        
        #---------------------Receive Product location Coordinates as MQTT Message from Server-----------------
        def on_message(client, userdata, message):
            messageJson = json.loads(message.payload.decode())
            x_coor = messageJson["itemX"]
            y_coor = messageJson["itemY"]
            x_coor = int(x_coor)
            y_coor = int(y_coor)
            
            if((x_coor == -1) and (y_coor == -1)):
                print("Received Coordiantes %s"%Points_New)
                client.loop_stop()  #Stop the loop_forever
                client.disconnect() #Disconnect from the loop
                
            else:
                Rec_Point = [x_coor, y_coor]    
                Points_New.append(Rec_Point)
        
        client = mqtt.Client("RaspBerry_PI_Rec1") #create new instance
        
        client.on_message=on_message #attach function to callback

        client.connect('192.168.1.9', 1883, 70) #connect to broker

        client.subscribe("buyItemFromServer/4/", 2)
        
        print("Receiving the coordinates from server")
        
        client.loop_forever() #Loop forever to receive the messages
        
        points =  Points_New  #Points Received from Server
        #-----------------------------------------------------------------------------------------------------
        
        #---------------------Receive Blocking Points from Server---------------------------------------------
        #blocking_points = [(2,1), (0,1), (0,4)] #[[0, 1], [1, 1], [3, 4] ] #Grt the points from the server
        BlockingPoints_New = [ ]
        
        def on_message(client, userdata, message):
            messageJson = json.loads(message.payload.decode())
            x_coor_bp = messageJson["X"]
            y_coor_bp = messageJson["Y"]
            x_coor_bp = int(x_coor_bp)
            y_coor_bp = int(y_coor_bp)
            
            if((x_coor_bp == -1) and (y_coor_bp == -1)):
                print("Received Blocking Points Coordiantes %s"%BlockingPoints_New)
                client.loop_stop()  #Stop the loop_forever
                client.disconnect() #Disconnect from the loop
                
            else:
                Rec_Blocking_Point = [x_coor_bp, y_coor_bp]
                print("Receieved Point %s"%Rec_Blocking_Point)
                if not (Rec_Blocking_Point in Points_New):          #Append a blocking point only if it is not a Product location
                    BlockingPoints_New.append(Rec_Blocking_Point)
        
        client = mqtt.Client("RaspBerry_PI_Rec2") #create new instance
        
        client.on_message=on_message #attach function to callback

        client.connect('192.168.1.9', 1883, 70) #connect to broker

        client.subscribe("pointOccupied/4/", 2)
        
        print("Receiving the blocking point coordinates from server")
        
        client.loop_forever() #Loop forever to receive the messages
        
        blocking_points = BlockingPoints_New
        #-----------------------------------------------------------------------------------------------------
        
        #------------------------Calculate the shortest path using Travveling Salesman Problem----------------
        self.Total_distance(self.Travelling_salesman(points))    
        
        print("Shortest path is : ")
        print(self.tsp_path)
        #-----------------------------------------------------------------------------------------------------
        
        self.SPUG_Run.Initialize_Values()
        
        for Index, Coordinates in enumerate(self.tsp_path[:]):
            
            P1_Init = Coordinates
            
            if(Index != (len(self.tsp_path) - 1)):
                P2_Des = self.tsp_path[Index+1]         
            else:
                P2_Des = [0, 0]
            
            Init_X_Coor = P1_Init[0]
            Init_Y_Coor = P1_Init[1]
            
            self.SPUG_Run.Set_product_destnation_position(P2_Des[0],P2_Des[1])            
            
            self.PDDL_Generator.Initialize_Values()
            self.PDDL_Generator.Set_Initial_Point(Init_X_Coor,Init_Y_Coor)
            self.PDDL_Generator.Set_Terminal_Point(P2_Des[0],P2_Des[1])
            self.PDDL_Generator.Set_Blocking_Points(blocking_points)
            
            self.PDDL_Generator.Generate_PDDL_Script()
            
            Response = self.PDDL_Generator.Get_Response()
            
            if(Response == "All paths blocked"):
                print("All paths are blocked. Please wait for some time")
                return
                
            else:
                print("Initial Coordinates - %s and Target Coordinates - %s"%(P1_Init,P2_Des))                         
                print("----- Path Taken")
            
                while(P1_Init != P2_Des):
            
                    with open("Plan_to_follow.txt", 'r') as PDDL_File:
                        for line in PDDL_File:
                            Cmd = line.split(' ')
                            Direction_Line = Cmd[0].split('_')
                            Dir = Direction_Line[1]
                    
                            if(Dir == "north"):
                                P1_Init[0] = P1_Init[0]
                                P1_Init[1] = P1_Init[1] + 1

                            elif(Dir == "south"):
                                P1_Init[0] = P1_Init[0]
                                P1_Init[1] = P1_Init[1] - 1

                            elif(Dir == "east"):
                                P1_Init[0] = P1_Init[0] + 1
                                P1_Init[1] = P1_Init[1]

                            elif(Dir == "west"):
                                P1_Init[0] = P1_Init[0] - 1
                                P1_Init[1] = P1_Init[1]
                            
                        
                            print("Next Point - %s"%P1_Init)
                
                            X_Target = P1_Init[0]
            
                            Y_Target = P1_Init[1]
            
                            self.SPUG_Run.Set_intermediate_destnation_position(X_Target,Y_Target)
            
                            self.SPUG_Run.Run_Cart12()
            
                            if (self.SPUG_Run.Is_Intermediate_DestinTion_Reached()):
                                continue
                            
                    #---------------------Receive Product location Coordinates as MQTT Message from Server-----------------
                    if(self.SPUG_Run.Is_Product_DestinTion_Reached()):
                        def on_message(client, userdata, message):
                            messageJson = json.loads(message.payload.decode())
                    
                            print(message)
                            print("Continue message received")
                            client.loop_stop()
                            client.disconnect()
        
                        client = mqtt.Client("RaspBerry_PI_Rec2") #create new instance
        
                        client.on_message=on_message #attach function to callback

                        client.connect('192.168.1.9', 1883, 70) #connect to broker

                        client.subscribe("continue/4/", 2)
        
                        print("Waiting for the continue message")
            
                        client.loop_forever() #stop the loop
                    #--------------------------------------------------------------------------------------------------------------
                                  
                print("--------------------------")
                
        self.SPUG_Run.LED.ledIndex(0xFF,0,0,0)
                

Sht_Pth = Shortest_Path()
if __name__ == "__main__":
    
    Sht_Pth.Main()