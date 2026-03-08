import pyautogui
import time
import numpy as np
import csv
import os

pyautogui.FAILSAFE = True # Move mouse to top left of screen to automatically stop.
pyautogui.PAUSE = 0.25 # Minimum time between each pyautogui action

# Function to get from played microbe stage to editor.
def to_editor():
    pyautogui.click(3550, 1857) # Click button to go to editor
    time.sleep(2) # Temp. TODO: Need to find way to know when loading screen is over. ***
    pyautogui.click(3606, 2071) # Skip first page
    pyautogui.click(3606, 2071) # Skip second page, and we're there!

# Converts log.txt file to a csv file for ease of use.
def convert_to_csv(added: list[str], ai_type: str, new: bool):
    if new == True:
        data = [["Ammonia", "Glucose", "Phosphates", "Hydrogensulfide", "Oxygen", "Carbondioxide", "Nitrogen", "Sunlight", "Temperature", "Iron", "Speed", "ATP Production", "ATP Consumption", "Population",
                "cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet"]]
    key_words1 = ["Ammonia", "Glucose", "Phosphates", "Hydrogensulfide", "Production", "Consumption", "Iron"]
    key_words2 = ["Oxygen", "Carbondioxide", "Nitrogen", "Sunlight", "Temperature"]

    # Fill data with csv-formated data from log.txt:
    __location__ = os.path.realpath(os.path.dirname(__file__))
    current_data = []
    with open(__location__ + "/log.txt", 'r') as file:
        for line in file:
            split = line.split(' ')
            if split[0] == "ATP":
                current = split[1][:-1] # ATP has end of name in second column, the rest are first column.
            else:
                current = split[0][:-1] # [:-1] removes colon
            if current == "Speed" or current == "Population":
                current_data.append(split[1]) # Only Speed and Population have data in second column.
            elif current in key_words1:
                current_data.append(split[2]) # Primary data in amount or is ATP-related.
            elif current in key_words2:
                current_data.append(split[6]) # Primary data in ambient.
    
    # Count how many of each organelle are currently on the micro-organism:
    organelle_count = [0]*12
    for organelle in added:
        if organelle == "cytoplasm":
            organelle_count[0] += 1
        elif organelle == "hydrogenase":
            organelle_count[1] += 1
        elif organelle == "metabolosomes":
            organelle_count[2] += 1
        elif organelle == "thylakoids":
            organelle_count[3] += 1
        elif organelle == "chemosynthesizing proteins":
            organelle_count[4] += 1
        elif organelle == "rusticyanin":
            organelle_count[5] += 1
        elif organelle == "nitrogenase":
            organelle_count[6] += 1
        elif organelle == "toxisome":
            organelle_count[7] += 1
        elif organelle == "flagellum":
            organelle_count[8] += 1
        elif organelle == "perforator pilus":
            organelle_count[9] += 1
        elif organelle == "chemoreceptor":
            organelle_count[10] += 1
        elif organelle == "slime jet":
            organelle_count[11] += 1

    # Add to current data:
    for i in organelle_count:
        current_data.append(i)
    
    if new == True:
        data.append(current_data)
        # Convert data into csv file:
        with open(__location__ + "/" + ai_type + "_log.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    else:
        data = [current_data]
        # Convert data into csv file:
        with open(__location__ + "/" + ai_type + "_log.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
    

# Function to get from editor to played microbe stage.
def to_active_stage():
    pyautogui.click(3606, 2071)

# Function to select different cell parts. Takes string of what part to select.
def select_part(organelle: str):
    if organelle == "cytoplasm":
        pyautogui.click(215, 720)
    elif organelle == "hydrogenase":
        # x=203, y=1114
        pyautogui.click(203, 1114)
    elif organelle == "metabolosomes":
        # x=520, y=1114
        pyautogui.click(520, 1114)
    elif organelle == "thylakoids":
        # x=823, y=1121
        pyautogui.click(823, 1121)
    elif organelle == "chemosynthesizing proteins":
        # x=208, y=1404
        pyautogui.click(208, 1404)
    elif organelle == "rusticyanin":
        # x=508, y=1410
        pyautogui.click(508, 1410)
    elif organelle == "nitrogenase":
        # x=825, y=1410
        pyautogui.click(825, 1410)
    elif organelle == "toxisome":
        # x=213, y=1711
        pyautogui.click(213, 1711)
    elif organelle == "flagellum": # From here on requires scroll
        # x=211, y=1370
        pyautogui.moveTo(211, 1380) # Can sometimes start scrolling before moving.
        pyautogui.scroll(-450)
        pyautogui.click(211, 1380)
        pyautogui.scroll(400, 211, 1380) # Scroll back to reset location on organelle list.
    elif organelle == "perforator pilus":
        # x=513, y=1380
        pyautogui.moveTo(513, 1380) # Can sometimes start scrolling before moving.
        pyautogui.scroll(-450)
        pyautogui.click(513, 1380)
        pyautogui.scroll(400, 513, 1380) # Scroll back to reset location on organelle list.
    elif organelle == "chemoreceptor":
        # x=823, y=1380
        pyautogui.moveTo(823, 1380) # Can sometimes start scrolling before moving.
        pyautogui.scroll(-450)
        pyautogui.click(823, 1380)
        pyautogui.scroll(400, 823, 1380) # Scroll back to reset location on organelle list.
    elif organelle == "slime jet":
        # x=206, y=1676
        pyautogui.moveTo(206, 1676) # Can sometimes start scrolling before moving.
        pyautogui.scroll(-450)
        pyautogui.click(206, 1676)
        pyautogui.scroll(400, 206, 1676) # Scroll back to reset location on organelle list.
    else:
        raise ValueError(f"Organelle \"{organelle}\" not known.")

# Function to add part in a spiral around current cell.
def add_part(num_placed: int, place_rotation: float):
    center = [1920, 1080]
    place_position = center
    
    # Add to current position:
    print("\n", place_position)
    place_position[0] += np.cos(np.deg2rad(place_rotation))*162
    place_position[1] -= np.sin(np.deg2rad(place_rotation))*162
    print(place_position)
    print(np.cos(np.deg2rad(place_rotation))*162, np.sin(np.deg2rad(place_rotation))*162)
    pyautogui.click(place_position[0], place_position[1]) # Casted here so we don't lose accuracy in future placement positions

    # Calculate next position:
    # Works for first circle. TODO: Need to find automated way to do expanding circles.
    if num_placed < 6: # First circle
        if (num_placed+1) % 3 == 0:
            place_rotation += 90
        else:
            place_rotation += 45
    return num_placed + 1, place_rotation

# Test code to find locations:
# Immediate potential problem found: Different monitors have different aspect ratios and pixel counts. ***
def test_position():
    while True:
        print(pyautogui.position())
        time.sleep(1)

# PLANNING:

def planner_AI():
    # for 30 generations:
    # Get to editor
    # Give current data to planning agent
    # Run planning agent
    # Make actions agent makes (Actions in the PDDL file are 1:1 with actions we take in game.)
    pass

# BAYES NETS:

def bayes_net_AI():
    pass

# DEEP LEARNING:

def deep_learning_AI():
    pass

if __name__ == "__main__":
    # test_position() # DEBUG
    # time.sleep(3) # To allow user to open Thrive/put in front of all other windows before control of mouse is taken.
    # to_editor()
    convert_to_csv(["cytoplasm"], "bayes_net", True) # Initial micro-organism starts with one cytoplasm.
    # select_part("flagellum")
    # num_placed = 0 # Initial is 0 parts placed.
    # place_rotation = 225 # In degrees. Cell placements move clockwise (subtract from this number.) Initial is 225 degrees.
    
    # num_placed, place_rotation = add_part(num_placed, place_rotation)

# List of locations:
# Point(x=3550, y=1857): Editor button
# Point(x=3606, y=2071): Next button
# Point(x=1920, y=1079): About center of cell
# Point(x=1799, y=1149): About bottom left of initial cytoplasm
# Organelles:
# Point(x=215, y=720): Cytoplasm
# Point(x=203, y=1114): Hydrogenase
# Point(x=520, y=1114): Metabolosomes
# Point(x=823, y=1121): Thylakoids
# Point(x=208, y=1404): Chemosynthesizing proteins
# Point(x=508, y=1410): Rusticyanin
# Point(x=825, y=1410): Nitrogenase
# Point(x=213, y=1711): Toxisome
# After four mouse scroll wheel movements:
# Point(x=211, y=1370): Flagellum
# Point(x=513, y=1380): Perforator Pilus
# Point(x=823, y=1378): Chemoreceptor
# Point(x=206, y=1676): Slime Jet
# There are more but they require nucleus.

# Diameter of cell appears to be 162 pixels