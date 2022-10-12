from collections import namedtuple
from dbconfig import get_pwdb
from add import getMasterKey
from cryptography.fernet import Fernet
from pyperclip import copy

def retrieve_password(masterpassword, salt, search, decryptpassword = False):
	db = get_pwdb()
	cursor = db.cursor(named_tuple=True)

	query = ""

	if len(search) == 0:
		query = "SELECT * FROM pmdatabase.passwords"
	else:
		query = "SELECT * FROM pmdatabase.passwords WHERE "
		for i in search: 
			query += f"{i} = '{search[i]}' AND "
		print(f"FOR MY OWN PERSONAL USE: {query}")
		query = query[:-5]
	cursor.execute(query)
	results = cursor.fetchall()[0]
	print(results)
	print(f"Type of result: {type(results)}")
	
	if len(results) == 0:
		print("No results for your search")
		return

	#if user wants the password to be decrypted and there are multiple results, prints all results without password
	#if user does not want to decrypt the password, prints all results without the password
	if (decryptpassword and len(results) > 1) or (decryptpassword == False):
		for i in results:
			if not i[4]:
				print(i)
		return

	if len(results) == 1 and decryptpassword == True:
		masterkey = getMasterKey(mp=masterpassword, salt=salt)

		fernet = Fernet(masterkey)

		decryptedPassword = fernet.decrypt(results[0][4]).decode()

		copy(decryptedPassword)

	db.close()
