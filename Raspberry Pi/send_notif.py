# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 23:03:36 2019

@author: User
"""

import requests

def bot_sendtext(bot_message):
    
    bot_token = "820989199:AAEPZUzUMZ3tJFTOU729AWGKSzFAl5f4Wlw"
    bot_chatID = "143264607"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    
    requests.get(send_text)
    
    
def getPrevStatus(level_name, bin_name):
    url = "https://bintheredonethatf04.firebaseio.com/"
    
    db_dict = requests.get(url + ".json").json()
    
    bin_status = db_dict[level_name][bin_name]["status"]
    
    return bin_status
    
