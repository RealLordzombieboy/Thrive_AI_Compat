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
        (iron ?irn - compound)
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
                        (increase (organelles ?ot) 1)) ; Preferably uses "at end ()" to ensure this is the last thing that is done, but causes an error of some kind when left in. Can still work if done at any consistent point in the effect process.
    )

    (:action select-hydrogenase
        :parameters (?hyd - selected ?p - balance ?g - compound ?tc - cost ?ot - cost)
        :precondition (and (not (hydrogenase ?hyd)) (<= (total ?tc) 55))
        ; Chose to multiply current glucose by 1.76 for the same reason as above (hydrogenase is about 76% better at converting glucose per cell than cytoplasm. Though cytoplasm is more efficient at it unit-value-wise the cost can become too great to have many organelles, so compacted into one can be better.)
        :effect (and    (hydrogenase ?hyd)
                        (increase (total ?tc) 45)
                        (increase (preferencer ?p) (* (glucose ?g) 1.76))
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
                        (increase (total ?tc) 45)
                        ; Though thylakoids mainly produce glucose, not ATP, they also convert glucose into ATP at a similar rate to cytoplasm so I will consider the production of glucose to be equivalent to production of ATP (though technically better as it produces its own assuming sunlight). *4 mainly because with 50% sunlight it is 4* more efficient than cytoplasm.
                        (increase (preferencer ?p) (+ (glucose ?g) (* 4 (+ (sunlight ?sl) (carbondioxide ?cd)))))
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
        :precondition (and (not (nitrogenase ?nit)) (<= (total ?tc) 45)) ; Configure values such that optimal until (>= ?hs 11)
        :effect (and    (nitrogenase ?nit)
                        (increase (total ?tc) 55)
                        (increase (preferencer ?p) (*(- (glucose ?g) (* 2.676 (nitrogen ?n))) 2)) ; Arbitrary preference increase to make it a selectible organelle if nitrogen high enough. (Organelle produced ammonium which is needed for mitosis, so both produces and consumes ATP.) At about 100% nitrogen consumes 2.676 ATP per second. Always produces 2 ATP per second.
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    ; FUTURE TODO: Make it so that microorganism/planner can only select/have up to one toxisome at a time. Not much need for any more as cons would start to drastically outweigh the diminishing returns.
    (:action select-toxisome
        :parameters (?tox - selected ?p - balance ?g - compound ?tc - cost ?ot - cost)
        :precondition (and (not (toxisome ?tox)) (<= (total ?tc) 45) (>= (organelles ?ot) 5)) ; This is an boost to attack capabilities, so only really works if organism has enough organelles to engulf most targets.
        :effect (and    (toxisome ?tox)
                        (increase (total ?tc) 55)
                        (increase (preferencer ?p) (+ (glucose ?g) 3)) ; Arbitrary addition to make toxisomes potentially worthwhile if there is not a "must pick this" option currently available. It converts some glucose but consumes 1 ATP more than it produces at maximum ATP production, excluding engulfing other organisms.
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    ; FUTURE TODO: Make it so that microorganism/planner can only select/have up to one toxisome at a time. Not much need for any more as cons would start to drastically outweigh the diminishing returns.
    (:action select-flagellum
        :parameters (?fla - selected ?p - balance ?tc - cost ?ot - cost)
        :precondition (and (not (flagellum ?fla)) (<= (total ?tc) 45) (>= (organelles ?ot) 10)) ; Only really necessary for especially large microorganisms.
        :effect (and    (flagellum ?fla)
                        (increase (total ?tc) 55)
                        (increase (preferencer ?p) (* (organelles ?ot) 1.5)) ; Proportional to organelle count to make flagellum potentially worthwhile if there is not a "must pick this" option currently available.
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    ; FUTURE TODO: Make it so that microorganism/planner can only select/have up to one toxisome at a time. Not much need for any more as cons would start to drastically outweigh the diminishing returns.
    (:action select-perforatorpilus
        :parameters (?per - selected ?p - balance ?tc - cost ?ot - cost)
        :precondition (and (not (perforatorpilus ?per)) (<= (total ?tc) 70) (>= (organelles ?ot) 5)) ; Similar to toxisome, should not be picked first and need the volume to be able to consume what is attacked.
        :effect (and    (perforatorpilus ?per)
                        (increase (total ?tc) 30)
                        (increase (preferencer ?p) 5) ; Arbitrary value to make perforatorpilus potentially worthwhile if there is not a "must pick this" option currently available.
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    ; FUTURE TODO: Make it so that microorganism/planner can only select/have up to one toxisome at a time. Not much need for any more as cons would start to drastically outweigh the diminishing returns.
    (:action select-chemoreceptor
        :parameters (?che - selected ?p - balance ?g - compound ?tc - cost ?ot - cost)
        :precondition (and (not (chemoreceptor ?che)) (<= (total ?tc) 55) (>= (organelles ?ot) 5) (<= (glucose ?g) 1)) ; Should not be picked first. Only really necessary when glucose is hard to find as it senses it out at a great range, directing the microorganism to larger clouds of glucose.
        :effect (and    (chemoreceptor ?che)
                        (increase (total ?tc) 45)
                        (increase (preferencer ?p) (+ (glucose ?g) 5)) ; Arbitrary value plus current glucose to make chemoreceptor potentially worthwhile if there is not a "must pick this" option currently available.
                        (decrease (preferencer ?p) (organelles ?ot))
                        (increase (organelles ?ot) 1))
    )

    ; FUTURE TODO: Make it so that microorganism/planner can only select/have up to one toxisome at a time. Not much need for any more as cons would start to drastically outweigh the diminishing returns.
    (:action select-slimejet
        :parameters (?sli - selected ?p - balance ?tc - cost ?ot - cost)
        :precondition (and (not (slimejet ?sli)) (<= (total ?tc) 40) (>= (organelles ?ot) 5)) ; Should not be picked first. Similar to flagellum, only really useful when larger to evade predators or catch prey.
        :effect (and    (slimejet ?sli)
                        (increase (total ?tc) 60)
                        (increase (preferencer ?p) (* (organelles ?ot) 1.6)) ; Proportional to organelle count to make flagellum potentially worthwhile if there is not a "must pick this" option currently available. Slightly higher than flagellum as does not come with the same giant ATP costs.
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