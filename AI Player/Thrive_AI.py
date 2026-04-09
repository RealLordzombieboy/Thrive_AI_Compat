import pyautogui
import time
import numpy as np
import csv
import os

pyautogui.FAILSAFE = True # Move mouse to top left of screen to automatically stop.
pyautogui.PAUSE = 0.3 # Minimum time between each pyautogui action

# Function to get from played microbe stage to editor.
def to_editor():
    pyautogui.click(3550, 1857) # Click button to go to editor
    time.sleep(4) # Temp. TODO: Need to find way to know when loading screen is over. ***
    pyautogui.click(3606, 2071) # Skip first page
    pyautogui.click(3606, 2071) # Skip second page, and we're there!

# Converts log.txt file to a csv file for ease of use.
"""
@param added: Integer count of organelles currently on microbe (0 if none.)
Order is: "cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet".
Must be exactly 12 integers long.
"""
def convert_to_csv(organelle_count: list[int], ai_type: str, new: bool):
    if new == True:
        data = [["Ammonia", "Glucose", "Phosphates", "Hydrogensulfide", "Oxygen", "Carbondioxide", "Nitrogen", "Sunlight", "Temperature", "Iron", "Speed", "ATP Production", "ATP Consumption", "Population",
                "cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet"]]

    # Fill data with csv-formated data from log.txt:
    __location__ = os.path.realpath(os.path.dirname(__file__))
    current_data = []
    with open(__location__ + "/log.txt", 'r') as file:
        for line in file:
            split = line.split(' ')
            if split[0] != "Compounds:\n" and split[0] != "Current" and split[0] != "\n": # Avoid headers
                current_data.append(split[1])

    # Add to current data:
    for i in organelle_count:
        current_data.append(i)
    
    if new == True: # Start csv file from scratch.
        data.append(current_data)
        # Convert data into csv file:
        with open(__location__ + "/" + ai_type + "_log.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    else: # Append to current csv file data.
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
"""
@param num_placed must start at 1 as we start with one organelle in r = 0. Can be used to place in specific positions, so if the initial organelle
is removed then num_placed = 0 will place at that location.
"""
def add_part(num_placed: int):
    if num_placed == 0:
        r = 0
    else:
        r = np.floor((3+np.sqrt(12*(num_placed)-3))/6) # See README for derivation. Finds the ring # such that center is ring 0.
    print(r, num_placed) # DEBUG

    # Calculate next position:
    # # Works for first circle. TODO: Need to find automated way to do expanding circles.
    # if num_placed < 6: # First circle
    #     if (num_placed+1) % 3 == 0:
    #         place_rotation += 90
    #     else:
    #         place_rotation += 45
    
    # A more automated way to deal with placement:
    if (r != 0):
        # place_rotation = 60 degrees * floor(index_in_ring/current_ring) # st index_in_ring and current_ring start at 0.
        index_in_ring = num_placed - 1
        index_in_ring -= 6*((r-1)*r/2) # Subtracts 6 * the sum of all rings from 1 to r-1.
        if r % 2 == 0:
            place_rotation = 60 * index_in_ring/(r) # Not -30 on even rings as they have hexagons on the x-axis.
            print(60 * index_in_ring/(r)) # DEBUG
        else:
            place_rotation = 60 * index_in_ring/(r) - 30 # -30 on odd rings as their hexagons are offset with an edge on the x-axis, but will always have a hexagon along the -30 degree line.
            print(60 * index_in_ring/(r) - 30) # DEBUG

    # Add to current position:
    center = [1920, 1080]
    place_position = center
    #print("\n", place_position) # DEBUG
    place_position[0] += np.cos(np.deg2rad(place_rotation))*(132*r) # Fine tuned 132 to be the pixel radius whose circles when multiplied by r overlap with at least 3 rings of hexagons (plus the centre when r=0).
    place_position[1] -= np.sin(np.deg2rad(place_rotation))*(132*r)
    print(place_position, place_rotation) # DEBUG
    #print(np.cos(np.deg2rad(place_rotation))*162, np.sin(np.deg2rad(place_rotation))*162) # DEBUG
    pyautogui.moveTo(place_position[0], place_position[1])
    time.sleep(0.3) # Too fast for game otherwise, game could sometimes think it was placing/clicking in the previous position.
    pyautogui.click(place_position[0], place_position[1])

    print(num_placed + 1, place_rotation, index_in_ring) # DEBUG
    return num_placed + 1

# Test code to find locations:
# Immediate potential problem found: Different monitors have different aspect ratios and pixel counts. ***
def test_position():
    while True:
        print(pyautogui.position())
        time.sleep(1)

if __name__ == "__main__":
    # YOU DO NOT NEED TO RUN THIS FILE DIRECTLY. IT IS AN IMPORT FOR THE AGENTS, AND USED DIRECTLY FOR DEBUGGING AND DATASET GENERATION.
    pass # Remove this pass and uncomment section you want to test if that is desired.
    # test_position() # DEBUG
    # time.sleep(3) # To allow user to open Thrive/put in front of all other windows before control of mouse is taken.
    # to_editor()
    #convert_to_csv([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "bayes_net", True) # Initial micro-organism starts with one cytoplasm.
    #convert_to_csv([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "deep_learning", False) # DEBUG

    # Test Hexagonal Spiral Placement:
    # num_placed = 1
    # time.sleep(2)
    # for i in range(30):
    #     time.sleep(0.3)
    #     num_placed = add_part(num_placed)
    #     print("\n",end="")

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
