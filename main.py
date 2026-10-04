import pyautogui
from time import sleep
from tkinter import filedialog, Tk
from os import remove, path
from traceback import print_exc
from sys import exit

# Set pyautogui parameters  
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

DEFAULT_DIRECTORY = 'C:/Users/engineer/Desktop/Jacob/AKADP/test/'

import sys

# USE THIS WHEN 
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

    # UNCOMMENT & COMMENT ALL PREVIOUS CODE WHEN DEBUGGING IN IDE MODE
    #return "static/" + relative_path

def name_prompt(cell_names, cell_number, n):
    if (cell_number > n):
        return
    
    new_name = input(f"Insert the name for spectrum {cell_number} >>> ")
    if new_name in cell_names:
        print("This name has already been selected! Please insert a different name for this spectrum!\n")
        name_prompt(cell_names, cell_number, n)
    else:
        cell_names.append(new_name)
        name_prompt(cell_names, cell_number+1, n)
    

def main():
    # Add Instructions
    print("---------------------------------------")
    print("Automated K-Alpha Data Processing")
    print("Jacob Rowe")
    print("---------------------------------------")
    print("STEPS\n")
    print("1. Open all spectrum files (.VGD files) into a new data grid in the Avantage software.")
    print("This can be done by clicking File->Open, then selecting 'Avantage Data Files (*.vgd) in the bottom-right.") 
    print("Select all of the desired spectrums together. This software can process multiple spectrums at a time.\n")
    print("2. In the new data grid, use the mouse to click and drag the horizontal border between the grid and 'Peaks' tab all the way to the top.\n")
    print("3. Follow the software prompts.")
    print("The mouse should start moving automatically. DO NOT USE THE MOUSE OR KEYBOARD UNTIL THE SOFTWARE IS DONE!\n")
    print("The software can't process several graphs with the same save name, you need to insert a unique name for each spectrum.\n")
    print("When inputting file name, you need to add the word 'Survey' (not capitalization sensitive) to save survey scans properly, otherwise it will be treated like a multiplex.\n")
    print("Depth profiles are not supported at this time.\n")
    print("When prompted to save the name for Spectrum [GRAPH_NUMBER], the graphs are numbered from then left to right, then to the next row.")
    print("EXAMPLE:\nSpectrum 1 is at Row 1 Col 1\nSpectrum 2 is at Row 1 Col 2\nSpectrum 3 is at Row 2 Col 1\nSpectrum 4 is at Row 2 Col 2")
    print("---------------------------------------\n")

    # Get Number of Graphs in Datagrid
    # Wait for "Enter"
    num_cells = int(input("How many spectrums are in the grid? >>> "))
    
    # Call recursive name prompt
    cell_names = []
    name_prompt(cell_names, 1, num_cells)

    root = Tk()
    root.attributes("-topmost", True)
    PROJECT_DIRECTORY = filedialog.askdirectory(title="Choose Output Folder!") + "/"
    root.withdraw()

    if (len(PROJECT_DIRECTORY) < 5): exit(1)
    
    # Press on "Avantage Icon in Bottom to Maximize"
    pyautogui.click(resource_path('Avantage Icon Button.png'))
    sleep(3)

    # Click to Maximize First Cell
    data_grid_location = pyautogui.locateCenterOnScreen(resource_path('Avantage Top-Left Spectrum.png'))
    pyautogui.click(data_grid_location[0]+200, data_grid_location[1])

    max_location = pyautogui.locateCenterOnScreen(resource_path('Avantage Max Data Grid.png'))

    # Find Top-Left Spectrum Area
    try:
        top_left_spectrum = pyautogui.locateCenterOnScreen(resource_path('Avantage Top-Left Spectrum.png'))
    except:
        top_left_spectrum = pyautogui.locateCenterOnScreen(resource_path('Avantage Top-Left Spectrum 2.png'))


    for cell in range(num_cells):
        pyautogui.click(max_location[0], max_location[1] + 20)
        pyautogui.click(*max_location)

        # Move to Next Cell
        if (cell != 0):
            if (cell % 2 == 0):
                pyautogui.press('left')
                pyautogui.press('down')
            else:
                pyautogui.press('right')

        spectrum_name = cell_names[cell]

        # Save Screenshot of Spectrum (top_left_spectrum + 8) | (468, 254) -> (1870, 915)
        pyautogui.screenshot(PROJECT_DIRECTORY + spectrum_name + "_Spectrum.png", region=(top_left_spectrum[0]+8, top_left_spectrum[1]-10, 1402, 661))

        # Right-Click on Spectrum -> Processing -> Utilities -> Export as Text File
        pyautogui.click(top_left_spectrum[0]+705, top_left_spectrum[1]+330, button='left')
        pyautogui.click(top_left_spectrum[0]+705, top_left_spectrum[1]+330, button='right') 
        properties_tab = pyautogui.locateCenterOnScreen(resource_path('Avantage Spectrum Properties Button.png'))
        pyautogui.click(*properties_tab)

        # (1072, 727) -> (1283, 910) | (1480, 846)
        pyautogui.click(properties_tab[0]+211, properties_tab[1]+183)
        pyautogui.click(properties_tab[0]+408, properties_tab[1]+119)

        # Click on Filename & Set Saved File Name
        filename_area = pyautogui.locateCenterOnScreen(resource_path('Avantage Dump Filename Area.png'))
        pyautogui.click(filename_area[0], filename_area[1]+15)
        pyautogui.typewrite(PROJECT_DIRECTORY + spectrum_name + "_temp.txt")

        # Set File Type to "Excel"
        normal_location = pyautogui.locateCenterOnScreen(resource_path('Avantage Dump Normal Button.png'))
        pyautogui.click(*normal_location)
        pyautogui.click(normal_location[0], normal_location[1]+30)

        # Click on "Save"
        pyautogui.click(resource_path('Avantage OK Button.png'))

        min_number = 0
        max_number = 0

        # Format Created File
        with open(PROJECT_DIRECTORY + spectrum_name + "_temp.txt", "r") as file:
            data = file.readlines()
            file.seek(0)

            first_line = data.index("eV\t\n")

        if "survey" in spectrum_name.lower():
            with open(PROJECT_DIRECTORY + spectrum_name + ".txt", "w") as file:
                file.write(f"Element ; Region 1 of 1; Depth Cycle 1 of 1; Time Per Step 50; Sweeps 10; Anode Al; Photon Energy 1486.6; XPS;\n")
                file.write("Lens Type OmniA3; Lens Area Small;\n")


                for line in data[first_line+1:-1]:
                    data_update = line.split()

                    if "inf" in data_update[1]:
                        continue
                    
                    file.write(str(round(1486.6 - float(data_update[0]), 3)) + '\t' + str(round(float(data_update[1]))) + '\n')
                
        else:
            min_number = 0
            max_number = 0

            # Calculate difference in min and max
            for line in data[first_line+1:-1]:
                data_update = line.split()

                if min_number == 0 or max_number == 0:
                    min_number = float(data_update[1])
                    max_number = min_number
                else:
                    if float(data_update[1]) < min_number:
                        min_number = float(data_update[1])
                    elif float(data_update[1]) > max_number:
                        max_number = float(data_update[1])

            with open(PROJECT_DIRECTORY + spectrum_name + ".txt", "w") as file:
                file.write("Cycles 1; Regions 1; Anode Al; Photon Energy 1486.6; XPS;\n")

                diff = max(round(max_number - min_number), 1)
                file.write(spectrum_name + f"\n{diff}\n")
                file.write(f"Element {spectrum_name}; Region 1 of 1; Depth Cycle 1 of 1; Time Per Step 200; Sweeps 10; Anode Al; Photon Energy 1486.6; XPS;\n")

                for line in data[first_line+1:-1]:
                    data_update = line.split()
                    
                    file.write(str(round(1486.6 - float(data_update[0]), 3)) + '\t' + str(round(float(data_update[1]))) + '\n')
        
                
        # DEBUG
        remove(PROJECT_DIRECTORY + spectrum_name + "_temp.txt")
        
    # Close GUI, Files, Return File Success
    exit(0)

    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_exc()
        input("Press enter to exit!")