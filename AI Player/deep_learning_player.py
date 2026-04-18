import os
import pandas as pd
from sklearn.model_selection import train_test_split
import Thrive_AI
import time
import torch
import torch.nn as nn
import torch.nn.functional as F

# Notes:
# Added selected column to the end of deep_learning_player's CSV file which will be the game's recommended
# option for the initial dataset.

"""
Takes in data from deep_learning_log.csv and outputs what option to choose for current generation.
"""
class Model(nn.Module):
    # 26 input features from CSV file. 12 actions (which organelle to select and add. Only one for now.)
    # From my experience having inner layers be at least double the first layer is a good starting point.
    def __init__(self, features=26, h1=52, h2=52, actions=13):
        super().__init__()
        self.fc1 = nn.Linear(features, h1)
        self.fc2 = nn.Linear(h1, h2)
        self.out = nn.Linear(h2, actions)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.out(x)

        return x

model = Model()
__location__ = os.path.realpath(os.path.dirname(__file__))
data = pd.read_csv(__location__ + "/deep_learning_log.csv")

X = data.drop("selected", axis=1)
y = data["selected"]

X = X.values
y = y.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)

# Convert X and Y's features into tensors
X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)
y_train = torch.LongTensor(y_train)
y_test = torch.LongTensor(y_test)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Train model:
epochs = 10
losses = []
for i in range(epochs):
    y_pred = model.forward(X_train)

    loss = criterion(y_pred, y_train)

    losses.append(loss.detach().numpy())

    #print(f"Epoch: {i}; loss: {loss}") # DEBUG

    # Back propagation:
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Start:
time.sleep(2) # To give time for the user to open Thrive window before mouse control is taken. BE CAREFUL, MOVE TO ANY CORNER SEVERAL TIMES TO FORCE STOP PROGRAM.
Thrive_AI.turn_on_cheats()
Thrive_AI.to_editor()

selection = 0
current_organelles = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
num_placed = 1

# Loop through 20 generations
for i in range(20):
    Thrive_AI.convert_to_csv(current_organelles, "deep_learning", False) # Requires manually setting what the optimal solution was, or delete these after each run.
    current_data = data.drop("selected", axis=1).iloc[len(data) - 1] # Get header and current data which is always on first and last line, respectively.
    current_data = torch.FloatTensor(current_data.values)

    with torch.no_grad():
        y_val = model.forward(current_data)
        selection = y_val.argmax().item()
    if selection != 12: # If selection == 12 then this is the inaction action (add no parts.)
        current_organelles[selection] += 1
        Thrive_AI.select_part(selection)
        time.sleep(1)
        num_placed = Thrive_AI.add_part(num_placed)
    Thrive_AI.to_active_stage()
    Thrive_AI.to_editor()
