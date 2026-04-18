(define (problem ai-player-editor)
    (:domain ai-player)
    (:objects
        balance
        compound
        cost
    )
    (:init
        (= (preferencer balance) 0)
        (= (total cost) 0)
        (= (organelles cost) 1) ; Starts with 1 organelle on microorganism at beginning of run/generation 1.
        (= (glucose compound) 3)
        (= (hydrogensulfide compound) 10)
        (= (oxygen compound) 0)
        (= (carbondioxide compound) 29)
        (= (nitrogen compound) 63)
        (= (sunlight compound) 0)
        (= (iron compound) 3)
    )
    
    
    (:goal (and (<= (total cost) 100))) ; Must not use more than 100 points in a generation.
    (:metric maximize (preferencer balance)) ; Maximize preferencer out of any viable combination of organelles to add.
)

; Fog of war? Make it try to plan out 5 generations of evolution only with the current round's statistics?
; Environmental variables:
    ; Glucose,Hydrogensulfide,Oxygen,Carbondioxide,Nitrogen,Sunlight,Temperature,Iron.
; Variables that will change throughout the plan but have an initial value:
    ; Speed,ATP Production,ATP Consumption.

; Actions:
; Select:
    ; cytoplasm,hydrogenase,metabolosomes,thylakoids,chemosynthesizing proteins,rusticyanin,nitrogenase,toxisome,flagellum,perforator pilus,chemoreceptor,slime jet.
; Evolve (Presses play, adds current cost to total cost, resets current cost to 0, generations += 1 (starts at 0))

; For now no fog of war. Would require estimating future compound quantities/percentages as all actions require them, which would take a long time to figure out and set up.
