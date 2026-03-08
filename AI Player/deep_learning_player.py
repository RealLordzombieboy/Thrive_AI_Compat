import Thrive_AI
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib as plt
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Notes:
# Added selected column to the end of deep_learning_player's CSV file which will be the game's recommended
# option for the initial dataset.

"""
Converts selection number to string Thrive_AI.select_part() can accept.
"""
def to_selection(selection: int):
    match selection:
        case 0:
            return "cytoplasm"
        case 1:
            return "hydrogenase"
        case 2:
            return "metabolosomes"
        case 3:
            return "thylakoids"
        case 4:
            return "chemosynthesizing proteins"
        case 5:
            return "rusticyanin"
        case 6:
            return "nitrogenase"
        case 7:
            return "toxisome"
        case 8:
            return "flagellum"
        case 9:
            return "perforator pilus"
        case 10:
            return "chemoreceptor"
        case 11:
            return "slime jet"


"""
Takes in data from deep_learning_log.csv and outputs what option to choose for current generation.
"""
class Model(nn.Module):
    # 26 input features from CSV file. 12 actions (which organelle to select and add. Only one for now.)
    # From my experience having inner layers be at least double the first layer is a good starting point.
    def __init__(self, features=26, h1=52, h2=52, actions=12):
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

# # Evaluate on test dataset:
# with torch.no_grad():
#     y_eval = model.forward(X_test)
#     loss = criterion(y_eval, y_test)

# with torch.no_grad():
#     for i, data in enumerate(X_test):
#         y_val = model.forward(data)

#         print(f"{y_test[i]}")

# Start:
current_data = data.drop("selected", axis=1).iloc[0] # Get header and initial data which is always on first line.
current_data = current_data.values
current_data = torch.FloatTensor(current_data)

with torch.no_grad():
    y_val = model.forward(current_data)
    selection = y_val.argmax().item()
    print(selection, to_selection(selection))

# Loop through DEMO's 5 more generations

