from getpass import getpass
import dbconfig
import hashlib
import random
import string

# Creates a salt for the hash of the password
def create_salt(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))


def config():
    #Creates Database We will be working with
    pwdb = dbconfig.get_pwdb()
    my_cursor = pwdb.cursor()
    masterpassword = ""

    my_cursor.execute("CREATE DATABASE pmdatabase")


    #Creates Table which store the Master Password and the Salt
    my_cursor.execute("CREATE TABLE pmdatabase.masterkeys (hash_masterpassword TEXT NOT NULL, salt TEXT NOT NULL)")
    print("masterkeys Table Created")
    #Creates Table which stores passwords
    my_cursor.execute("CREATE TABLE pmdatabase.passwords (website TEXT NOT NULL, websiteurl TEXT NOT NULL, username TEXT, email TEXT, password TEXT NOT NULL)")
    print("passwords Table Created")

    #User Chooses a Master Password, Which is then Hashed
    while True:
        masterpassword = getpass("Choose your Master Password: ")
        temp_mp = getpass("Please confirm your Master Password")
        if masterpassword == temp_mp and masterpassword != "": 
            break
        print("The two passwords you entered were not the same, please try again")
    hash_masterpassword = hashlib.sha256(masterpassword.encode()).hexdigest()
    print("Hash of Master Password Generated")

    #Salt is created
    salt = create_salt()
    print("Salt was Succesfully Created")

    #Add hash_masterpassword and salt into masterkeys Table
    my_cursor.execute("INSERT INTO pmdatabase.masterkeys (hash_masterpassword, salt) values (%s, %s)", (hash_masterpassword, salt))
    pwdb.commit()
    print("Hash of Master Password and Salt added to Masterkeys Table")


    pwdb.close()

config()




