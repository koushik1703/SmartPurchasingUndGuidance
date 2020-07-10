(define (problem MoveSPUG)
	(:domain SPUG)
	(:objects 
	n_0_0	n_0_1	n_0_2	n_0_3	n_0_4
	n_1_0	n_1_1	n_1_2	n_1_3	n_1_4
	n_2_0	n_2_1	n_2_2	n_2_3	n_2_4
	n_3_0	n_3_1	n_3_2	n_3_3	n_3_4
	n_4_0	n_4_1	n_4_2	n_4_3	n_4_4	- node
	spug1 	- spug
  )
	(:init 
	(is_node_north n_0_0 n_0_1)	(is_node_north n_0_1 n_0_2)	(is_node_north n_0_2 n_0_3)	(is_node_north n_0_3 n_0_4)
	(is_node_north n_1_0 n_1_1)	(is_node_north n_1_1 n_1_2)	(is_node_north n_1_2 n_1_3)	(is_node_north n_1_3 n_1_4)
	(is_node_north n_2_0 n_2_1)	(is_node_north n_2_1 n_2_2)	(is_node_north n_2_2 n_2_3)	(is_node_north n_2_3 n_2_4)
	(is_node_north n_3_0 n_3_1)	(is_node_north n_3_1 n_3_2)	(is_node_north n_3_2 n_3_3)	(is_node_north n_3_3 n_3_4)

	(is_node_south n_0_1 n_0_0)	(is_node_south n_0_2 n_0_1)	(is_node_south n_0_3 n_0_2)	(is_node_south n_0_4 n_0_3)
	(is_node_south n_1_1 n_1_0)	(is_node_south n_1_2 n_1_1)	(is_node_south n_1_3 n_1_2)	(is_node_south n_1_4 n_1_3)
	(is_node_south n_2_1 n_2_0)	(is_node_south n_2_2 n_2_1)	(is_node_south n_2_3 n_2_2)	(is_node_south n_2_4 n_2_3)
	(is_node_south n_3_1 n_3_0)	(is_node_south n_3_2 n_3_1)	(is_node_south n_3_3 n_3_2)	(is_node_south n_3_4 n_3_3)

	(is_node_east n_0_0 n_1_0)	(is_node_east n_1_0 n_2_0)	(is_node_east n_2_0 n_3_0)	(is_node_east n_3_0 n_4_0)
	(is_node_east n_0_1 n_1_1)	(is_node_east n_1_1 n_2_1)	(is_node_east n_2_1 n_3_1)	(is_node_east n_3_1 n_4_1)
	(is_node_east n_0_2 n_1_2)	(is_node_east n_1_2 n_2_2)	(is_node_east n_2_2 n_3_2)	(is_node_east n_3_2 n_4_2)
	(is_node_east n_0_3 n_1_3)	(is_node_east n_1_3 n_2_3)	(is_node_east n_2_3 n_3_3)	(is_node_east n_3_3 n_4_3)

	(is_node_west n_1_0 n_0_0)	(is_node_west n_2_0 n_1_0)	(is_node_west n_3_0 n_2_0)	(is_node_west n_4_0 n_3_0)
	(is_node_west n_1_1 n_0_1)	(is_node_west n_2_1 n_1_1)	(is_node_west n_3_1 n_2_1)	(is_node_west n_4_1 n_3_1)
	(is_node_west n_1_2 n_0_2)	(is_node_west n_2_2 n_1_2)	(is_node_west n_3_2 n_2_2)	(is_node_west n_4_2 n_3_2)
	(is_node_west n_1_3 n_0_3)	(is_node_west n_2_3 n_1_3)	(is_node_west n_3_3 n_2_3)	(is_node_west n_4_3 n_3_3)

	(spug-at spug1 n_0_0)


	)

	(:goal (spug-at spug1 n_2_2)
	)

)