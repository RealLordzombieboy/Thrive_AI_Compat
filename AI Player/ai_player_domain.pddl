(define (domain ai-player)
    (:requirements :negative-preconditions :typing :fluents)

    (:types
        compound selected cost balance - object
    )

    (:predicates
        ; Organelle types:
        (cytoplasm ?cyt - selected)
        (hydrogenase ?hyd - selected)
        (metabolosomes ?met - selected)
        (thylakoids ?thy - selected)
        (chemosynthesizingproteins ?che - selected)
        (rusticyanin ?rus - selected)
        (nitrogenase ?nit - selected)
        (toxisome ?tox - selected)
        (flagellum ?fla - selected)
        (perforatorpilus ?per - selected)
        (chemoreceptor ?che - selected)
        (slimejet ?sli - selected)
    )

; cytoplasm,hydrogenase,metabolosomes,thylakoids,chemosynthesizing proteins,rusticyanin,nitrogenase,toxisome,flagellum,perforator pilus,chemoreceptor,slime jet.

    ; Functions are numerical values that can change over time, compared to predicates which are just True/False.
    (:functions 
        (preferencer ?p - balance) ; Preference is a key word so preferencer needs to be used. In place of ATP production and consumption as their formulas are complicated, change, and some are hidden. Also since ATP does not show everything (A giant microbe with 100 ATP produced and 4 consumed will still likely die as that is at peak production and the environment likely cannot sustain that many resources all the time)
        (glucose ?g - compound)
        (hydrogensulfide ?hs - compound)
        (oxygen ?o - compound) ; A percentage out of 100. To use, need to divide by 100 so the upper bound is 1.
        (carbondioxide ?cd - compound) ; A percentage out of 100. To use, need to divide by 100 so the upper bound is 1.
        (nitrogen ?n - compound) ; A percentage out of 100. To use, need to divide by 100 so the upper bound is 1.
        (sunlight ?sl - compound)
        (temperature ?tmp - compound)
        (iron - ?irn compound)
        (total ?tc - cost)
        (organelles ?ot - cost) ; Keeps track of how many organelles are on the microorganism. To ensure larger microorganisms are less adventageous unless the environment allows.
    )

    (:action select-cytoplasm
        :parameters (?cyt - selected ?p - balance ?g - compound ?tc - cost ?ot - cost)
        :precondition (and (not (cytoplasm ?cyt)) (<= (total ?tc) 78))
        ; Chose to add 3.4 as when glucose was at 4.5 the expected total energy gathered was about equal with hydrogenase, and hydrogenase is about 76% faster at converting glucose to ATP than cytoplasm. So this tickover point is when cytoplasm's other properties outshine hydrogenase (like storage).
        :effect (and    (cytoplasm ?cyt)
                        (increase (total ?tc) 22)
                        (increase (preferencer ?p) (+ (glucose ?g) 3.4))
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    (:action select-hydrogenase
        :parameters (?hyd - selected ?p - balance ?g - compound ?tc - cost)
        :precondition (and (not (hydrogenase ?hyd)) (<= (total ?tc) 55))
        ; Chose to multiply current glucose by 1.76 for the same reason as above (hydrogenase is about 76% better at converting glucose per cell than cytoplasm. Though cytoplasm is more efficient at it unit-value-wise the cost can become too great to have many organelles, so compacted into one can be better.)
        :effect (and    (hydrogenase ?hyd)
                        (increase (total ?tc) 45)
                        (increase (preferencer ?p) (* ?g 1.76))
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    (:action select-metabolosomes
        :parameters (?met - selected ?p - balance ?g - compound ?o -compound ?tc - cost ?ot - cost)
        :precondition (and (not (metabolosomes ?met)) (<= (total ?tc) 50))
        ; At 32.2% oxygen metabolosomes are about 2.41 times better than hydrogenase, so multiplying by 7.5 which will be the max is oxygen reaches 100%.
        :effect (and    (metabolosomes ?met)
                        (increase (total ?tc) 50)
                        (increase (preferencer ?p) (* 7.5 (* (glucose ?g) (/ (oxygen ?o) 100))))
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    (:action select-thylakoid
        :parameters (?thy - selected ?p - balance ?g - compound ?sl - compound ?cd - compound ?tc - cost ?ot - cost)
        :precondition (and (not (thylakoids ?thy)) (<= (total ?tc) 55))
        :effect (and    (thylakoids ?thy)
                        (increase ?tc 45)
                        ; Though thylakoids mainly produce glucose, not ATP, they also convert glucose into ATP at a similar rate to cytoplasm so I will consider the production of glucose to be equivalent to production of ATP (though technically better as it produces its own assuming sunlight). *4 mainly because with 50% sunlight it is 4* more efficient than cytoplasm.
                        (increase (preferencer ?p) (+ (glucose ?g) (* 4 (+ ?sl ?cd))))
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    (:action select-chemproteins
        :parameters (?che - selected ?p - balance ?hs - compound ?cd - compound ?tc - cost ?ot - cost)
        :precondition (and (not (chemosynthesizingproteins ?che)) (<= (total ?tc) 55)) ; Configure values such that optimal until (>= ?hs 11)
        :effect (and    (chemosynthesizingproteins ?che)
                        (increase (total ?tc) 45)
                        (increase (preferencer ?p) (* (hydrogensulfide ?hs) (/ (carbondioxide ?cd) 100)))
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    (:action select-rusticyanin
        :parameters (?rus - selected ?p - balance ?irn - compound ?tc - cost ?ot - cost)
        :precondition (and (not (rusticyanin ?rus)) (<= (total ?tc) 55)) ; Configure values such that optimal until (>= ?hs 11)
        :effect (and    (rusticyanin ?rus)
                        (increase (total ?tc) 45)
                        (increase (preferencer ?p) (iron ?irn))
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    (:action select-nitrogenase
        :parameters (?nit - selected ?p - balance ?g - compound ?n - compound ?tc - cost ?ot - cost)
        :precondition (and (not (rusticyanin ?rus)) (<= (total ?tc) 45)) ; Configure values such that optimal until (>= ?hs 11)
        :effect (and    (nitrogenase ?nit)
                        (increase (total ?tc) 55)
                        (increase (preferencer ?p) (*(- (glucose ?g) (* 2.676 (nitrogen ?n)))) 2) ; Arbitrary preference increase to make it a selectible organelle if nitrogen high enough. (Organelle produced ammonium which is needed for mitosis, so both produces and consumes ATP.) At about 100% nitrogen consumes 2.676 ATP per second. Always produces 2 ATP per second.
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
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