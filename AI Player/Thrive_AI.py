import pyautogui
import pydirectinput # Needed for DirectX games like Thrive as they ignore the virtual keys pyautogui uses.
import time
import numpy as np
import csv
import os
import pandas as pd # For gathering data

pyautogui.FAILSAFE = True # Move mouse to top left of screen to automatically stop.
pyautogui.PAUSE = 0.2 # Minimum time between each pyautogui action

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
@param empty: Will not put any new data in the CSV if empty=True. When paired with new=True, will make a CSV file of name ai_type.csv only with the header.
"""
def convert_to_csv(organelle_count: list[int], ai_type: str, new: bool, additional_name: list[str]=[], additional_data=None, empty=False):
    if new == True:
        data = [["Ammonia", "Glucose", "Phosphates", "Hydrogensulfide", "Oxygen", "Carbondioxide", "Nitrogen", "Sunlight", "Temperature", "Iron", "Speed", "ATP Production", "ATP Consumption", "Population",
                "cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet"]]
        data[0].extend(additional_name)

    
    # Fill data with csv-formated data from log.txt:
    __location__ = os.path.realpath(os.path.dirname(__file__))
    current_data = []
    if not empty: # Allows new 
        with open(__location__ + "/log.txt", 'r') as file:
            for line in file:
                split = line.split(' ')
                if split[0] != "Compounds:\n" and split[0] != "Current" and split[0] != "\n": # Avoid headers
                    current_data.append(split[1])

        # Add to current data:
        for i in organelle_count:
            current_data.append(i)
        if additional_data != None:
            current_data.append(additional_data)

    if new == True: # Start csv file from scratch.
        if current_data != []: # In case empty is called. Do not want an empty line to be added.
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
    #print(r, num_placed) # DEBUG

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
            #print(60 * index_in_ring/(r)) # DEBUG
        else:
            place_rotation = 60 * index_in_ring/(r) - 30 # -30 on odd rings as their hexagons are offset with an edge on the x-axis, but will always have a hexagon along the -30 degree line.
            #print(60 * index_in_ring/(r) - 30) # DEBUG

    # Add to current position:
    center = [1920, 1080]
    place_position = center
    #print("\n", place_position) # DEBUG
    place_position[0] += np.cos(np.deg2rad(place_rotation))*(132*r) # Fine tuned 132 to be the pixel radius whose circles when multiplied by r overlap with at least 3 rings of hexagons (plus the centre when r=0).
    place_position[1] -= np.sin(np.deg2rad(place_rotation))*(132*r)
    #print(place_position, place_rotation) # DEBUG
    #print(np.cos(np.deg2rad(place_rotation))*162, np.sin(np.deg2rad(place_rotation))*162) # DEBUG
    pyautogui.moveTo(place_position[0], place_position[1])
    time.sleep(0.3) # Too fast for game otherwise, game could sometimes think it was placing/clicking in the previous position.
    pyautogui.click(place_position[0], place_position[1])

    #print(num_placed + 1, place_rotation, index_in_ring) # DEBUG
    return num_placed + 1

# Test code to find locations:
# Immediate potential problem found: Different monitors have different aspect ratios and pixel counts. ***
def test_position():
    while True:
        print(pyautogui.position())
        time.sleep(1)

"""
Checks if load.txt contains loaded, indicating the game has finished loading.
"""
def check_loading_completed() -> bool:
    __location__ = os.path.realpath(os.path.dirname(__file__))
    with open(__location__ + "/load.txt", 'r') as file:
            for line in file:
                if line == "Loaded":
                    return loading_complete(__location__)
    return False

"""
Clears load.txt.
"""
def loading_complete(__location__) -> bool:
    with open(__location__ + "/load.txt", 'w', newline='') as file:
            writer = csv.writer(file)
            data = []
            writer.writerows(data)
            return True
    return False

"""
Runs the game for 'quantity' generations, running each generation 12 times, picking one organelle in each time and one loop of no organelles.
Must ensure autosave has been turned off and a Temp game save has already been made (does not matter what is in it, but it WILL BE DELETED/OVERWRITTEN)!
@param quantity The quantity of generations to run for.
"""
def gather_data(quantity: int):
    loaded = False
    time.sleep(2) # Gives time to open game.
    loading_complete(os.path.realpath(os.path.dirname(__file__)))
    # Set infinite compounds and unlimited growth cheats to on.
    pydirectinput.press('f6')
    pyautogui.click(100, 175, duration=0.2)
    pyautogui.click(100, 400, duration=0.2)
    time.sleep(2)

    to_editor()
    num_placed = 1
    organelles = ["cytoplasm", "hydrogenase", "metabolosomes", "thylakoids", "chemosynthesizing proteins", "rusticyanin", "nitrogenase", "toxisome", "flagellum", "perforator pilus", "chemoreceptor", "slime jet", "none"] # No reason to do thylakoids
    organelle_count = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for _ in range(quantity):
        convert_to_csv([], "gathered_data", True, empty=True) # Ensure gathered_data is empty.
        # Save current state with name "Temp"
        pydirectinput.press("esc")
        pyautogui.click(1902, 557, duration=0.1)
        time.sleep(0.1)
        # Write "Temp"
        pydirectinput.keyDown("shift")
        pydirectinput.press("t")
        pydirectinput.keyUp("shift")
        pydirectinput.write("emp", 0.02) # 0.02 a second interval between each character pressed.
        pyautogui.click(3273, 353, duration=0.1)
        pyautogui.click(1620, 1141, duration=0.1)

        for i in range(len(organelles)):
            if i != 3: # No need to do thylakoids
                if organelles[i] != "none":
                    select_part(organelles[i])
                    time.sleep(1)
                    add_part(num_placed)
                
                to_active_stage()
                pyautogui.click(1622, 1166, duration=0.1) # In case "negative ATP warning comes up", will be in loading screen when pressed if warning does not appear.
                while not loaded: # Wait for loading.
                    loaded = check_loading_completed()
                    time.sleep(0.2)

                # Set infinite compounds and unlimited growth cheats to on.
                pydirectinput.press('f6')
                pyautogui.click(100, 175, duration=0.2)
                pyautogui.click(100, 400, duration=0.2)
                time.sleep(2)

                to_editor()
                convert_to_csv([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "gathered_data", False) # Will only use population here so organelle count does not matter.

                # Go to and load "Temp" save
                pydirectinput.press("esc")
                pyautogui.click(1920, 710, duration=0.1)
                pyautogui.click(3273, 284, duration=0.1)
                while not loaded: # Wait for loading.
                    loaded = check_loading_completed()
                    time.sleep(0.2)
        # Convert all paths into a list of their population outcomes:
        __location__ = os.path.realpath(os.path.dirname(__file__))
        data = pd.read_csv(__location__ + "/gathered_data_log.csv")
        populations = data[data.columns[13]].to_list()
        print(populations) # DEBUG

        # Calculate organelle that leads to largest population:
        largest_pop = -1 # Can never be negative so assuming not broken this will always be replaced.
        largest_pop_pos = 0
        for i in range(len(populations)):
            if populations[i] > largest_pop:
                largest_pop = populations[i]
                largest_pop_pos = i
        if largest_pop_pos > 2: # Account for not gathering data on thylakoids.
            largest_pop_pos += 1

        convert_to_csv(organelle_count, "data", False, ["selected"], largest_pop_pos) # Add best path for these environmental variables.
        
        select_part(organelles[largest_pop_pos])
        num_placed = add_part(num_placed)
        organelle_count[largest_pop_pos] += 1
        to_active_stage()
        while not loaded: # Wait for loading.
            loaded = check_loading_completed()
            time.sleep(0.2)

        # Set infinite compounds and unlimited growth cheats to on.
        pydirectinput.press('f6')
        pyautogui.click(100, 175, duration=0.2)
        pyautogui.click(100, 400, duration=0.2)
        time.sleep(2)

        to_editor()
        
    
    # Turn on infinite growth speed and compounds
        # Press F6
        # Move to then click at Point(x=100, y=175) (Infinite Compounds)
        # Move to then click at Point(x=96, y=400) (Unlimited grown speed)
    
    # Go to editor

    # for quantity loops:
        # Save with name "Temp"
            # Press escape
            # Move to then click at Point(x=1902, y=557) (Save menu)
            # Type "Temp"
            # Move to then click at Point(x=3273, y=353) (Save)
            # Move to then click at Point(x=1620, y=1141) (Override previous save)
        # Create list called "generation_pop"
        # For each option "organelle" in organelles to select or not (12 total loops):
            # Select and add organelle
            # Go to run-time
            # Go to editor
            # Save data from log.txt to file "gathered_data.csv"
            # Save population to "generation_pop"
            # Go to load
            # Load "Temp"
                # Press escape
                # Move to then click at Point(x=1910, y=710) (Load menu)
                # Move to then click at Point(x=3273, y=284) (Load)
                # Wait 1 second.
            # *** Check if cheats stay enabled. If not, re-enable them when going back to run-time/active stage.
        # Select and add organelle that led to highest population
        # Go to run-time
        # Go to editor
        # Save data from log.txt to file "data_log.csv"

if __name__ == "__main__":
    # YOU DO NOT NEED TO RUN THIS FILE DIRECTLY. IT IS AN IMPORT FOR THE AGENTS, AND USED DIRECTLY FOR DEBUGGING AND DATASET GENERATION.
    pass # Remove this pass and uncomment section you want to test if that is desired.
    #test_position() # DEBUG
    # gather_data(30)
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
