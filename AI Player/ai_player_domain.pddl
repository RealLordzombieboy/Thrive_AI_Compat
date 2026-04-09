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

    ; (:action select
    ;     :parameters (?organelle ?cost)
    ;     :precondition (and 
    ;     ; Need to find formulas on how much ATP production is increased for each organelle based on the current compound amounts.
    ;         (and (valid_selection ?organelle))
    ;     ) 
    ;     :effect (and
    ;         (increase (total ?tc) (?cost)) ; Unsure why this is considered a syntax error. Could be numeric planner not yet on system, or an actual error? - Likely the former.
    ;     )
    ; )
)