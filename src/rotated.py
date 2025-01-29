# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 25.04.23
Time: 08:09

"""
import Result_Parser as RP
import Database_Handler as DH
Results_Dict = []
Key = "Us_A2B2C1D0E0F0_592bb_563c7_Tx_Rnd_Rotated"
Results_Dict[Key] = {"Results": RP.Results_Reader(Key)}
DH.Json_Database_Creator(Results_Dict, "Data_Base_Updated.json")