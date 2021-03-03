#!/bin/python3

import sqlite3
from hashlib import sha256

MASTER_KEY = "123456"

master_key_input = input ("Please enter master key to enter vault: (q to quit)\n")
    
while master_key_input != MASTER_KEY:
    if master_key_input == "q": 
        print("Exiting")
        break
    master_key_input = input("Sorry. The master key in invalid. Please enther master key againg to enter vault: (q to quit)\n")

print("Master key matches...")

database = sqlite3.connect('vault.db')

if master_key_input == MASTER_KEY:
    try:
        database.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")

def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = database.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)

def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)

    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key +'"')        
    database.execute(command)
    database.commit()
    return create_password(secret_key, service, admin_pass)



while True:
    print("\n"+ "*"*15)
    print("Commands:")
    print("q = quit program")
    print("gp = get password")
    print("sp = store password")
    print("*"*15)
    input_ = input(":")

    if input_ == "q":
        break
    if input_ == "sp":
        service = input("What is the name of the service?\n")
        print("\n" + service.capitalize() + " password created:\n" + add_password(service, MASTER_KEY))
    if input_ == "gp":
        service = input("What is the name of the service?\n")
        print("\n" + service.capitalize() + " password:\n"+get_password(MASTER_KEY, service))
