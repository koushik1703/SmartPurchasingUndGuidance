map_size = 3
number_spug = 1
start_point_spugs =[(0,0),(0,2)]
end_point_spug =(3,4)



def write_pddl_problem(map_size, number_spug, start_point_spugs, end_point_spug):
	problem_file = open("Move_SPUG.pddl", "w")
	
	##### write the definition part #####
	problem_file.write("(define (problem MoveSPUG)\n")
	problem_file.write("	(:domain SPUG)\n")
	problem_file.write("	(:objects \n")
	
	nodes = [(x,y) for x in range(map_size+1) for y in range(map_size+1)]
	
	spugs = range (0, number_spug)
	I=0
	I_new=0
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
	
	########### write the init part ##########
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
	
	problem_file.write("\n\t)")
	
	
	###########goal##########
	problem_file.write("\n\n\t(:goal (spug-at spug{0} n_{1}_{2})\n\t)\n".format(1, end_point_spug[0], end_point_spug[1]))
	
	####EOF####
	problem_file.write("\n)")
	
write_pddl_problem(map_size, number_spug, start_point_spugs, end_point_spug)