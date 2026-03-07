import pyagrum as gum

# Initialization:
bn = gum.BayesNet("Player") # First argument given is the name of the Bayes Net.

# Create nodes for the compounds

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
