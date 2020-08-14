import sqlite3
import datetime as dt
now = dt.datetime.now()
endDateBronzeDeposit = now + dt.timedelta(days=7)
endDateSilverDeposit = now + dt.timedelta(days=20)
endDateGoldDeposit = now + dt.timedelta(days=45)

class SQLighter:

	def __init__(self, database_file):
		'''ИНИЦИ'''
		self.con = sqlite3.connect(database_file, check_same_thread=False)
		self.cur = self.con.cursor()

	def get_balance(self, user_id):
		'''ПОЛУЧИТЬ БАЛАНЦ ПОЛЬЗОВАТЕЛЯ'''
		with self.con:
			result = self.cur.execute("SELECT balance FROM users WHERE id = '%s'"%(user_id)).fetchone()
			return result[0]

	def get_deposits(self, user_id):
		'''ПОЛУЧИТЬ АКТИВНЫЕ ВКЛАДЫ'''
		with self.con:
			return self.cur.execute("SELECT * FROM usersdeposits WHERE id = '%s'"%(user_id)).fetchone()

	def add_user(self, user_id, userfirstname, userlastname):
		'''ДОБАВИТЬ ID, ИМЯ И ФАМИЛИЮ И ДАТУ РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ'''
		'''ДОБАВИТЬ ПОЛЬЗОВТАЕЛЯ В ТАБЛИЦУ usersdeposits'''
		with self.con:
			dtnow = dt.datetime.now()
			dtnow2 = dtnow.strftime("%d.%m.%Y")
			x = self.cur.execute("INSERT OR IGNORE INTO users (id, firstname, lastname, regdate) VALUES ('%s', '%s', '%s', '%s')"%(user_id, userfirstname, userlastname, dtnow2))
			y = self.cur.execute("INSERT OR IGNORE INTO usersdeposits (id) VALUES ('%s')"%(user_id))
			return x, y

	def register_deposit(self, user_id, typedeposit, sumdeposit):
		'''ЗАРЕГИСТРИРОВАТЬ ВКЛАД'''
		dtnow = dt.datetime.now()
		dtnowstrf = dtnow.strftime("%d.%m.%Y")
		if typedeposit == 'Bronze':
			dtend = dtnow + dt.timedelta(days=7)
			dtendstrf = dtend.strftime("%d.%m.%Y")
			regbronzedeposit = self.cur.execute("UPDATE usersdeposits SET bronzeactive = 1, startbronzedeposit = '%s', endbronzedeposit = '%s', sumbronze = '%s' WHERE id = '%s'"%(dtnowstrf, dtendstrf, sumdeposit, user_id))
			selectbalance = self.cur.execute("SELECT balance FROM users WHERE id = '%s'"%(user_id)).fetchone()
			resetbalance = self.cur.execute("UPDATE users SET balance = '%s' WHERE id = '%s'"%(selectbalance[0] - int(sumdeposit), user_id))
			return regbronzedeposit, resetbalance, self.con.commit()
		elif typedeposit == 'Silver':
			dtend = dtnow + dt.timedelta(days=20)
			dtendstrf = dtend.strftime("%d.%m.%Y")
			regsilverdeposit = self.cur.execute("UPDATE usersdeposits SET silveractive = 1, startsilverdeposit = '%s', endsilverdeposit = '%s', sumsilver = '%s' WHERE id = '%s'"%(dtnowstrf, dtendstrf, sumdeposit, user_id))
			selectbalance = self.cur.execute("SELECT balance FROM users WHERE id = '%s'" % (user_id)).fetchone()
			resetbalance = self.cur.execute("UPDATE users SET balance = '%s' WHERE id = '%s'" % (selectbalance[0] - int(sumdeposit), user_id))
			return regsilverdeposit, resetbalance, self.con.commit()
		elif typedeposit == 'Gold':
			dtend = dtnow + dt.timedelta(days=45)
			dtendstrf = dtend.strftime("%d.%m.%Y")
			reggolddeposit = self.cur.execute("UPDATE usersdeposits SET goldactive = 1, startgolddeposit = '%s', endgolddeposit = '%s', sumgold = '%s' WHERE id = '%s'"%(dtnowstrf, dtendstrf, sumdeposit, user_id))
			selectbalance = self.cur.execute("SELECT balance FROM users WHERE id = '%s'" % (user_id)).fetchone()
			resetbalance = self.cur.execute("UPDATE users SET balance = '%s' WHERE id = '%s'" % (selectbalance[0] - int(sumdeposit), user_id))
			return reggolddeposit, resetbalance, self.con.commit()

	def checkdeposit(self, user_id, typedeposit):
		'''ПРОВЕРКА НАЛИЧИЯ ВКЛАДА'''
		with self.con:
			result = self.cur.execute("SELECT %s FROM usersdeposits WHERE id = '%s'"%(typedeposit, user_id)).fetchone()
			return result[0]

	def withdraw(self, user_id, sum):
		'''ВЫЧЕТ СРЕДСТВ НА ВЫВОД'''
		with self.con:
			return self.cur.execute("UPDATE users SET balance = '%s' WHERE id = '780903878'"%(sum))

	def add_query(self, user_id, sum, number_card):
		'''ДОБАВИТЬ ЗАПРОС НА ВЫВОД'''
		with self.con:
			dateRequest = dt.datetime.now()
			dateRequestStrf = dateRequest.strftime('%H:%M %d.%m')
			return self.cur.execute("INSERT OR IGNORE INTO payment_query (user_id, card, sum, dateRequest) VALUES ('%s', '%s', '%s', '%s')"%(user_id, number_card, sum, dateRequestStrf))

	def close_request(self, number):
		'''ЗАКРЫТЬ ЗАПРСО НА ВЫВОД'''
		with self.con:
			return self.cur.execute("UPDATE payment_query SET history = 'Yes' WHERE requestNumber = '%s'"%(number))

	def check_id(self, user_id):
		'''ПРОЕРКА ID'''
		with self.con:
			result = self.cur.execute("SELECT id FROM users WHERE id = %s"%(user_id)).fetchone()
			try:
				return result[0]
			except:
				return 'notfound'

	def get_date(self):
		'''ПОЛУЧИТЬ ДАТУ'''
		dtnow = dt.datetime.now()
		dtnowstrf = dtnow.strftime("%d.%m.%Y")
		return dtnowstrf

	def close_deposit(self, user_id, type):
		'''ЗАКРЫТЬ ВКЛАД'''
		with self.con:
			if type == 'Bronze':
				return self.cur.execute("UPDATE usersdeposits SET bronzeactive = 0, startbronzedeposit = null, endbronzedeposit = null, sumbronze = null WHERE id = '%s'"%(user_id))
			if type == 'Silver':
				return self.cur.execute("UPDATE usersdeposits SET silveractive = 0, startsilverdeposit = null, endsilverdeposit = null, sumsilver = null WHERE id = '%s'" % (user_id))
			if type == 'Gold':
				return self.cur.execute("UPDATE usersdeposits SET goldactive = 0, startgolddeposit = null, endgolddeposit = null, sumgold = null WHERE id = '%s'" % (user_id))

			else: return print("Hello :D")

	def id(self):
		with self.con:
			return self.cur.execute("SELECT id FROM users").fetchall()

	def countdeposits(self, type):
		with self.con:
			return self.cur.execute("SELECT COUNT (*) FROM usersdeposits WHERE %s == 1"%(type)).fetchone()

	def countusers(self):
		with self.con:
			return self.cur.execute("SELECT COUNT (*) FROM users").fetchone()

	def sumbalance(self):
		with self.con:
			return self.cur.execute("SELECT sum(balance) FROM users").fetchone()

	def idinfo(self, user_id):
		with self.con:
			return self.cur.execute("SELECT * FROM users WHERE id = %s"%(user_id)).fetchone()


	def close(self):
		self.con.close()