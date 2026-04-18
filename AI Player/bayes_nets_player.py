import os
import pandas as pd
from pgmpy.models import LinearGaussianBayesianNetwork
# from pgmpy.models import BayesianNetwork
# from pgmpy.factors.continuous import LinearGaussianCPD
# from pgmpy.estimators import ParameterEstimator # For training
# from pgmpy.estimators import MaximumLikelihoodEstimator
import Thrive_AI
import time

# Initialization:
time.sleep(2) # Allow the user to quickly open the game after starting this program.
Thrive_AI.turn_on_cheats()

# Create model with connections between nodes:
model = LinearGaussianBayesianNetwork([("ATP Production", "Population"), ("ATP Consumption", "Population"), ("Speed", "Population"), # Base direct impacts on Population
                                       ("Ammonia", "Population"), #("Phosphates", "Population") # Phosphates do not change in initial dataset.
                                       #("ATP Consumption", "selected"), ("ATP Production", "selected"), ("Population", "selected"), # Enable this row if data points >= 512.
                                       ("Glucose", "selected"), ("Hydrogensulfide", "selected"), ("Iron", "selected"), ("Oxygen", "selected"), #("Sunlight", "thylakoids"), # Sunlight does not change in initial dataset.
                                       ("Carbondioxide", "selected"), ("Nitrogen", "selected")
])

__location__ = os.path.realpath(os.path.dirname(__file__))
num_placed = 1
current_organelles = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data = pd.read_csv(__location__ + "/data_log.csv") # Read current log.csv.

# Drop unchanging values and organelle counts in dataset.
data.drop(columns=["Temperature", "Sunlight", "Phosphates", "cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet"], inplace=True)
model.fit(data)

# Run for 20 generations:
for i in range(20):
    Thrive_AI.to_editor()
    Thrive_AI.convert_to_csv(current_organelles, "bayes_net", False)

    # Predict which organelle to select:
    current_data = data.iloc[[len(data) - 1]] # Get just the header and most recent data.

    data = pd.read_csv(__location__ + "/bayes_net_log.csv") # Read current log.csv.
    # Force Bayes Net to pick something that increases its population (Did not work, output still the same.)
    # current_data.at[0, "Population"] = current_data["Population"].iloc[0] * 2

    # Calculate what organelle to add:
    
    df = current_data.drop(columns="selected")
    organelle_prediction = round(model.predict(df)[1][0][0])
    #print(organelle_prediction) # DEBUG

    # If predicted a value that does not have an organelle associated with it (or the option of no organelles) make it choose to add no organelles:
    if organelle_prediction < 0 or organelle_prediction > 12:
        organelle_prediction = 12
        print("Unexpected value, defaulting to:", organelle_prediction) # DEBUG
    else:
        Thrive_AI.select_part(organelle_prediction)
        time.sleep(1)
        num_placed = Thrive_AI.add_part(num_placed)
        current_organelles[organelle_prediction] += 1
    Thrive_AI.to_active_stage()

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
