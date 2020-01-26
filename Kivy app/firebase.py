# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 18:12:53 2019

@author: User
"""

import requests

def getBinMessage_Info(level_name, bin_name):
    url = "https://bintheredonethatf04.firebaseio.com/"
    
    db_dict = requests.get(url + ".json").json()
    
    dict_bin_info = db_dict[level_name][bin_name]
    dict_message = db_dict["message"]
    dict_color = db_dict["bin_color"]
    
    bin_ack = dict_bin_info["ack"]
    bin_status = dict_bin_info["status"]
    location = dict_bin_info["location"]
    
    #get the color of the bin and the message to display
    if bin_ack == "N" and bin_status != "not full, no spill":
        color = "red"
        message = dict_message["acknowledgement"]
        
    elif bin_ack == "Y" and bin_status != "not full, no spill":
        color = "yellow"
        message = dict_message["report"]
        
    else:
        color = "green"
        message = "I'm Good! :)"
    
    #add the information of the bin in the message
    message = message.replace("*location*",location)
    
    status = bin_status.split(", ")
    if status[0] == "full":
        message += "Please empty the bin as it is full.\n"
            
    if status[1] == "spill":
        message += "Please bring cleaning equipment as it is wet.\n"
    
    dict_bin_info["color"] = color
    
    return dict_bin_info, dict_color[color], message

def updateBin_ack(level_name, bin_name, reset = False):
    url = "https://bintheredonethatf04.firebaseio.com/"
    
    bin_url = url + "/"+ str(level_name) + "/" + str(bin_name) 
    
    if not reset: 
        requests.patch(bin_url + ".json", json = {"ack": "Y"})
        print("updated")
    else:
        requests.patch(bin_url + ".json", json = {"ack": "N"})
        
        
def getWarning():
    url = "https://bintheredonethatf04.firebaseio.com/"
    
    db = requests.get(url + ".json").json()
    
    list_warning_levels = []
    
    #get the status of the levels that requires attention
    for level_num in range(1,4):
        level_name = "l" + str(level_num)
        
        for bin_num in range(1,4):
            bin_name = "bin" + str(bin_num)
            bin_status = db[level_name][bin_name]["status"]
            
            if bin_status != "not full, no spill":
                if level_name not in list_warning_levels:
                    list_warning_levels.append(level_name)

    return list_warning_levels
    