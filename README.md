# Password-Manager
A secure password manager that encrypts and stores user passwords in a MySQL database using Cryptography libraries
Ensures the security of passwords against rainbow table and dictionary attacks through hashing and salting of master password

To use, Follow the following steps:

1) You must start a local MySQL server on your device and set your username as "root" and password as "root"

2) Install the following packages via pip:
    pyperclip
    mysql-connector-python
    fernet
    tabulate
 
 3) Open a terminal, enter the directory with the Password manager files, and run the command "python config.py", this will ask you to choose a master password,
    the master password is very important and is the key to all your other passwords, memorizing this password is highly recommended
    
 4) Enjoy! You can now add, generate, or extract passwords by simply typing "python pm.py" followed by your query. If you require further help, simply type "python pm.py     help"
