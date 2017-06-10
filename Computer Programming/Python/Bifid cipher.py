from random import randint # for randomising letter casing

def VerifyOption(prompt,example=""):
    option = (input(prompt + " (Y/N) " + example + "\n>>> ").upper()).replace(" ","")
    while option != "Y" and option != "N":
        option = (input("Invalid input. " + prompt + " (Y/N) " + example + "\n>>> ").upper()).replace(" ","")

    return option

def RememberLetterCasingAndFormat(msg,mode="prompt", msg_info=[]): # modes: 'prompt', 'apply'; default='prompt'
    if mode.upper() == "PROMPT":
        option = VerifyOption("Remember letter-casing and format?")

        if option == "N":
            return None # stop rest of function from running
        else:
            pass # continue function

        msg_info = [] # reset msg_info
        for char in msg:
            if char.upper() not in alphabet and char != " ":
                continue #skip
            
            if char == " ": # if space:
                msg_info.append("SPACE")
            elif char.upper() == char: # if upper case
                msg_info.append("UPPER")
            else:  # if lower case
                msg_info.append("LOWER")

        return msg_info

    elif mode.upper() == "APPLY":
        for info in msg_info:
            if info == "SPACE": #increase msg length to avoid IndexError
                msg += " "


        msg_string = ""
        index = 0
        for info in msg_info:
            if info == "UPPER":
                msg_string += msg[index].upper()
                index += 1
            elif info == "LOWER":
                msg_string += msg[index].lower()
                index += 1
            else: # info == "SPACE"
                msg_string += " "

        return msg_string

    else:
        raise Exception("Invalid mode. Mode not 'prompt' or 'apply'")
def StringListConverter(msg,convert_to):
    try:
        if convert_to.upper() == "STR" or convert_to.upper() == "STRING":
            msg_string = ""
            for char in msg:
                msg_string += char

            return msg_string

        elif convert_to.upper() == "LIST" or convert_to.upper() == "ARRAY":
            msg_list = []
            for char in msg:
                msg_list.append(char)

            return msg_list
        
    except AttributeError:
        pass
    raise Exception("Invalid input (not 'str', 'string', 'list' or 'array'") # raise error if input is invalid

def FormatString(msg):
    option = VerifyOption("Format encrypted string?","\n(e.g 'VFXGVTBUGOOG' -> 'VFXG VTBU GOOG')")
    
    if option == "N":
        return msg # stop rest of function from running
    else:
        pass # continue function

    while True:
        try:
            letters_per_group = int((input("How many letters per group? (e.g AAA BBB CCC = 3 per group) \n>>> ").upper()).replace(" ",""))
            break # will not run until the input above is valid
        except ValueError:
            print("Invalid input. Please enter an integer only.")

    msg_list = StringListConverter(msg,"list")
    
    spaces_added = 0
    for char_index in range(letters_per_group,len(msg_list),letters_per_group): #add spaces
        msg_list.insert(char_index+spaces_added," ")
        spaces_added += 1
        

    msg = StringListConverter(msg_list,"string")

    return msg
    

def RandomiseLetterCasing(msg):
    option = VerifyOption("Randomise letter casing?")

    if option == "N":
        return msg # stop rest of function from running
    else:
        pass # continue function

    msg_list = StringListConverter(msg,"list")
    
    for char_index in range(0,len(msg_list)):
        case = randint(0,1) # 0 = lower-case,  1 = upper-case
        if case: # case == 1
            msg_list[char_index] = msg_list[char_index].upper()
        else:
            msg_list[char_index] = msg_list[char_index].lower()

    msg = StringListConverter(msg_list,"string")

    return msg

def ChangeKey():
    global key,letter_replace

    option = VerifyOption("Change key?")

    if option == "N":
        return "no key change" # stop rest of function from running
    else:
        pass # continue function

    print("\n(Leave blank to use default value)")
    letter_replace_temp = input("Replace all []'s with []'s (input using format x,y) \n>>> ").upper()
    if letter_replace_temp == "":
        letter_replace_temp = "J,I"

    while (len(letter_replace_temp) != 3 or letter_replace_temp[1] != "," or
           letter_replace_temp[0] not in alphabet or letter_replace_temp[2] not in alphabet): # validation check
        print("\nInvalid input.")
        letter_replace_temp = input("Replace all []'s with []'s (input using format x,y) \n>>> ").upper()
        if letter_replace_temp == "":
            letter_replace_temp = "J,I"
        

    letter_replace = [letter_replace_temp[0],letter_replace_temp[2]]

    
    temp_key = (input("Enter new key. (e.g ATTACKATDAWN,ACBEFDGHIKLMNOPQRSTVWXUZY) \n>>> ").upper()).replace(" ","")
    new_key= ""

    if letter_replace[0] in temp_key: # remove character(s) from key if they are equal to letter_replace[0]
        temp_key = temp_key.replace(letter_replace[0],"")

    for char in temp_key: #turn keyword into key if necessary
        if char not in new_key:
            new_key += char

    for char in alphabet: #add rest of alphabet in order if necessary
        if char not in new_key and char != letter_replace[0]:
            new_key += char

    key = [] # remove default key
    for i in range(0,21,5): # split key into 5 equal parts and add to global key
        key += [[new_key[i],new_key[i+1],new_key[i+2],new_key[i+3],new_key[i+4]]]

    print(((("\nNew key:\n" + str(key[0]) + "\n" + str(key[1]) + "\n" + str(key[2]) + "\n" + str(key[3]) + "\n" + str(key[4]))
          .replace("[","").replace("]","")).replace("'","")).replace(",",""))
    print("All {}'s are replaced by {}'s".format(letter_replace[0],letter_replace[1]))



# Program start
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

print("Bifid cipher encrypter/decrypter\n")

while True:
    key = [["A","B","C","D","E"],
           ["F","G","H","I","K"],
           ["L","M","N","O","P"],
           ["Q","R","S","T","U"],
           ["V","W","X","Y","Z"]]

    letter_replace = ["j","i"]
    
    print("Default key: \nA B C D E \nF G H I K \nL M N O P \nQ R S T U \nV W X Y Z")
    print("All J's are replaced by I's \n")

    ChangeKey() # asks user if he/she wants to change the key, and does so if necessary

    option = input("\n[E]ncrypt or [D]ecrypt? \n>>> ").upper()

    while option != "E" and option != "D":
        option = input("Invalid input. [E]ncrypt or [D]ecrypt? \n>>> ").upper()


    if option == "E":
        plain_text = input("Input plain text to be encrypted \nAll non-letter characters will be removed) \n>>>  ")

        plain_text_info = RememberLetterCasingAndFormat(plain_text)

        plain_text = plain_text.lower() # make lower case
        
        plain_text = plain_text.replace(letter_replace[0].lower(),letter_replace[1].lower()) # replace one character by another one, j -> i by default
        row_numbers = ""
        column_numbers = ""

        for char in plain_text:
            for i in range(0,5): #row
                for j in range(0,5): #column
                    if char.upper() == key[i][j]:
                        row_numbers += str(i+1)
                        column_numbers += str(j+1)

        output_numbers = row_numbers + column_numbers
        cipher_text = ""
        for i in range(0,len(output_numbers),2):
            cipher_text += key[int(output_numbers[i])-1][int(output_numbers[i+1])-1]

        if plain_text_info == None:
            cipher_text = RandomiseLetterCasing(cipher_text) # ask user if he/she wants to randomise the letter casing
            cipher_text = FormatString(cipher_text) # ask user if he/she wants to format the string, e.g  FNPOLPARRD -> FNPO LPAR RD
        else:
            cipher_text = RememberLetterCasingAndFormat(cipher_text,"apply",plain_text_info)
        
        print("Cipher text: " + cipher_text)


    else: # option == "D"
        cipher_text = input("Input cipher text to be decrypted \nAll non-alphabetical characters will be removed) \n>>>  ")

        cipher_text_info = RememberLetterCasingAndFormat(cipher_text)

        cipher_text = cipher_text.upper() # make upper-case

        for char in cipher_text: #remove non-alphabetical characters
            if char not in alphabet:
                cipher_text = cipher_text.replace(char,"")

        row_numbers = ""
        column_numbers = ""

        for char in cipher_text:
            for i in range(0,5): #row
                for j in range(0,5): #column
                    if char.upper() == key[i][j]:
                        row_numbers += str(i+1)
                        column_numbers += str(j+1)

        input_numbers = row_numbers + column_numbers
        
        input_numbers_processed = []
        for i in range(0,len(cipher_text)):
            try:
                input_numbers_processed.append(row_numbers[i])
                input_numbers_processed.append(column_numbers[i])
            except:
                print("Looks like an error occured. This may have an effect on your decrypted string.")

        output_row_numbers = input_numbers_processed[:len(input_numbers_processed)//2]
        output_column_numbers = input_numbers_processed[len(input_numbers_processed)//2:]
        output_numbers = []

        for i in range(0,len(output_row_numbers)):
            output_numbers.append([output_row_numbers[i],output_column_numbers[i]])

        
        plain_text = ""

        for letter_position in output_numbers:
            plain_text += key[int(letter_position[0])-1][int(letter_position[1])-1]

        if cipher_text_info: # if cipher_text_info != None
            plain_text = RememberLetterCasingAndFormat(plain_text, "apply",cipher_text_info)

        print("Plain text: " + plain_text)
        print("Note: some " + letter_replace[1] + "'s may be " + letter_replace[0] + "'s")
            

    print("\n\n\n---PROGRAM RESTART---\n\n\n")
