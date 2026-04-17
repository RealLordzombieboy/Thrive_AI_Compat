import os
import pandas as pd
import Thrive_AI

# This file makes a an ai_plaer_problem_file based on the current log.txt environment conditions when run. Used to quickly create problem files during each generation
# to make using the planner much faster.

# Initial lines:
lines = [
        "(define (problem ai-player-editor)\n", 
        "    (:domain ai-player)\n",
        "    (:objects\n",
        "        balance\n",
        "        compound\n",
        "        cost\n",
        "    )\n",
        "    (:init\n",
        "        (= (preference balance) 0)\n",
        "        (= (total cost) 0)\n",
        "        (= (organelles cost) 1) ; Starts with 1 organelle on microorganism at beginning of run/generation 1.\n"
        ]

Thrive_AI.convert_to_csv([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "planner", True)

# Convert csv environment/compound data into Python list:
__location__ = os.path.realpath(os.path.dirname(__file__))
data = pd.read_csv(__location__ + "/planner_log.csv")
data = data.iloc[0].to_list()[1:10] # All current compound/environmental data excluding Ammonia.
data.pop(1) # Also removes Phosphates. Both of these are not needed as there are no organelles to select that directly use them.
compounds = ["glucose","hydrogensulfide","oxygen","carbondioxide","nitrogen","sunlight","temperature","iron"]

# Loop through adding all compounds/environmental data to the init:
for i in range(len(compounds)):
    next_line = "        (= (" + compounds[i] + " compound) " + (str)(data[i]) + ")\n"
    lines.append(next_line)

# Concluding lines:
conclusion = [
            "    )\n",
            "    ; Maximize preference out of any viable combination of organelles to add. Must not use more than 100 points in a generation.\n",
            "    (:goal (and (maximize preference) (<= (total cost) 100)))\n",
            ")\n"
]

lines.extend(conclusion)

# Write to new ai_player_problem_file.pddl file:
with open(__location__ + "/ai_player_problem_file.pddl", 'w') as file:
        file.writelines(lines)
