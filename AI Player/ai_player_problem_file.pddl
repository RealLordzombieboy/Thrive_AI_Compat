(define (problem ai-player-editor)
    (:domain ai-player)
    (:objects
        balance
        compound
        cost
    )
    (:init
        (= (preference balance) 0)
        (= (total cost) 0)
        (= (organelles cost) 1) ; Starts with 1 organelle on microorganism at beginning of run/generation 1.
        (= (glucose compound) 3.2829087)
        (= (hydrogensulfide compound) 10.125566)
        (= (oxygen compound) 0.0)
        (= (carbondioxide compound) 29.874914)
        (= (nitrogen compound) 63.27038)
        (= (sunlight compound) 0.0)
        (= (temperature compound) 9800.0)
        (= (iron compound) 3.0275025)
    )
    ; Maximize preference out of any viable combination of organelles to add. Must not use more than 100 points in a generation.
    (:goal (and (maximize preference) (<= (total cost) 100)))
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
