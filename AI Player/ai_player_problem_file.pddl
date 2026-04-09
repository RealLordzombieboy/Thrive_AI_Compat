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