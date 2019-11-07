import mysql.connector



class MyDB:
	def __init__ (self,host,database):
		self.host = host
		self.database = database


	def getConn(self):
		print(self.host,self.database)
		conn = None
		conn =  mysql.connector.connect(host= self.host,
                                       database= self.database,
                                       user='dpm',
                                       password='sql')

		return conn
