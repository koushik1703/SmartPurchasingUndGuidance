(define (domain SPUG)

    
    (:types spug node  - object

    )

    

    (:predicates (spug-at ?s - spug ?n - node)
                 ;(is_path_connected_to_node ?n1 - node ?n2 - node ?d - direction)
                 (is_node_north ?n1 - node ?n2 - node)  
                 (is_node_east ?n1 - node ?n2 - node)
                 (is_node_west ?n1 - node ?n2 - node)
                 (is_node_south ?n1 - node ?n2 - node)
    
    )

    

    (:action MoveNorth
        :parameters (?s - spug ?n1 - node ?n2 - node)
        :precondition (and (spug-at ?s ?n1) (not(spug-at ?s ?n2)) (is_node_north ?n1 ?n2))
        :effect (and (spug-at ?s ?n2) (not(spug-at ?s ?n1)) )
    )
    
    (:action MoveSouth
        :parameters (?s - spug ?n1 - node ?n2 - node)
        :precondition (and (spug-at ?s ?n1) (not(spug-at ?s ?n2)) (is_node_south ?n1 ?n2))
        :effect (and (spug-at ?s ?n2) (not(spug-at ?s ?n1)) )
    )
    
    (:action MoveEast
        :parameters (?s - spug ?n1 - node ?n2 - node)
        :precondition (and (spug-at ?s ?n1) (not(spug-at ?s ?n2)) (is_node_east ?n1 ?n2))
        :effect (and (spug-at ?s ?n2) (not(spug-at ?s ?n1)) )
    )
    
     (:action MoveWest
        :parameters (?s - spug ?n1 - node ?n2 - node)
        :precondition (and (spug-at ?s ?n1) (not(spug-at ?s ?n2)) (is_node_west ?n1 ?n2))
        :effect (and (spug-at ?s ?n2) (not(spug-at ?s ?n1)) )
    )
    )
    
    
    
