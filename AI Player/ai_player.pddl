(define (domain ai-player)
    (:requirements :typing :fluents)

    (:predicates
        (selected ?organelle)
    )

    ; Functions are numerical values that can change over time, compared to predicates which are just True/False.
    (:functions 
        (produced ?p -atp)
        (consumed ?c -atp)
    )
)

(define (problem ai-player-editor)
    (:domain ai-player)
    (:objects
        atp
    )
    (:init
        (= (produced atp) 1)
        (= (consumed atp) 3)
    )

(:goal (and (>= (produced atp) (consumed atp)))) ; Must be at least equal ATP produced as consumed, not less.
; How to make it actually change something rather than stay with initial microbe?
; Need more requirements for goal.
)
