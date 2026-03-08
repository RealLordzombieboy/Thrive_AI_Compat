import pandas as pd
from pgmpy.models import LinearGaussianBayesianNetwork
# from pgmpy.models import BayesianNetwork
# from pgmpy.factors.continuous import LinearGaussianCPD
# from pgmpy.estimators import ParameterEstimator # For training
# from pgmpy.estimators import MaximumLikelihoodEstimator
import os
import Thrive_AI
import time

# IMPORTANT: Will need to run this many times to train the model.
# Final value will state what it selected in the previous run or current run? -- Current run, ish, unfortunately.

def best_organelle_calc(current_data):
    organelles = ["cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet"]
    organelle_prediction = []
    for i in range(12):
        df = current_data.drop(columns=organelles[i])
        organelle_prediction.append(model.predict(df))

    best_num = -2147483648 # Negative integer limit
    best_organelle = "N/A"
    best_organelle_num = 0
    for i in range(len(organelle_prediction)):
        val = organelle_prediction[i][1][0][0]
        #print(val) # DEBUG
        if val > best_num:
            best_num = val
            best_organelle = organelle_prediction[i][0][0]
            best_organelle_num = i
    
    if best_organelle == "N/A":
        raise RuntimeError("No best Organelle found. Organelles: {organelle_prediction}")

    return best_organelle, best_organelle_num

# Initialization:

# WARNING: Ensure cheats are enabled, press F6, turn on Unlimited Resources and Infinite Growth Speed before running this program.
time.sleep(3) # So user can quickly re-enter Thrive environment before mouse control is taken.
Thrive_AI.to_editor()

# Create model with connections between nodes:
model = LinearGaussianBayesianNetwork([("ATP Production", "Population"), ("ATP Consumption", "Population"), ("Speed", "Population"), # Base direct impacts on Population
                         # ATP Production and Consumption:
                         ("cytoplasm", "ATP Production"), ("cytoplasm", "ATP Consumption"), ("hydrogenase", "ATP Production"), ("hydrogenase", "ATP Consumption"),
                         ("metabolosomes", "ATP Production"), ("metabolosomes", "ATP Consumption"), ("thylakoids", "ATP Production"), ("thylakoids", "ATP Consumption"),
                         ("chemosynthesizing proteins", "ATP Production"), ("chemosynthesizing proteins", "ATP Consumption"),
                         ("rusticyanin", "ATP Production"), ("rusticyanin", "ATP Consumption"), ("nitrogenase", "ATP Production"), ("nitrogenase", "ATP Consumption"),
                         ("toxisome", "ATP Production"), ("toxisome", "ATP Consumption"), ("flagellum", "ATP Production"), ("flagellum", "ATP Consumption"),
                         ("perforator pilus", "ATP Consumption"), ("chemoreceptor", "ATP Consumption"), ("slime jet", "ATP Consumption"),
                         ("perforator pilus", "Population"), ("chemoreceptor", "Population"), # Unique direct effects on Population
                         # Speed:
                         ("flagellum", "Speed"), ("slime jet", "Speed"), ("cytoplasm", "Speed"), ("hydrogenase", "Speed"), ("metabolosomes", "Speed"),
                         ("thylakoids", "Speed"), ("chemosynthesizing proteins", "Speed"), ("rusticyanin", "Speed"), ("nitrogenase", "Speed"), ("toxisome", "Speed"),
                         ("perforator pilus", "Speed"), ("chemoreceptor", "Speed"),
                         # Compounds effects on Organelles (more of the corresponding compound means organelle more effective):
                         ("Glucose", "cytoplasm"), ("Glucose", "hydrogenase"), ("Glucose", "chemosynthesizing proteins"), ("Glucose", "nitrogenase"), ("Glucose", "toxisome"),
                         ("Carbondioxide", "thylakoids"),  ("Hydrogensulfide", "chemosynthesizing proteins"), #("Iron", "rusticyanin"), ("Oxygen", "metabolosomes"), ("Sunlight", "thylakoids"), # Iron, Oxygen and Sunlight do not change in initial dataset.
                         ("Carbondioxide", "chemosynthesizing proteins"), ("Nitrogen", "nitrogenase"),
                         # Ammonia and Phosphates have a direct effect on Population, as that is what is required to reproduce.
                         ("Ammonia", "Population"), #("Phosphates", "Population") # Phosphates do not change in initial dataset.
                         ])

# Read current log.csv:
__location__ = os.path.realpath(os.path.dirname(__file__))
data = pd.read_csv(__location__ + "/bayes_net_log.csv")
data.drop(columns=["Temperature", "Sunlight", "Oxygen", "Phosphates", "Iron"], inplace=True) # Drop unchanging values in dataset.
model.fit(data)
#print(model.get_cpds()) # DEBUG

# Predict which organelle to select:
current_data = data.iloc[[0]] # Get just the header and initial data.

# Force Bayes Net to pick something that increases its population (Did not work, output still the same.)
# current_data.at[0, "Population"] = current_data["Population"].iloc[0] * 2

# Calculate what organelle to add first:
best_organelle, best_organelle_num = best_organelle_calc(current_data)

place_rotation = 225
num_placed = 0
current_organelles = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Thrive_AI.select_part(best_organelle)
num_placed, place_rotation = Thrive_AI.add_part(num_placed, place_rotation)
current_organelles[best_organelle_num] += 1

Thrive_AI.to_active_stage()
time.sleep(5)

for i in range(7):
    Thrive_AI.to_editor()
    Thrive_AI.convert_to_csv(current_organelles, "bayes_net", False)

    data = pd.read_csv(__location__ + "/bayes_net_log.csv")
    data.drop(columns=["Temperature", "Sunlight", "Oxygen", "Phosphates", "Iron"], inplace=True) # Drop unchanging values in dataset.
    model.fit(data)
    #print(model.get_cpds()) # DEBUG

    # Predict which organelle to select:
    current_data = data.iloc[[len(data) - 1]] # Get just the header and most recent data.

    # Force Bayes Net to pick something that increases its population (Did not work, output still the same.)
    # current_data.at[0, "Population"] = current_data["Population"].iloc[0] * 2

    # Calculate what organelle to add:
    best_organelle, best_organelle_num = best_organelle_calc(current_data)
    time.sleep(2)
    Thrive_AI.select_part(best_organelle)
    time.sleep(2)
    num_placed, place_rotation = Thrive_AI.add_part(num_placed, place_rotation)
    current_organelles[best_organelle_num] += 1
    time.sleep(2)
    Thrive_AI.to_active_stage()
    time.sleep(5)

Thrive_AI.to_editor() # So it ends in the editor.

# Estimate based on data:
#estimate = ParameterEstimator(model, data)
#dag = estimate.estimate(ci_test="pearsonr", return_type="dag") # Pearsonr is only continuous variable test available.
#print(f"Learned edges: {dag}")

# Create nodes for the compounds


# Create nodes for how many of each organelle we already have?

# Create in-between nodes combining compounds and organelles we already have.

# Create nodes for the current atp consumption and production

# Create nodes for the organelles it can select.

# Needs a restriction so it can only select up to 100 points of organelles
# Maybe link organelle nodes together such that we use givens to limit what can be selected?
# Meaning if two of organelle X are selected, the probability of selecting organelle Y is 0%.

# For 30 generations:

    # Enter editor and read data from log.txt.

    # Add data to Bayes Net.

    # Run Bayes Net to determine which organelles to add.

    # For organelle in selected:

        # Select organelle.

        # Add organelle to micro-organism.

    # End editor/confirm.
