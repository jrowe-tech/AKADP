import pyautogui
import clipboard
from time import sleep
from tkinter import filedialog, Tk
from os import remove, path

# Set pyautogui parameters  
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

DEFAULT_DIRECTORY = 'C:/Users/engineer/Desktop/Jacob/AKADP/test/'

import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

def resource_alt(relative_path):
    return "static/" + relative_path

def main():
    root = Tk()
    root.attributes("-topmost", True)
    PROJECT_DIRECTORY = filedialog.askdirectory(title="Choose Output Folder!") + "/"
    root.withdraw()

    if (len(PROJECT_DIRECTORY) < 5): exit(1)
    
    # Press on "Avantage Icon in Bottom to Maximize"
    pyautogui.click(resource_alt('Avantage Icon Button.png'))
    sleep(2)

    peak_locations = []

    # Locate if any unprocessed spectrums exist
    try:
        peak_locations += [(location[0]+(location[2]//2), location[1]+(location[3]//2)) for location in pyautogui.locateAllOnScreen(resource_alt('Avantage Activated Peak.png'))] 
    except:
        pass

    try:
        [(location[0]+(location[2]//2), location[1]+(location[3]//2)) for location in pyautogui.locateAllOnScreen(resource_alt('Avantage Saved Peaks.png'))]
    except:
        pass

    if (len(peak_locations) == 0): exit(1)

    pyautogui.click(*peak_locations[0])

    # Locate + Cache "Scan"
    scan_location = ()
    try:
        scan_location = pyautogui.locateCenterOnScreen(resource_alt('Avantage Scan Tab.png'))
    except:
        try:
            scan_location = pyautogui.locateCenterOnScreen(resource_alt('Avantage Highlighted Scan Tab.png'))
        except:
            scan_location = pyautogui.locateCenterOnScreen(resource_alt('Avantage Alternative Scan Button.png'))
    
    # Locate + Cache all Depth Profiles
    depth_profiles = []
    try:
        depth_profiles += [(location[0]+(location[2]//2), location[1]+(location[3]//2)) for location in pyautogui.locateAllOnScreen(resource_alt('Avantage Depth Profile Icon.png'))]
    except:
        pass

    try:
        depth_profiles += [(location[0]+(location[2]//2), location[1]+(location[3]//2)) for location in pyautogui.locateAllOnScreen(resource_alt('Avantage Highlighted Depth Profile Icon.png'))]
    except:
        pass

    
    # NOTE: May need to uncomment in future
    # pyautogui.click(*data_grid_tab_location)
    for spectrum_location in peak_locations:

        # Click on the Spectrum We Want
        pyautogui.click(*spectrum_location)

        # Click on "General" Tab
        pyautogui.click(scan_location[0] + 40, scan_location[1])

        # Click on "Name" Section (w/ +200px X Offset)
        name_location = pyautogui.locateCenterOnScreen(resource_alt('Avantage Name Area.png'))
        pyautogui.click(name_location[0] + 200, name_location[1])

        # Click Control-A -> Control-C -> Copy File Name to Clipboard
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')

        # Extract Name of Spectrum File
        spectrum_name = clipboard.paste()

        # Click on 'Scan' Tab for Spectrum
        pyautogui.click(*scan_location)

        # Save Screenshot of Spectrum Parameters (40,730) -> (430,986)
        pyautogui.screenshot(PROJECT_DIRECTORY + spectrum_name + "_Parameters.png", region=(40, 730, 390, 256))

    # Close GUI, Files, Return File Success
    exit(0)

    

if __name__ == "__main__":
    main()