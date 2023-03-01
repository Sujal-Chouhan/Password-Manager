from dbconfig import get_pwdb
from add import getMasterKey
from cryptography.fernet import Fernet
from pyperclip import copy
import base64
from tabulate import tabulate

def retrieve_password(masterpassword, salt, search, decryptpassword = False):
	db = get_pwdb()
	cursor = db.cursor(buffered=True)

	query = ""
	
	if len(search) == 0:
		query = "SELECT * FROM pmdatabase.passwords"
	else:
		query = "SELECT * FROM pmdatabase.passwords WHERE "
		for i in search: 
			query += f"{i} = '{search[i]}' AND "
		query = query[:-5]
	cursor.execute(query)
	results = cursor.fetchall()
	

	if len(results) == 0:
		print("No results for your search")
		return

	#if user wants the password to be decrypted and there are multiple results, prints all results without password
	#if user does not want to decrypt the password, prints all results without the password
	if (decryptpassword and len(results) > 1) or (decryptpassword == False):

		table = [["Website", 'Website URL', 'Email', 'Username']]
		for row in results:
			addition = []
			for x in range(len(row)):
				if x == 4:
					pass
				else:
					addition.append(row[x])
			table.append(addition)

		print(tabulate(table,headers="firstrow",tablefmt="github"))
		
		return
	
	if len(results) == 1 and decryptpassword == True:
		masterkey = getMasterKey(mp=masterpassword, salt=salt)
		masterkey = base64.urlsafe_b64encode(masterkey)
		fernet = Fernet(masterkey)


		decryptedPassword = fernet.decrypt(results[0][4]).decode()

		copy(decryptedPassword)
		print("Password has been copied to your clipboard")

	db.close()
