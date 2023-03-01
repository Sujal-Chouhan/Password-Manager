from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
from dbconfig import get_pwdb
import base64


def getMasterKey(mp, salt):
    mp_encoded = mp.encode()
    salt_encoded = salt.encode()
    master_key = PBKDF2(mp_encoded, salt_encoded, 32, count=1000000, hmac_hash_module=SHA512)
    return master_key 


def addEntry(mp, salt, website, websiteurl, username, email):
    #gets password for the new entry
    password = getpass("Please enter the password: ")

    #generates masterkey, which will be used to encrypt the password
    masterkey = getMasterKey(mp, salt)
    masterkey = base64.urlsafe_b64encode(masterkey)
    

    #encrypts password using fernet
    fernet = Fernet(masterkey)
    encrypted_pw = fernet.encrypt(password.encode())

    #adds to the password database
    db = get_pwdb()
    cursor = db.cursor()
    query = "INSERT INTO pmdatabase.passwords (website, websiteurl, username, email, password) values (%s,%s,%s,%s,%s)"
    values = (website, websiteurl, username, email, encrypted_pw)
    cursor.execute(query, values)
    db.commit()

    print("Password added!")