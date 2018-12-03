import pymysql

def connect_to_db(self):
	mysqlHost = self.bot.config.mysql["host"]
	mysqlUser = self.bot.config.mysql["username"]
	mysqlPass = self.bot.config.mysql["password"]
	mysqlDB = self.bot.config.mysql["dbname"]

	try:
		return pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db=mysqlDB, charset='utf8')
	except KeyError:
		print("Rest in peperoni, Impossible de se connecter a la base de données.")
		print(str(KeyError))
		return

def reconnect_to_db(self):
	if not self.conn:
		mysqlHost = self.bot.config.mysql["host"]
		mysqlUser = self.bot.config.mysql["username"]
		mysqlPass = self.bot.config.mysql["password"]
		mysqlDB = self.bot.config.mysql["dbname"]

		return pymysql.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db=mysqlDB, charset='utf8')
	return self.conn