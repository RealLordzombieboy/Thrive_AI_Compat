import pandas as pd
from pgmpy.models import LinearGaussianBayesianNetwork
from pgmpy.models import BayesianNetwork
from pgmpy.factors.continuous import LinearGaussianCPD
from pgmpy.estimators import ParameterEstimator # For training
from pgmpy.estimators import MaximumLikelihoodEstimator
import os

# IMPORTANT: Will need to run this many times to train the model.
# Final value will state what it selected in the previous run or current run?

# Initialization:
#model = LinearGaussianBayesianNetwork()
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
                         ("Carbondioxide", "thylakoids"), ("Iron", "rusticyanin"), ("Hydrogensulfide", "chemosynthesizing proteins"), ("Oxygen", "metabolosomes"), ("Sunlight", "thylakoids"),
                         ("Carbondioxide", "chemosynthesizing proteins"), ("Nitrogen", "nitrogenase"),
                         # Ammonia and Phosphates have a direct effect on Population, as that is what is required to reproduce.
                         ("Ammonia", "Population"), ("Phosphates", "Population")
                         ])

# Read current log.csv:
__location__ = os.path.realpath(os.path.dirname(__file__))
data = pd.read_csv(__location__ + "/bayes_net_log.csv")

#data.drop(columns=["Iron", "Temperature", "Sunlight", "Oxygen", "Glucose", "Phosphates", "Hydrogensulfide", "Ammonia"], inplace=True) # Drop unchanging values in dataset.

model.fit(data)
#print(model.get_cpds())

# Predict which organelle to select:
current_data = data.iloc[[0]] # Get just the header and initial data.
organelles = ["cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet"]
organelle_prediction = []
for i in range(12):
    df = current_data.drop(columns=organelles[i])
    organelle_prediction.append(model.predict(df))

best_num = -2147483648 # Negative integer limit
best_organelle = "N/A"
for organelle in organelle_prediction:
    val = organelle[1][0][0]
    print(val) # DEBUG
    if val > best_num:
        best_num = val
        best_organelle = organelle[0][0]

if best_organelle == "N/A":
    raise RuntimeError("No best Organelle found. Organelles: {organelle_prediction}")

print(best_organelle)

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
