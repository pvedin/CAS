## TODO:
## - Add ability to keep letter-casing and format (e.g h eLl O -> f fNv D)
## - Add ability to randomise letter-casing (e.g hello -> HeLLO)
## - Add ability to format encrypted letters (e.g VDCSASLKBXWKIP - > VDCSA SLKBX WKIP)
##

def ChangeKey():
    global key,letter_replace

    option = (input("Change key? (Y/N) \n>>> ").upper()).replace(" ","")
    while option != "Y" and option != "N":
        option = input("Invalid input. Change key? (Y/N) \n>>> ").upper()

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
        letter_replace_temp = input("Replace all []'s with []'s (input using format x,y \n>>> ").upper()

    letter_replace = [letter_replace_temp[0],letter_replace_temp[2]]

    
    temp_key = input("Enter new key. (e.g ATTACKATDAWN,ACBEFDGHIKLMNOPQRSTVWXUZY) \n>>> ").upper()
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
        plain_text = input("Input plain text to be encrypted \nAll non-letter characters will be removed) \n>>>  ").lower()
        
        plain_text = plain_text.replace(letter_replace[0],letter_replace[1]) # replace one character by another one, j -> i by default
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
        print("Cipher text: " + cipher_text)

    else: # option == "D"
        cipher_text = input("Input cipher text to be decrypted \nAll non-alphabetical characters will be removed) \n>>>  ").upper()

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
            input_numbers_processed.append(row_numbers[i])
            input_numbers_processed.append(column_numbers[i])

        output_row_numbers = input_numbers_processed[:len(input_numbers_processed)//2]
        output_column_numbers = input_numbers_processed[len(input_numbers_processed)//2:]
        output_numbers = []

        for i in range(0,len(output_row_numbers)):
            output_numbers.append([output_row_numbers[i],output_column_numbers[i]])

        
        plain_text = ""

        for letter_position in output_numbers:
            plain_text += key[int(letter_position[0])-1][int(letter_position[1])-1]

        print("Plain text: " + plain_text)
        print("Note: some " + letter_replace[1] + "'s may be " + letter_replace[0] + "'s")
            

    print("\n\n\n---PROGRAM RESTART---\n\n\n")

        
        
        
                        
