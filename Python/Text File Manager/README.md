Download the contents in this folder, and place them in the same folder.


Run Text File Manager.exe 
OR 
Run Text File Manager.py (by double-clicking on it, not through IDLE)
You can use IDLE to run the program, but one security feature will be disabled
(when you input a password, the password will be displayed as you type it)

The password for the user "admin" is "adminadmin".

Content info:

Files: Folder that contains one folder for every user; each folder will contain .txt 
files accessible only to them (within the program, anyway)

users.txt: Contains a dictionary with username:password pairs, where the password has been 
salted and hashed using the SHA512 algorithm 100000 times.

