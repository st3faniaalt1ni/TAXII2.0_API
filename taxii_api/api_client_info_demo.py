from taxii2client import Server,Collection,ApiRoot, Status


if __name__ == "__main__":
	server = Server('http://localhost:8090/taxii', user='stefania', password='1234')

	print("Server title : %s"% server.title)
	print("Default API : %s"%server.default)
	print("Description : %s"%server.description)
	print("Contact : %s"%server.contact)
	print('Available API roots: ')
	counter = 0
	for api in server.api_roots:
		print('%d : %s'%(counter, api.url))
		counter +=1

	print('-------APIs info--------------')
	for api in server.api_roots:
		print('endpoint URL : %s'% api.url)
		print('title : %s'% api.title)
		print('description : %s'% api.description)
		print('...----------Collection info')
		for collection in api.collections:
			print('ID : %s'%collection.id)
			print('Title : %s'%collection.title)
			print('Description : %s'%collection.description)
			print('________________________________________')

    ###########################################################
