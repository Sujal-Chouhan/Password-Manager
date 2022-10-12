from cgi import print_exception
import mysql.connector

def get_pwdb():
	try:
		pwdb = mysql.connector.connect(host = "localhost",user = "root", passwd = "root")
	
	except Exception as e:
		print("Error connecting to database")
		print_exception()

	return pwdb
