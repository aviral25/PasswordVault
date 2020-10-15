#!/bin/python3

def master_key():
    MASTER_KEY = "123456"

    master_key_input = input ("PLease enter master key to enter vault: (q to quit)\n")
    str = "Master key matches..."
    while master_key_input != MASTER_KEY:
        if master_key_input == "q": 
            str= "Exiting"
            break
        master_key_input = input("Sorry. The master key in invalid. Please enther master key againg to enter vault: (q to quit)\n")
        
    return str