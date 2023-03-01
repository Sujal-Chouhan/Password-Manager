from getpass import getpass
import hashlib
import argparse
import pyperclip
from dbconfig import get_pwdb
import add
import get_password
import generate_password
from delete import deletePassword

parser = argparse.ArgumentParser(description="Password Manager")

parser.add_argument('option', help="(a)dd / (g)et / (gen)erate / (d)elete")
parser.add_argument("-w", "--website", help="website")
parser.add_argument("-url", "--url", help="website url")
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-e", "--email", help="email")
parser.add_argument("-l", "--length", help="length of the password to generate")
parser.add_argument("-c", "--copy",action="store_true", help="Copy password to clipboard")



args = parser.parse_args()


def getAndValidateMasterPassword():
	masterpw = getpass("Input your Master Password: ")
	hash_masterpw = hashlib.sha256(masterpw.encode()).hexdigest()

	pwdb = get_pwdb()
	cursor = pwdb.cursor(named_tuple=True)
	cursor.execute("SELECT * FROM pmdatabase.masterkeys")
	result = cursor.fetchall()
	result = result[0][0]
	if hash_masterpw != result:
		print("WRONG! Please Try Again")
		return None
	return [masterpw, result[0]]


def main():
	if args.option in ["add", "a"]:
		if args.website == None or args.url == None or args.username == None or args.email == None:
			if args.website == None:
				print("Website name (-w) required")
			if args.url == None:
				print("Website URL (-url) required")
			if args.username == None:
				print("Username (-u) required")
			if args.email == None:
				print("Email (-e) required")

		res = getAndValidateMasterPassword()

		if res is not None:
			add.addEntry(res[0][0], res[0][1], args.website, args.url, args.username, args.email)

	if args.option in ["get", "g"]:
		res = getAndValidateMasterPassword()

		search = {}
		if args.website is not None:
			search["website"] = args.website
		if args.url is not None:
			search["websiteurl"] = args.url
		if args.email is not None:
			search["email"] = args.email
		if args.username is not None:
			search["username"] = args.username

		if res is not None:
			get_password.retrieve_password(res[0][0], res[0][1], search, decryptpassword= args.copy)

	if args.option in ["gen", "generate"]:
		if args.length == 0:
			print("Please enter the length of the password you would like to generate (-l) / (--length)")
			return None
		password = generate_password.generate_password(length = int(args.length))
		pyperclip.copy(password)
		print("A Password has been generated and copied to your clipboard")

	if args.option in ["d", "delete"]:
		res = getAndValidateMasterPassword()

		search = {}
		if args.website is not None:
			search["website"] = args.website
		if args.url is not None:
			search["websiteurl"] = args.url
		if args.email is not None:
			search["email"] = args.email
		if args.username is not None:
			search["username"] = args.username

		if res is not None:
			deletePassword(search)

		


main()




