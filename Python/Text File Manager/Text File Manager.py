from ast import literal_eval # safer version of eval()
from hashlib import sha512 # algorithm used to hash passwords
from getpass import getpass # used so that password is not shown when entered (command line only, IDLE will warn that password will be shown)
from random import randint # used in Generate_Salt()
from os import mkdir,rmdir # create/remove folders as accounts are created/removed

def Generate_Salt(): # used to make dictionary attacks against the hashed passwords more difficult
    key_space = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u",
                 "v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
                 "Q","R","S","T","U","V","W","X","Y","Z","!",'"',"@","#","£","¤","$","%","&","(",")",
                 "[","]","=","+","?","´","`","¨","^","'","*",",",";",".",":","-","_","1","2","3","4",
                 "5","6","7","8","9","0"]
    salt = ""
    for i in range(0,16): #generate 16 character salt
        salt += key_space[randint(0,len(key_space)-1)] # add a character from the key space at random

    return salt

def Hash_Password(salt,password): # hash password using the sha512 algorithm
    hashed_password = (salt[0:8] + password + salt[9:]).encode() #prepend half of the salt to the password; append the other half
    for i in range(0,100000): # hash password 100000 times, makes brute-force attacks significantly longer
        hashed_password = ((sha512(hashed_password)).hexdigest()).encode()
    hashed_password = hashed_password.decode() # byte to str

    return hashed_password
    
def Input_Username_And_Password(mode="login"):
    username = input("Input username: (input 'BACK' to go back)\n>>> ")
    if mode == "create":
        while username in list(users_dict.keys()) and username.upper() != "BACK": # if username already exists
            username = input("Username already taken. Input username: (input 'BACK' to go back)\n>>> ")
    if username.upper() == "BACK":
        print("\n\n")
        return "BACK" # end function
    
    
    password = getpass("\nInput password: (note that characters will not appear)\n>>> ")
    
    if mode == "create":
        password_confirm = getpass("Confirm password: (note that characters will not appear)\n>>> ")
        while password != password_confirm:
            print("\nPasswords do not match!")
            password = getpass("Re-enter password: (note that characters will not appear)\n>>> ")
            password_confirm = getpass("Confirm password: (note that characters will not appear)\n>>> ")

        salt = Generate_Salt()

        hashed_password = Hash_Password(salt,password)

        users_dict[username] = [salt,hashed_password]
        users_file = open("users.txt","w")
        users_file.write(str(users_dict)) # update user.txt (overwrite; if an error were to occur here
                                          # (e.g users_dict is not converted into a string), then all
                                          # users would be deleted
        users_file.close()

        return True # end function

    if mode == "login":
        successful_login = [False,""] # [logged in,username]
        if username in list(users_dict.keys()): # if username exists
                print(username + " in list")
                print(successful_login)
                if users_dict[username][1] == Hash_Password(users_dict[username][0],password): # if password is valid
                    print("Login Successful\n\n")
                    successful_login[0] = "True" # return as str instead of bool since function can return more than 2 values
                    successful_login[1] = username
                else: # username valid, password invalid
                    print("Invalid username and/or password \n(Both username and password are case-sensitive)")
                    successful_login[0] = "False"

                print(successful_login)
        else:
            if username not in list(users_dict.keys()): # delay eventual brute-force attack
                Hash_Password("dummysaltdummysa","dummypassword")
            print("Invalid username and/or password \n(Both username and password are case-sensitive)")
            successful_login[0] = "False" # return as str instead of bool since function can return more than 2 values

        return successful_login # end function


# program start
users_file = open("users.txt","r")
users_dict = literal_eval(users_file.read()) # contains a dictionary with username:[salt,hashedpassword] pairs
users_file.close() # close when not needed

while True:
    print("Text file manager\n")
    print("Enter option:")
    login_or_create_account = input(("[L]ogin \n[C]reate account \n>>>")).upper().replace(" ","")
    
    while login_or_create_account != "L" and login_or_create_account != "C":
        print(("\n'{}' is not valid input.").format(login_or_create_account))
        login_or_create_account = input(("[L]ogin  \n[C]reate account \n>>>")).upper().replace(" ","")

    if login_or_create_account == "C": # create new account
        account_created = Input_Username_And_Password("create")

        if account_created == True:
            print("Account successfully created.\n\n")

    if login_or_create_account == "L": # log into account
        successful_login = Input_Username_And_Password()
        if successful_login == "BACK":
            continue # reset program
        else:
            while successful_login[0] == "False":
                successful_login[0] = Input_Username_And_Password()

        logged_in_user = successful_login[1]

    
                


            
        
