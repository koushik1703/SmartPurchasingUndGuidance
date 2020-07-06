from itertools import permutations
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

        points = [[0, 0], [1, 4], [0, 2], [3, 1], [3,3]] #Get the points from the Server
        
        blocking_points = [] #[[0, 1], [1, 1], [3, 4] ] #Grt the points from the server
        
        print("""The minimum distance to visit all the following points: {}\n \
                  starting at {}""".format(tuple(points),points[0]))
        
        print("""With travelling salesman algorithm is {}""".format(
            self.Total_distance(self.Travelling_salesman(points))))
        
        print(self.tsp_path)
        
        self.SPUG_Run.Initialize_Values()
        
        for Index, Coordinates in enumerate(self.tsp_path[:]):
            
            P1_Init = Coordinates
            
            if(Index != (len(self.tsp_path) - 1)):
                P2_Des = self.tsp_path[Index+1]         
            else:
                P2_Des = [0, 0]
            
            print("Initial Coordinates - %s and Target Coordinates - %s"%(P1_Init,P2_Des))                         
            print("----- Path Taken")
            
            while(P1_Init != P2_Des):
                Y_Pos_BP = X_Pos_BP = Y_Neg_BP = X_Neg_BP = 0
                
                for bp in blocking_points:
                    if (bp[0] == P1_Init[0]) and (bp[1] == P1_Init[1] + 1):
                        Y_Pos_BP = 1     
                        
                    elif (bp[0] == P1_Init[0] + 1) and (bp[1] == P1_Init[1]):
                        X_Pos_BP = 1  
                        
                    elif (bp[0] == P1_Init[0]) and (bp[1] == P1_Init[1] - 1):
                        Y_Neg_BP = 1 
                        
                    elif (bp[0] == P1_Init[0] - 1) and (bp[1] == P1_Init[1]):
                        X_Neg_BP = 1
                        
                if((P2_Des[1] - P1_Init[1]) > 0):
                    if (not Y_Pos_BP):
                        P1_Init[1] = P1_Init[1] + 1
                    elif(not X_Pos_BP):
                        P1_Init[0] = P1_Init[0] + 1 
                    
                elif((P2_Des[0] - P1_Init[0]) > 0):
                    if(not X_Pos_BP):
                        P1_Init[0] = P1_Init[0] + 1
                    elif (not Y_Pos_BP):
                        P1_Init[1] = P1_Init[1] + 1
                        
                elif((P2_Des[1] - P1_Init[1]) < 0):
                    if (not Y_Neg_BP):
                        P1_Init[1] = P1_Init[1] - 1
                    elif(not X_Neg_BP):
                        P1_Init[0] = P1_Init[0] + 1 
                        
                elif((P2_Des[0] - P1_Init[0]) < 0):
                    if(not X_Neg_BP):
                        P1_Init[0] = P1_Init[0] - 1
                    elif (not Y_Neg_BP):
                        P1_Init[1] = P1_Init[1] - 1
                        
                        
                if(P1_Init[0] == 0 and P1_Init[1] == 0 and X_Pos_BP and Y_Pos_BP):
                    print("All ways are blocked")
                    break
                elif(X_Pos_BP and Y_Pos_BP and X_Neg_BP and Y_Neg_BP):
                    print("All ways are blocked")
                    break                      
                 
                print("Next Point - %s"%P1_Init)
                
                X_Target = P1_Init[0]
            
                Y_Target = P1_Init[1]
            
                self.SPUG_Run.Set_destnation_position(X_Target,Y_Target)
            
                self.SPUG_Run.Run_Cart12()
            
                if (self.SPUG_Run.Is_DestinTion_Reached()):
                    continue
                                  
            print("--------------------------")

Sht_Pth = Shortest_Path()
if __name__ == "__main__":
    
    Sht_Pth.Main()