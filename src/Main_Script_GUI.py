# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 07.04.22
Time: 18:17

"""
import numpy as np
import Key_Parser as KP
import Key_Generator as KG
import Database_Handler as DH
import Result_Parser as RP
import Meta_reader as MR
import Load_Creator as LC
import Key_Folder_Creator as KFC
import Geom_Generator as GG
import Abaqus_Runner as AR
import Strain_Result_Check as SRC
import os
from appJar import gui
import threading
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    pass  #

def run_script(btn):
    threading.Thread(target=main_process, daemon=True).start()
    if app.getCheckBox("Download Results?"):
        print("User has opted to download the results.")

def upload_file(btn):
    fileTypeDict = {
        "Upload Load File": ("Text files", "*.txt"),
        "Upload Materials File": ("INP files", "*.inp"),
        "Upload Orientation File": ("Text files", "*.txt"),
        "Upload Geometry File": ("INP files", "*.inp")
    }
    title, fileTypes = f"Open {btn.split()[-2]}", fileTypeDict[btn]
    file_path = app.openBox(title=title, fileTypes=[fileTypes], asFile=False)
    app.setLabel(f"{btn.lower().replace(' ', '_')}_path", file_path if file_path else "No file selected")


def upload_load_file(btn): upload_file(btn)
def upload_materials_file(btn): upload_file(btn)
def upload_orientation_file(btn): upload_file(btn)
def upload_geometry_file(btn): upload_file(btn)


def main_process():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    Results_Dict = DH.Read_Database_From_Json("Data_Base.json")
    load_cases = "sigdata1.txt"
    loads = np.genfromtxt(load_cases)
    Source_Path = os.getcwd()
    os.chdir('..')
    Current_Path = os.getcwd()

    for counter, load in enumerate(loads):
        Key = KG.Key_Generator(load)
        if Key in Results_Dict.keys():
            continue
        else:
            KFC.Create_Sub_Folder(Key)
            scaling_factor = 80
            scaled_load = load * scaling_factor
            Max_Strain = 0
            itertation = 0
            Lower_Strain_Limit = 0.0001
            Upper_Strain_Limit = 100
            while (Upper_Strain_Limit < Max_Strain or Lower_Strain_Limit > Max_Strain ):
                itertation += 1
                LC.Load_File_Generator(scaled_load, Key)
                GG.Abaqus_Input_Generator(Key)
                AR.Abaqus_Runner(Key, 6)
                Max_Strain = SRC.Max_Strain_Finder(Key)
                if Max_Strain < Lower_Strain_Limit:
                    scaling_factor *= 1.05
                    scaled_load = load * scaling_factor

                elif Max_Strain > Upper_Strain_Limit:
                    scaling_factor *= 0.95
                    scaled_load = load * scaling_factor

            #Insert Results to the Data Base
            Results_Dict[Key] = {"Meta_Data": {
                                  **MR.Meta_reader(Key),
                                 "Scaling_Factor": scaling_factor,
                                 "Initial_Load": load.tolist(),
                                 "Applied_Load": scaled_load.tolist(),
                                 "Max_Total_Strain": Max_Strain,
                                    },
                                 "Results": RP.Results_Reader(Key)}

        DH.Json_Database_Creator(Results_Dict, "Data_Base_Updated.json")
    app.queueFunction(app.setTextArea, "output", "\nProcess completed.")


app = gui("Simulation GUI", "600x400")
app.setFont(12, "Arial")
app.setBg("white")
app.setPadding([8, 8])
app.setInPadding([5, 5])

app.addLabel("instruction", "Upload Input Files:", colspan=2)

button_width = 20
label_width = 30
file_buttons = ["Upload Load File", "Upload Materials File", "Upload Orientation File", "Upload Geometry File"]

for index, button in enumerate(file_buttons, start=1):
    app.addButton(button, upload_file, row=index, column=0)
    app.setButtonWidth(button, button_width)

    label_key = f"{button.lower().replace(' ', '_')}_path"
    app.addLabel(label_key, "No file selected", row=index, column=1)
    app.setLabelWidth(label_key, label_width)
    app.setLabelRelief(label_key, "groove")  # Adds a border effect to the label
    app.setLabelHeight(label_key, 2)  # Optional: Adjust if you want more vertical space
    app.setLabelAlign(label_key, "west")  # Aligns text to the west/left side

app.addCheckBox("Download Results", row=len(file_buttons) + 1, column=0)
app.setCheckBoxBg("Download Results", "white")
app.addCheckBox("Upload to Database*", row=len(file_buttons) + 1, column=1)
app.setCheckBoxBg("Upload to Database*", "white")
app.addLabel("db_info", "* Requires pre-existing username and password in the system.", row=len(file_buttons) + 3, colspan=2)
app.setLabelFont("db_info", size=12, family="Arial")
app.addButton("Run Simulations", run_script, row=len(file_buttons) + 2, colspan=2)
app.setButtonBg("Run Simulations", "lightblue")
app.setButtonFg("Run Simulations", "black")
app.go()