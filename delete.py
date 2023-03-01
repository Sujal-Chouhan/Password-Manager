from dbconfig import get_pwdb



def deletePassword(search):
	db = get_pwdb()
	cursor = db.cursor(buffered=True)

	query = ""

	if len(search) == 0:
		print("Please add some information for the password you are trying to delete")
	else:
		query = "SELECT * FROM pmdatabase.passwords WHERE "
		for i in search:
			query += f"{i} = '{search[i]}' AND "
		query = query[:-5]
	cursor.execute(query)
	results = cursor.fetchall()

	if len(results) == 0:
		print(f"search query: {query}")
		print(results)
		print("No results for your search")
		return

	if len(results) > 1:
		print("Too many results, add more information about the password you are trying to delete")

	if len(results) == 1:
		deleteQuery = "DELETE FROM pmdatabase.passwords WHERE "
		for i in search:
			deleteQuery += f"{i} = '{search[i]}' AND "
		deleteQuery = deleteQuery[:-5]
		cursor.execute(deleteQuery)
		db.commit()
		print("Password Deleted")
		db.close()
		