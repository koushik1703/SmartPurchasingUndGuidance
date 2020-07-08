(define (domain SPUG)

	(:types spug node - object
	)

(:predicates 
	(spug-at ?s - spug ?n - node)
	(not_same_spug ?s1 - spug ?s2 - spug)
	(is_node_north ?n1  ?n2 - node)
	(is_node_east ?n1  ?n2 - node)
	(is_node_west ?n1  ?n2 - node)
	(is_node_south ?n1  ?n2 - node)
	)

(:action Move_North_
	:parameters (?s1 - spug ?n1 - node ?n2 - node) 
	:precondition (and (spug-at ?s1 ?n1) (is_node_north ?n1 ?n2) (not(spug-at ?s1 ?n2)) )

	:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )
	)

(:action Move_South_
	:parameters (?s1 - spug ?n1 - node ?n2 - node) 
	:precondition (and (spug-at ?s1 ?n1) (is_node_south ?n1 ?n2) (not(spug-at ?s1 ?n2)) )

	:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )
	)

(:action Move_East_
	:parameters (?s1 - spug ?n1 - node ?n2 - node) 
	:precondition (and (spug-at ?s1 ?n1) (is_node_east ?n1 ?n2) (not(spug-at ?s1 ?n2)) )

	:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )
	)

(:action Move_West_
	:parameters (?s1 - spug ?n1 - node ?n2 - node) 
	:precondition (and (spug-at ?s1 ?n1) (is_node_west ?n1 ?n2) (not(spug-at ?s1 ?n2)) )

	:effect (and (spug-at ?s1 ?n2) (not (spug-at ?s1 ?n1)) )
	)

)