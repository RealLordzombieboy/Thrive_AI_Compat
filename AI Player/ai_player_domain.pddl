(define (domain ai-player)
    (:requirements :typing :fluents)

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
        (preference ?p - balance) ; In place of ATP production and consumption as their formulas are complicated, change, and some are hidden. Also since ATP does not show everything (A giant microbe with 100 ATP produced and 4 consumed will still likely die as that is at peak production and the environment likely cannot sustain that many resources all the time)
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

    (:action select_proteins
        :parameters (?che - selected ?p - balance ?hs - compound ?cd - compound ?tc - cost)
        :precondition (and (>= ?hs 11) (not chemosynthesizingproteins ?che) (<= ?tc 55))
        :effect (and (chemosynthesizingprotiens) (increase ?tc 45) (increase ?p (* ?che (/ ?cd 100))) (decrease ?p ?ot) (at end (increase ?ot 1)))
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