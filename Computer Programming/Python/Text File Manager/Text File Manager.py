from ast import literal_eval # safer version of eval()
from hashlib import sha512 # algorithm used to hash passwords
from getpass import getpass # used so that password is not shown when entered (command line only, will show the password in IDLE)
from random import randint # used in Generate_Salt()
from os import mkdir # create folders as accounts are created
from os import listdir # list all text files in a user's folder
from os import remove # remove files when requested by user
from shutil import rmtree # remove folders as accounts are deleted

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

def Remove_Useless_Spaces(username): #e.g " real admin  " -> "real admin", used to avoid potential problems with folder generation and access
    if username == "":
        return username
    while username[0] == " ":
        username = username[1:] # remove spaces before first non-space character
        if len(username) == 0:
            return username
    while username[-1] == " ": # currently does not work
        username = username[:-1] # remove spaces after last non-space character

    return username

def Input_Password(prompt, password_confirm = False, create_account = False, recursive_call = False):
    # prompt should not start with "Input", "Re-enter", etc., since this will be added later in the
    # function through confirm_word
    confirm_word = "Input " if recursive_call == False else "Re-enter "
    
    loop = True
    while loop:
        print("\n(Leave password blank to cancel)")
        password = Remove_Useless_Spaces(getpass(confirm_word + prompt + "\n>>> "))
        if password == "":
            return "BACK"
        
        if create_account:
            if len(password) < 8:
                print("Password is too short; should be at least 8 characters long\n")
                continue
            elif len(password) > 100:
                print("Password is too long; should be less than 100 characters long\n")
                continue
            password_confirm = True

        if password_confirm:
            password_reenter = Input_Password(prompt,recursive_call = True) #recursive
            if password_reenter == password:
                return password
            else:
                if password_reenter == "BACK":
                    return "BACK"
                print("Passwords do not match!\n")
                continue # prompt user to input password again, and re-enter

        return password # for normal login and recursive calls; password_confirm and create_account == False

def Check_For_Banned_Characters(file_or_user_name="file",name="INPUT"):
    banned_characters = ["/","\\",":","?","<",">","|","*",'"']
    if name == "INPUT": # no string is given to the function
        name = input("Input {}name: (Leave blank to cancel)\n>>> ".format("user" if file_or_user_name.upper() == "USER" else "file "))
        
    while True:
        banned_char_included = False
        for banned_char in banned_characters:
            if banned_char in name:
                banned_char_included = True
                break
        if banned_char_included:
            print("{}name cannot contain any of the following characters:".format("User" if file_or_user_name.upper() == "USER" else "File "))
            print(", ".join([char for char in banned_characters]))
            name = input("Input {}name: (Leave blank to cancel)\n>>> ".format("User" if file_or_user_name.upper() == "USER" else "File "))
        else:
            break
    return name
        
def Input_Username_And_Password(mode="login"):
    banned_characters = ["/","\\",":","?","<",">","|","*",'"']
    
    username = Remove_Useless_Spaces(Check_For_Banned_Characters("user"))
    if username == "":
        return "BACK" # end function
    
    if mode == "create":
        username_not_accepted = True
        while username_not_accepted:
            if username in list(users_dict.keys()):
                print("Username already taken.")
                username = Remove_Useless_Spaces(Check_For_Banned_Characters("user"))
            elif username == "BACK":
                print("Username cannot be 'BACK'.")
                username = Remove_Useless_Spaces(Check_For_Banned_Characters("user"))
            else:
                username_not_accepted = False
                
    if username == "":
        return "BACK" # end function
    
    if mode == "create":
        password = Input_Password("password (8-100 characters): (note that characters will not appear)",create_account=True)
        while password == False:
            password = Input_Password("password (8-100 characters): (note that characters will not appear)",create_account=True)
        if password == "BACK":
            return "BACK"

        salt = Generate_Salt()
        hashed_password = Hash_Password(salt,password)

        users_dict[username] = [salt,hashed_password]
        users_file = open("users.txt","w")
        users_file.write(str(users_dict)) # update user.txt (overwrite; if an error were to occur here
                                          # (e.g users_dict is not converted into a string), then all
                                          # users would be deleted
        users_file.close()
        mkdir("Files\\"+username) # create folder 

        return True # end function

    if mode == "login":
        password = Input_Password("password: (note that characters will not appear)")
        if password == "BACK":
            return "BACK"
        
        successful_login = [False,""] # [logged in,username]
        if username in list(users_dict.keys()): # if username exists
                if users_dict[username][1] == Hash_Password(users_dict[username][0],password): # if password is valid
                    successful_login[0] = "True" # return as str instead of bool since function can return more than 2 values
                    successful_login[1] = username
                else: # username valid, password invalid
                    print("\nInvalid username and/or password \n(Both username and password are case-sensitive)")
                    successful_login[0] = "False"
                    
        else:
            if username not in list(users_dict.keys()): # delay eventual brute-force attack
                Hash_Password("dummysaltdummysa","dummypassword")
            print("\nInvalid username and/or password \n(Both username and password are case-sensitive)")
            successful_login[0] = "False" # return as str instead of bool since function can return more than 2 values

        return successful_login # end function

def List_Files(files):
    print("Files in your folder:")
    for file in files:
        print(("'{}'{}").format(file,"," if file != files[-1] else ""),end=" ")

def Choose_Lines_Input(): # for the "Choose line(s)" edit mode
    global text, text_not_accepted
    text = input(">>> ").split(",",1)
    text_not_accepted = True

# program start
users_file = open("users.txt","r")
try:
    users_dict = literal_eval(users_file.read()) # contains a dictionary with username:[salt,hashedpassword] pairs
except SyntaxError: # e.g if users_file is empty due to error when updating it (when accounts are created/deleted)
    users_dict = {}
users_file.close() # close when not needed

logged_in = False

while True:
    if not logged_in:
        print("\n\nText file manager\n")
        print("Enter option:")
        login_or_create_account = input(("[L]ogin \n[C]reate account \n[E]xit \n>>> ")).upper().replace(" ","")
        print()
        
        while login_or_create_account not in ["L","C","E","LOGIN","CREATE","CREATEACCOUNT","EXIT"]:
            print("Invalid input.")
            login_or_create_account = input(("[L]ogin  \n[C]reate account \n[E]xit \n>>> ")).upper().replace(" ","")
            print()

        if login_or_create_account in ["L","LOGIN"]: # log into account
            successful_login = Input_Username_And_Password()
            while successful_login[0] == "False":
                successful_login = Input_Username_And_Password()
            if successful_login == "BACK":
                continue # go back to menu

            logged_in_user = successful_login[1]
            logged_in = True
            print("\nSuccessfully logged in as " + logged_in_user)
            
        elif login_or_create_account in ["C","CREATE","CREATEACCOUNT"]: # create new account
            account_created = Input_Username_And_Password("create")

            if account_created == True:
                print("\nAccount successfully created.\n\n")

        else: # login_or_create_account in ["E","EXIT"]
            exit()
            
    elif logged_in:
        files = listdir("Files\\" + logged_in_user)
        print("\n\nEnter option:")
        user_option = (input("[L]ist your files \n[C]reate new text file \n[R]ead file" +
                                "\n[E]dit file \n[D]elete file \n[LO]g out \n\n[CHANGE] password \n[DELETE ACCOUNT] \n>>> ").upper()).replace(" ","")
        print() # \n
        while (user_option not in ["L","C","R","E","D","LO","DELETEACCOUNT",
                                   "LIST","CREATE","READ","EDIT","DELETE",
                                   "LOGOUT","LS","RM","DEL","NEW","CHANGE",
                                   "CHANGEPASSWORD"]):
            print("Invalid input.")
            user_option = (input("[L]ist your files \n[C]reate new text file \n[R]ead file" +
                                "\n[E]dit file \n[D]elete file \n[LO]g out \n\n[CHANGE] password \n[DELETE ACCOUNT] \n>>> ").upper()).replace(" ","")
            
        if user_option in ["L","LIST","LS"]:
            List_Files(files)

        elif user_option in ["C","CREATE"]:
            while True:
                file_name = Check_For_Banned_Characters()
                if file_name+".txt" in files:
                    print()
                    print("File {}.txt already exists.".format(file_name))
                    print()
                break

            if file_name != "":
                open("Files\\" + logged_in_user + "\\" + file_name +".txt", "w").close() # create blank file
                print()
                print("File '" + file_name + ".txt' has been created.")

        elif user_option in ["R","READ"]:
            List_Files(files)
            file_to_open = input("\nWhat file would you want to open?(case-sensitive) \n>>> ")
            print() # \n
            if file_to_open == "":
                print("Returning to menu...")
            elif file_to_open not in files:
                print("File '" + file_to_open + "' is not in your folder. Returning to menu...")

            else:
                print("Contents of " + file_to_open + ":")
                file = open("Files\\"+logged_in_user+"\\"+file_to_open,"r")
                print('"""\n' + file.read() + '\n"""')
                file.close()
                

        elif user_option in ["E","EDIT"]:
            List_Files(files)
            file_to_open = input("\nWhat file would you want to edit?(case-sensitive) \n>>> ")
            print() # \n
            if file_to_open == "":
                print("Returning to menu...")
            elif file_to_open not in files:
                print("File '" + file_to_open + "' is not in your folder. Returning to menu...")
            else:
                mode = (input("Select editing mode: \n[A]ppend \n[C]hoose line(s) \n>>> ").upper()).replace(" ","")
                print() # \n
                while mode.upper() not in ["A","C","APPEND","CHOOSE",""]:
                    mode = (input("Invalid input. \nSelect editing mode: \n[A]ppend \n[C]hoose line(s) \n>>> ").upper()).replace(" ","")

                if mode == "":
                    continue # cancel
                
                elif mode in ["A","APPEND"]:
                    with open("Files\\"+logged_in_user+"\\"+file_to_open,"r") as file:
                        file_lines = file.readlines()

                    print("\n-----FILE START-----")
                    for index in range(0,len(file_lines)):
                        print(index,file_lines[index],end="")
                    print("-----FILE   END-----\n")
                        
                    print("\nWrite the text you want to append to the file, line by line. Write 'EXIT' (without quotation marks) to stop appending.\n")
                    text = input(">>> ") + "\n"
                    while text != "EXIT\n":
                        with open("Files\\"+logged_in_user+"\\"+file_to_open,"a") as file:
                            file.write(text) # does not work properly

                        # reopen file so the displayed text updates
                        with open("Files\\"+logged_in_user+"\\"+file_to_open,"r") as file:
                            file_lines = file.readlines()

                        print("\n-----FILE START-----")
                        for index in range(0,len(file_lines)):
                            print(index,file_lines[index],end="")
                        print("-----FILE   END-----\n")
                        text = input(">>> ") + "\n"

                    file.close()

                else: # mode in ["C","CHOOSE"]
                    with open("Files\\"+logged_in_user+"\\"+file_to_open,"r") as file:
                        file_lines = file.readlines()
                        
                    print("\nWrite the number of the line you want to edit.")
                    print("Then, separated by a comma, write the text you want to replace the line with.")
                    print("To add a new line, write 'N' instead of a number.")
                    print("For example, '5,Hello World' or 'N,Newline!'")
                    print("Write 'EXIT' (without quotation marks) to stop editing.")
                    print("Write 'DELETE, LineNo' to remove a line, where LineNo is the number of the line you want to delete.")
                    print("    If LineNo is not entered, the last line will be removed by default.")
                    print("(note that changes will not be saved until you write 'EXIT') \n")

                    print("-----FILE START-----")
                    for index in range(0,len(file_lines)):
                        print(index,file_lines[index],end="")
                    print("-----FILE   END-----")
                    print() # \n
                        
                    Choose_Lines_Input()
                    while text[0].upper() != "EXIT":
                        while text_not_accepted:
                            if text[0].isnumeric() == False and text[0].upper() not in ["N","EXIT","DELETE","DEL","RM"]:
                                print("\nText line '{}' invalid.".format(text[0]))
                            elif text[0].isnumeric():
                                if int(text[0]) >= len(file_lines):
                                    print("\n'{}' exceeds the highest line number. Please use 'N' to make a new line.".format(text[0]))
                                else:
                                    if len(text) > 1:
                                        text_not_accepted = False
                                        break
                                    else:
                                        print("\nInvalid input; no comma found.")
                                        
                            elif text[0].upper() in ["N","DELETE","DEL","RM"] and len(text) == 1:
                                print("\nInvalid input; no comma found.")
                            else:
                                text_not_accepted = False
                                break
                            
                            Choose_Lines_Input()
                            print() # \n
                            
                        if len(text) > 1:
                            text[1] += "\n"
                            
                        if text[0].upper() == "N":
                            file_lines.append(text[1])
                            
                        elif text[0].upper() in ["DELETE","DEL","RM"]:
                            if len(text) == 1:
                                print("Please specify which line you want to delete. (e.g 'DELETE, 4')")
                                Choose_Lines_Input()
                                continue

                            try:
                                if int(text[1]) < len(file_lines):
                                    file_lines.pop(int(text[1]))
                                else:
                                    print("Line number '{}' does not exist.".format(int(text[1])))
                                    Choose_Lines_Input()
                                    continue
                            except ValueError: # text[1] is blank or not a number
                                if text[1] == "\n": # text[1] is blank
                                    try:
                                        file_lines.pop(len(file_lines)-1) # remove last line
                                    except IndexError: # file is empty
                                        print("Can not remove what does not exist!")
                                        Choose_Lines_Input()
                                        continue
                                else: # text[1] is not an integer and is not n or N
                                    print("'{}' is not an integer. Enter an integer. (or ".format(text[1][:-1]) +
                                          "leave blank to delete the last line)")
                                    print("(e.g 'DELETE,4')")
                                    Choose_Lines_Input()
                                    continue
                           
                            print("Line {} deleted".format(len(file_lines)))
                            
                        elif text[0].upper() == "EXIT":
                            continue # end loop
                        else: # text[0] == valid integer
                            file_lines[int(text[0])] = text[1]

                        with open("Files\\"+logged_in_user+"\\"+file_to_open,"w") as file:
                            file.write("".join(file_lines))
                            file.close()
                            
                        print("-----FILE START-----")
                        for index in range(0,len(file_lines)):
                            print(index,file_lines[index],end="")
                        print("-----FILE   END-----")
                            
                        print() # \n
                        Choose_Lines_Input()
                        print() # \n

                        
        elif user_option in ["D","DEL","RM"]:
            List_Files(files)
            file_to_delete = input("\nWhat file would you want to delete?(case-sensitive) \n>>> ")
            if file_to_delete == "":
                print("\nReturning to menu...")
            elif file_to_delete not in files:
                print("\nFile '" + file_to_delete + "' is not in your folder. Returning to menu...")
            else:
                confirm = (input("\nReally delete '"+ file_to_delete +"'? (Y/N) \n>>> ").upper()).replace(" ","")
                while confirm not in ["Y","YES","N","NO"]:
                    confirm = (input("\nReally delete '"+ file_to_delete +"'? (Y/N)\n>>> ").upper()).replace(" ","")
                if confirm == "Y":
                    remove("Files\\"+logged_in_user+"\\"+file_to_delete)
                    print("\nFile '" + file_to_delete+ "' deleted.")


        elif user_option in ["CHANGE","CHANGEPASSWORD"]:
            old_password = getpass("Please re-enter your password. (Leave blank to cancel) \n>>>")
            if Hash_Password(users_dict[logged_in_user][0],old_password) == users_dict[logged_in_user][1]:
                new_password = Input_Password("new password (8-100 characters):",create_account=True)
                salt = Generate_Salt()
                users_dict[logged_in_user] = [salt,Hash_Password(salt,new_password)]
                users_file = open("users.txt","w")
                users_file.write(str(users_dict))
                users_file.close()

                print("Password changed.")
            else:
                print("Invalid password. Logging out...") # assume a person other than the owner of the account tried to change the password
                logged_in_user = ""
                logged_in = False
                

        elif user_option == "DELETEACCOUNT":
            confirm = (input("Do you really want to delete your account? (Y/N) \n>>> ").upper()).replace(" ","")
            while confirm not in ["Y","YES","N","NO"]:
                print("Invalid input.")
                confirm = (input("Do you really want to delete your account? (Y/N) \n>>> ").upper()).replace(" ","")
            if confirm == "Y":
                password = getpass("Please re-enter your password. (Leave blank to cancel) \n>>> ")
                if password == "":
                    continue # do not delete account
                else:
                    if Hash_Password(users_dict[logged_in_user][0],password) == users_dict[logged_in_user][1]:
                        rmtree("Files\\"+logged_in_user,ignore_errors=True)
                        print("\nAccount Deleted\n\n")
                        users_dict.pop(logged_in_user)
                        users_file = open("users.txt","w")
                        users_file.write(str(users_dict))
                        users_file.close()
                        logged_in_user = ""
                        logged_in = False
                        continue
                    else:
                        print("Invalid password. Logging out...") # assume a person other than the owner of the account tried to delete it
                        logged_in_user = ""
                        logged_in = False
                    
        else: # user_option in ["LO","LOGOUT"]:
            print("Logged out")
            logged_in_user = ""
            logged_in = False
            continue
