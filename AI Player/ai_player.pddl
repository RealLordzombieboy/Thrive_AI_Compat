(define (domain ai-player)
    (:requirements :typing :fluents)

    (:predicates
        (cost ?cst)
        (valid_selection ?org)
    )

    ; Functions are numerical values that can change over time, compared to predicates which are just True/False.
    (:functions 
        (produced ?p -atp)
        (consumed ?c -atp)
        (glucose ?g -compound)
        (phosphates ?phosphate -compound)
        (hydrogensulfide ?hs -compound)
        (oxygen ?o -compound)
        (carbondioxide ?cd -compound)
        (nitrogen ?n -compound)
        (total ?tc -cost)
    )

    (:action select
        :parameters (?organelle ?cost)
        :precondition (and 
        ; Need to find formulas on how much ATP production is increased for each organelle based on the current compound amounts.
            (and (valid_selection ?organelle))
        ) 
        :effect (and
            (increase (total ?tc) (?cost)) ; Unsure why this is considered a syntax error. Could be numeric planner not yet on system, or an actual error? - Likely the former.
        )
    )
)

(define (problem ai-player-editor)
    (:domain ai-player)
    (:objects
        atp
        compound
        cost
    )
    (:init
        (= (produced atp) 1)
        (= (consumed atp) 3)
        (= (total cost) 0) ; Starts total cost at 0.
    )

; Must be at least equal ATP produced as consumed, not less. Must not use more than 100 points in a generation.
(:goal (and (>= (produced atp) (consumed atp)) (<= (total cost) 100)))
; How to make it actually change something rather than stay with initial microbe?
; Need more requirements for goal.
)
