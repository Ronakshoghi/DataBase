# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 28.07.22
Time: 10:01

"""
import json
import Database_Handler as DC
import itertools
import Database_Handler as DH

Translate_Dict = DH.Read_Database_From_Json("System_Key_Translator.json")

Current_Dict_1 = DC.Read_Database_From_Json("Data_Base_Updated1.json")
Current_Dict_2 = DC.Read_Database_From_Json("Data_Base_Updated2.json")
Current_Dict_3 = DC.Read_Database_From_Json("Data_Base_Updated3.json")
Final_Dic = {**Current_Dict_1, **Current_Dict_2, **Current_Dict_3}

for key in list(Final_Dic.keys()):
    if key in Translate_Dict:
        Final_Dic[Translate_Dict[key]] = Final_Dic.pop(key)

with open('Data_Base_pwfl20_Complete.json', 'w') as fd:
    json.dump(Final_Dic, fd)

TobeDeleted = []

counter = 0

#Find how many load cases converged.
for key in list(Final_Dic.keys()):
    Max_Strain = Final_Dic[key]["Max_Strain"]
    if Max_Strain > 0.04:
        counter += 1
    else:
        print(key)
        del Final_Dic[key]

print (counter)
print(len(Final_Dic))
with open('Data_Base_pwfl20.json', 'w') as fd:
    json.dump(Final_Dic, fd)