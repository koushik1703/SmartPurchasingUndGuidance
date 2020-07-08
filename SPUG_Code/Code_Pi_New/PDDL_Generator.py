import time
import requests
import sys
from itertools import combinations

class PDDL_Generator:
    def Initialize_Values(self):
        self.map_size = 4
        self.number_spug = 1
        self.start_point_spugs =[(0,0)]
        self.end_point_spug =(2,2)
        
    def Set_Initial_Point(self, X_Coordinate, Y_Coordinate):
        Initial_Point = (X_Coordinate, Y_Coordinate)
        self.start_point_spugs[0] = Initial_Point
        
    def Set_Terminal_Point(self, X_Coordinate, Y_Coordinate):
        Terminating_Point = (X_Coordinate, Y_Coordinate)
        self.end_point_spug = Terminating_Point
        
    def Set_Blocking_Points(self, Blocking_Points):
        for Index, Coordinates in enumerate(Blocking_Points[:]):
            Blocking_Point = Coordinates
            self.start_point_spugs.append(Blocking_Point)
            self.number_spug = Index + 2
		
    def write_pddl_domain (self, number_spug):
        spugs = range(0, number_spug)
        domain_file = open("domain_SPUG.pddl", "w")
        domain_file.write("(define (domain SPUG)\n\n\t(:types spug node - object\n\t)\n\n")
        domain_file.write("(:predicates \n\t(spug-at ?s - spug ?n - node)\n\t(not_same_spug ?s1 - spug ?s2 - spug)\n\t(is_node_north ?n1  ?n2 - node)\n\t(is_node_east ?n1  ?n2 - node)\n\t(is_node_west ?n1  ?n2 - node)\n\t(is_node_south ?n1  ?n2 - node)\n\t)")
		# ****************** Move North *************************#
        domain_file.write("\n\n(:action Move_North_\n\t:parameters (")
        for i in spugs:
            domain_file.write("?s{0} ".format(i+1))
        domain_file.write("- spug ?n1 - node ?n2 - node) \n\t:precondition")
        domain_file.write(" (and (spug-at ?s1 ?n1) (is_node_north ?n1 ?n2) ")
        for i in spugs:
            domain_file.write("(not(spug-at ?s{0} ?n2)) ".format(i+1))
        
        res_lst = sorted(map(sorted, combinations(set(spugs), 2)))
        for item in res_lst:
            domain_file.write("(not_same_spug ?s{0} ?s{1}) ".format(item[0]+1, item[1]+1))
        domain_file.write(")\n\n")
        
        domain_file.write("\t:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )\n\t)")
		# ****************** Move South *************************#
        domain_file.write("\n\n(:action Move_South_\n\t:parameters (")
        for i in spugs:
            domain_file.write("?s{0} ".format(i+1))
        domain_file.write("- spug ?n1 - node ?n2 - node) \n\t:precondition")
        
        domain_file.write(" (and (spug-at ?s1 ?n1) (is_node_south ?n1 ?n2) ")
        
        for i in spugs:
            domain_file.write("(not(spug-at ?s{0} ?n2)) ".format(i+1))
        
        res_lst = sorted(map(sorted, combinations(set(spugs), 2)))
        for item in res_lst:
            domain_file.write("(not_same_spug ?s{0} ?s{1}) ".format(item[0]+1, item[1]+1))
        domain_file.write(")\n\n")
        
        domain_file.write("\t:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )\n\t)")
        
        #********************** Move East ***************************#
        domain_file.write("\n\n(:action Move_East_\n\t:parameters (")
        for i in spugs:
            domain_file.write("?s{0} ".format(i+1))
        domain_file.write("- spug ?n1 - node ?n2 - node) \n\t:precondition")
        
        domain_file.write(" (and (spug-at ?s1 ?n1) (is_node_east ?n1 ?n2) ")
        
        for i in spugs:
            domain_file.write("(not(spug-at ?s{0} ?n2)) ".format(i+1))
        
        res_lst = sorted(map(sorted, combinations(set(spugs), 2)))
        for item in res_lst:
            domain_file.write("(not_same_spug ?s{0} ?s{1}) ".format(item[0]+1, item[1]+1))
        domain_file.write(")\n\n")
        
        domain_file.write("\t:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )\n\t)")
        
        #********************** Move West ****************************#
        domain_file.write("\n\n(:action Move_West_\n\t:parameters (")
        for i in spugs:
            domain_file.write("?s{0} ".format(i+1))
        domain_file.write("- spug ?n1 - node ?n2 - node) \n\t:precondition")
        
        domain_file.write(" (and (spug-at ?s1 ?n1) (is_node_west ?n1 ?n2) ")
        
        for i in spugs:
            domain_file.write("(not(spug-at ?s{0} ?n2)) ".format(i+1))
        
        res_lst = sorted(map(sorted, combinations(set(spugs), 2)))
        for item in res_lst:
            domain_file.write("(not_same_spug ?s{0} ?s{1}) ".format(item[0]+1, item[1]+1))
        domain_file.write(")\n\n")
        
        domain_file.write("\t:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )\n\t)")
        domain_file.write("\n\n)")
		
        
    def write_pddl_problem(self, map_size, number_spug, start_point_spugs, end_point_spug):

        spugs = range (0, number_spug)
        I=0
        I_new=0
        problem_file = open("Move_SPUG.pddl", "w")
	
        #--------------write the definition part------------------#
        problem_file.write("(define (problem MoveSPUG)\n")
        problem_file.write("	(:domain SPUG)\n")
        problem_file.write("	(:objects \n")
	
        nodes = [(x,y) for x in range(map_size+1) for y in range(map_size+1)]
	
        for (i,j) in nodes:
            I_new = i
            if (I != I_new):
                I=I_new
                problem_file.write("\n")
            problem_file.write("	n_"+str(i)+"_"+str(j))
	
        problem_file.write("	- node\n")
	
        for i in spugs:
            problem_file.write("\tspug"+str(i+1)+" ")
        problem_file.write("	- spug")
        problem_file.write("\n  )\n")
	
        #-----------write the init part---------------#
        problem_file.write("	(:init \n")
	
        for i in range(0, map_size): #init North relationships
            for j in range(0, map_size):
                problem_file.write("\t(is_node_north n_{0}_{1} n_{0}_{2})".format(i,j,j+1))
            problem_file.write("\n")
        problem_file.write("\n")
	
        for i in range(0, map_size): #init South relationships
            for j in range(0, map_size):
                problem_file.write("\t(is_node_south n_{0}_{2} n_{0}_{1})".format(i,j,j+1))
            problem_file.write("\n")
        problem_file.write("\n")
	
        for i in range(0, map_size): #init East relationships
            for j in range(0, map_size):
                problem_file.write("\t(is_node_east n_{1}_{0} n_{2}_{0})".format(i,j,j+1))
            problem_file.write("\n")
        problem_file.write("\n")
		
        for i in range(0, map_size): #init West relationships
            for j in range(0, map_size):
                problem_file.write("\t(is_node_west n_{2}_{0} n_{1}_{0})".format(i,j,j+1))
            problem_file.write("\n")
        problem_file.write("\n")
	
        for i in range(0, number_spug):
            problem_file.write("\t(spug-at spug{0} n_{1}_{2})".format(i+1, start_point_spugs[i][0], start_point_spugs[i][1] ))
            problem_file.write("\n")
        res_lst = sorted(map(sorted, combinations(set(spugs), 2)))
        for item in res_lst:
            problem_file.write("(not_same_spug spug{0} spug{1}) ".format(item[0]+1, item[1]+1))
        problem_file.write("\n")
	
        problem_file.write("\n\t)")
        #----------------goal----------------------#
        problem_file.write("\n\n\t(:goal (spug-at spug{0} n_{1}_{2})\n\t)\n".format(1, end_point_spug[0], end_point_spug[1]))
	
        #----------------EOF-----------------------#
        problem_file.write("\n)")	

    def PDDL_solve(self):
        data = {'domain': open("domain_SPUG.pddl", 'r').read(), 'problem': open("Move_SPUG.pddl", 'r').read()}
        response = requests.post('http://solver.planning.domains/solve',json=data).json()
        with open("Plan_to_follow.txt", 'w') as f:
            for act in response ['result']['plan']:
                f.write(str(act['name']))
                f.write('\n')        
        
    def Generate_PDDL_Script(self):
        self.write_pddl_problem(self.map_size, self.number_spug, self.start_point_spugs, self.end_point_spug)
        self.write_pddl_domain(self.number_spug)
        self.PDDL_solve()
					
PDDL_Gen = PDDL_Generator()
if __name__ == "__main__":

    PDDL_Gen.Initialize_Values()
    PDDL_Gen.Generate_PDDL_Script()
    
    