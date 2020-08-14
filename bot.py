import telebot
import markup
import config
import text
import sqlite3
from sqlighter import SQLighter

bot = telebot.TeleBot(config.token)

# DataBase
db = SQLighter('bot.db')
con = sqlite3.connect('bot.db', check_same_thread = False)
cur = con.cursor()

# Комманда - /start - ГОТОВО
@bot.message_handler(commands = ['start'])
def handler_start(message):
	bot.send_message(message.from_user.id, 'Добро пожаловать!', reply_markup = markup.start_markup)
	db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
	# db.create_user_table(message.from_user.id)

# Комманда - /anal
@bot.message_handler(commands=['anal'])
def handler_analytics(message):
	bot.send_message(config.admin, 'Аналитика', reply_markup = markup.analytical_markup)

# Комманда - /admin - ГОТОВО
@bot.message_handler(commands = ['admin'])
def handler_admin(message):
	user_id = message.from_user.id
	if user_id == config.admin:
		bot.send_message(message.from_user.id, 'С возвращением!', reply_markup = markup.admin_markup)
# Декоратор текста
@bot.message_handler(content_types = ['text'])
def handler_text(message):
# ПОЛЬЗОВАТЕЛЬСЕКАЯ ЧАСТЬ
# ======================================================================================================================
# ======================================================================================================================

# Главное меню - ГОТОВО
	if message.text == markup.main_menu:
		bot.send_message(message.from_user.id, 'Главное меню', reply_markup = markup.start_markup)
# О сервисе - ГОТОВО
	if message.text == markup.start_button_faq:
		bot.send_message(message.from_user.id, text.faq)
# Вклады - ГОТОВО
	if message.text == markup.start_button_deposits:
		bot.send_message(message.from_user.id, text.deposit_information, reply_markup = markup.deposits_markup)
# Кабинет - ГОТОВО
	if message.text == markup.start_button_cabinet:
		bot.send_message(message.from_user.id, 'Личный кабинет', reply_markup = markup.cabinet_markup)
# Вывести ГОТОВО
	if message.text == markup.cabinet_button_withdraw:
		msg = bot.send_message(message.from_user.id, 'Укажите номер карты, на которую будут отправлены ваши средства в формате "XXXX-XXXX-XXXX-XXXX"')
		bot.register_next_step_handler(msg, select_card_withdraw)
# Пополнить ГОТОВО, но нужно дописать текст
	if message.text == markup.cabinet_button_top_up:
		bot.send_message(message.from_user.id, text.top_up)
		bot.send_message(message.from_user.id, 'Номер карты - 4890494670660083')
		bot.send_message(message.from_user.id, 'Ваш ID - {}'.format(message.from_user.id))
# Баланц ГОТОВО
	if message.text == markup.cabinet_button_balance:
		bot.send_message(message.from_user.id, 'Ваш баланс: {}р'.format(db.get_balance(message.from_user.id)))
# Мои вклады ГОТОВО
	if message.text == markup.cabinet_button_my_deposits:
		depositlist = db.get_deposits(message.from_user.id)
		get_balance_user = db.get_balance(message.from_user.id)
		if depositlist[1] == '0' and depositlist[2] == '0' and depositlist[3] == '0':
			bot.send_message(message.from_user.id, 'У вас нету активных вкладов :(')
			if get_balance_user >= 500:
				bot.send_message(message.from_user.id, 'На вашем счету имеется {}р\nИ у вас есть возможность зарегистрировать вклад!'.format(get_balance_user))
				bot.send_message(message.from_user.id, text.deposit_information, reply_markup=markup.deposits_markup)
		if depositlist[1] == '1':
			bot.send_message(message.from_user.id, 'Бронзовый вклад\nСумма вклада - {}р\nДата оформления вклада - {}\nДата окончания вклада - {}'.format(depositlist[10], depositlist[4], depositlist[7]))
		if depositlist[2] == '1':
			bot.send_message(message.from_user.id, 'Серебряный вклад\nСумма вклада - {}р\nДата оформления вклада - {}\nДата окончания вклада - {}'.format(depositlist[11], depositlist[5], depositlist[8]))
		if depositlist[3] == '1':
			bot.send_message(message.from_user.id, 'Золотой вклад\nСумма вклада - {}р\nДата оформления вклада - {}\nДата окончания вклада - {}'.format(depositlist[12], depositlist[6], depositlist[9]))
# История выводов ГОТОВО
	if message.text == markup.cabinet_button_conclusion_history:
		cur.execute("SELECT * FROM payment_query WHERE user_id = '%s'"%(message.from_user.id))
		rows = cur.fetchall()
		for row in rows:
			if row[5] == 'Yes':
				bot.send_message(message.from_user.id, 'Статус запроса - Закрыт\nНомер карты - {}\nСумма для вывода - {}р\nДата запроса - {}'.format(row[1], row[2], row[4]))
			else:
				bot.send_message(message.from_user.id, 'Статус запроса - Обрабатывается\nНомер карты - {}\nСумма для вывода - {}р\nДата запроса - {}'.format(row[1], row[2], row[4]))

# АДМИНСКАЯ ЧАСТЬ
# ======================================================================================================================
# ======================================================================================================================

# Вклады пользователей
	if message.text == markup.admin_button_users_deposits:
		if message.from_user.id == config.admin: # Проверка доступа
			get_users_deposits = cur.execute("SELECT * FROM usersdeposits").fetchall() # Получить список вкладов
			for row in  get_users_deposits: # Вывод вкладов по одному
				if row[1] == '1' or row[2] == '1' or row[3] == '1':
					if row[1] == '1':
						bot.send_message(config.admin, 'Тип вклада - Бронзовый\nID пользователя - {}\nДата активации вклада - {}\nДата окончания вклада - {}\nСумма вклада - {}({})'.format(row[0], row[4], row[7], row[10], int(int(row[10])*1.1)))
					if row[2] == '1':
						bot.send_message(config.admin, 'Тип вклада - Серебряный\nID пользователя - {}\nДата активации вклада - {}\nДата окончания вклада - {}\nСумма вклада - {}({})'.format(row[0], row[5], row[8], row[11], int(int(row[11])*1.25)))
					if row[3] == '1':
						bot.send_message(config.admin, 'Тип вклада - Золотой\nID пользователя - {}\nДата активации вклада - {}\nДата окончания вклада - {}\nСумма вклада - {}({})'.format(row[0], row[6], row[9], row[12], int(int(row[12])*1.5)))
				else:
					bot.send_message(config.admin, 'Активных вкладов не имеется :(')

# Запросы на вывод - ГОТОВО
	if message.text == markup.admin_button_withdrawal_requests:
		if message.from_user.id == config.admin:
			get_withdrawal_requests = cur.execute("SELECT * FROM payment_query").fetchall()
			for row in get_withdrawal_requests:
				if row[5] == 'No':
					bot.send_message(config.admin, 'Номер запроса - {}\nID пользователя - {}\nНомер карты - {}\nСумма вывода - {}'.format(row[3], row[0], row[1], row[2]))
			bot.send_message(config.admin, 'Если ничего не вышло, значит запросов нет')

# Закрыть запрос на вывод - ГОТОВО
	if message.text == markup.admin_button_close_request:
		if message.from_user.id == config.admin:
			msg = bot.send_message(config.admin, 'Для закрытия вкалада, введите его номер')
			bot.register_next_step_handler(msg, close_request)

# Пополнить баланц
	if message.text == markup.admin_buttont_top_up_balance:
		if message.from_user.id == config.admin:
			msg = bot.send_message(message.from_user.id, 'Введите ID пользователя')
			bot.register_next_step_handler(msg, get_id_by)

# Обновить
	if message.text == markup.admin_button_restart:
		if message.from_user.id == config.admin:
			nowdate = db.get_date()
			get_users_deposits = cur.execute("SELECT * FROM usersdeposits").fetchall()
			for row in get_users_deposits:
				if row[7] == nowdate:
					balance = db.get_balance(row[0]) # Получить баланц
					sum = int(row[10]) * 1.1 + int(balance) # Добавить к баланцу сумму вклада
					sumbronze = int(row[10]) * 1.1
					db.withdraw(row[0], sum) # Обновить баланц
					db.close_deposit(row[0], 'Bronze') # Закрыть вклад
					bot.send_message(row[0], 'Бронзовый вклад успешно закрыт!\nНа ваш счёт начисленр {}р'.format(int(sumbronze)))
				if row[8] == nowdate:
					balance = db.get_balance(row[0])  # Получить баланц
					sum = int(row[11]) * 1.25 + int(balance)  # Добавить к баланцу сумму вклада
					sumsilver = int(row[11]) * 1.25
					db.withdraw(row[0], sum)  # Обновить баланц
					db.close_deposit(row[0], 'Silver')  # Закрыть вклад
					bot.send_message(row[0], 'Серебряный вклад успешно закрыт!\nНа ваш счёт начисленр {}р'.format(int(sumsilver)))
				if row[9] == nowdate:
					balance = db.get_balance(row[0])  # Получить баланц
					sum = int(row[12]) * 1.5 + int(balance)  # Добавить к баланцу сумму вклада
					sumgold = int(row[12]) * 1.5
					db.withdraw(row[0], sum)  # Обновить баланц
					db.close_deposit(row[0], 'Gold')  # Закрыть вклад
					bot.send_message(row[0], 'Золотой вклад успешно закрыт!\nНа ваш счёт начисленр {}р'.format(int(sumgold)))

			bot.send_message(config.admin, 'Обновлено!')

# РАЗДЕЛ АНАЛИТИКИ
# ======================================================================================================================
# ======================================================================================================================

	if message.text == markup.analytical_button_id:
		users_id = db.id()
		for row in users_id:
			bot.send_message(config.admin, '{}'.format(row[0]))

	if message.text == markup.analytical_button_deposits:
		bronzeactive = db.countdeposits('bronzeactive')
		silveractive = db.countdeposits('silveractive')
		goldactive = db.countdeposits('goldactive')

		bot.send_message(config.admin, 'Кол-во бронзовых вкладов - {}\nКол-во серебряных вкладов - {}\nКол-во золотых вкладов - {}'.format(bronzeactive[0], silveractive[0], goldactive[0]))

	if message.text == markup.analytical_button_name:
		msg = bot.send_message(config.admin, 'Введите ID пользователя')
		bot.register_next_step_handler(msg, id_info)

	if message.text == markup.analytical_button_users:
		countusers = db.countusers()
		bot.send_message(config.admin, 'Кол-во пользователей - {}'.format(countusers[0]))

	if message.text == markup.analytical_button_balance:
		allbalance = db.sumbalance()
		bot.send_message(config.admin, 'Сумма всех баланцов - {}р'.format(allbalance[0]))
# Callback запросы
@bot.callback_query_handler(func = lambda c: True)
def handler_callback(message):
# FAQ - ГОТОВО
	if message.data == markup.faq_cb_faq_data:
		bot.send_message(message.from_user.id, text.faq)
# Деятельность - ГОТОВО
	if message.data == markup.faq_cb_activity_data:
		bot.send_message(message.from_user.id, text.activity)
# Бронзовый вклад - ГОТОВО
	if message.data == markup.deposits_cb_bronze_data:
		balanceforcheck = db.get_balance(message.from_user.id) # Получаем баланац
		user_id = message.from_user.id # Получаем ID
		checkdeposit = db.checkdeposit(message.from_user.id, 'bronzeactive')
		if checkdeposit == '0':
			if balanceforcheck >= 500: # Проверяем баланц для вклада
				msg = bot.send_message(message.from_user.id, 'Укажите сумму вклада от 500р до 1499р'
															 '\nПосле того, как вы укажите сумму вклада, с вашего счёта будут сняты средства и активируется бронзовый вклад')
				bot.register_next_step_handler(msg, reg_bronze_deposit)
			else:
				bot.send_message(message.from_user.id, 'У вас недостаточно средств на счету')
		else:
			bot.send_message(message.from_user.id, 'Бронзовый вклад у вас уже активирован')

# Серебряный вклад - ГОТОВО
	if message.data == markup.deposits_cb_silver_data:
		balanceforcheck = db.get_balance(message.from_user.id) # Получаем баланц
		user_id = message.from_user.id # Получаем ID
		checkdeposit = db.checkdeposit(message.from_user.id, 'silveractive')
		if checkdeposit == '0':
			if balanceforcheck >= 1500: # Проверяем баланц для вклада
				msg = bot.send_message(message.from_user.id, 'Укажите сумму вклада от 1500р до 2999р'
															 '\nПосле того, как вы укажите сумму вклада, с вашего счёта будут сняты средства и активируется серебряный вклад')
				bot.register_next_step_handler(msg, reg_silver_deposit)
			else:
				bot.send_message(message.from_user.id, 'У вас недостаточно средств на счету')
		else:
			bot.send_message(message.from_user.id, 'Серебряный вклад у вас уже активирован')

# Золотой вклад - ГОТОВО
	if message.data == markup.deposits_cb_gold_data:
		balanceforcheck = db.get_balance(message.from_user.id) # Получаем баланц
		user_id = message.from_user.id # Получаем ID
		checkdeposit = db.checkdeposit(message.from_user.id, 'goldactive')
		if checkdeposit == '0':
			if balanceforcheck >= 3000: # Проверяем баланц для вклада
				msg = bot.send_message(message.from_user.id, 'Укажите сумму вклада от 3000р'
															 '\nПосле того, как вы укажите сумму вклада, с вашего счёта будут сняты средства и активируется золотой вклад')
				bot.register_next_step_handler(msg, reg_gold_deposit)
			else:
				bot.send_message(message.from_user.id, 'У вас недостаточно средств на счету')
		else:
			bot.send_message(message.from_user.id, 'Золотой вклад у вас уже активирован')

# Регистрация бронзового влкдаа - ГОТОВО
def reg_bronze_deposit(message):
	sumbronzedeposit = message.text # Поулчаем сумму вклада
	typedeposit = 'Bronze' # Указываем тип вклада
	balanceforcheck = db.get_balance(message.from_user.id) # Поулчаем баланц
	if sumbronzedeposit.isdigit() == True: # Проверяем из чего состоит текст. Из цифр или букв
		if int(sumbronzedeposit) <= balanceforcheck: # Проверем баланц для регистрации вклада
			if int(sumbronzedeposit) >= 500 and int(sumbronzedeposit) < 1500: # Проверяем диапазон вклада
				bot.send_message(message.from_user.id, 'Вы зарегистрировали бронзовый вклад!')
				db.register_deposit(message.from_user.id, typedeposit, sumbronzedeposit) # РЕГИСТРАЦИЯ ВКЛАДА
			else:
				bot.send_message(message.from_user.id, 'Введённая вами сумма не подходит для данного вклада')
		else:
			bot.send_message(message.from_user.id, 'У вас недосточно средств на счету')
	else:
		bot.send_message(message.from_user.id, 'Сумма должна быть указана в рублях')

# Регистрация серебряного вклада - ГОТОВО
def reg_silver_deposit(message):
	sumsilverdeposit = message.text # Такой же алгоритм, как и при регистрации бронзового вклада
	typedeposit = 'Silver'
	balanceforcheck = db.get_balance(message.from_user.id)
	if sumsilverdeposit.isdigit() == True:
		if int(sumsilverdeposit) <= balanceforcheck:
			if int(sumsilverdeposit) >= 1500 and int(sumsilverdeposit) < 3000:
				bot.send_message(message.from_user.id, 'Вы зарегистрировали серебряный вклад!')
				db.register_deposit(message.from_user.id, typedeposit, sumsilverdeposit)
			else:
				bot.send_message(message.from_user.id, 'Введённая вами сумма не подходит для данного вклада')
		else:
			bot.send_message(message.from_user.id, 'У вас недостаточно средств на счету')
	else:
		bot.send_message(message.from_user.id, 'Сумма должна быть указана в рублях')

# Регистрация золотого вклада - ГОТОВО
def reg_gold_deposit(message):
	sumgolddeposit = message.text # Такой же алгоритм, как и при регистрации бронзового вклада
	typedeposit = 'Gold'
	balanceforcheck = db.get_balance(message.from_user.id)
	if sumgolddeposit.isdigit() == True:
		if int(sumgolddeposit) <= balanceforcheck:
			if int(sumgolddeposit) >= 3000:
				bot.send_message(message.from_user.id, 'Вы зарегистрировали золотой вклад!')
				db.register_deposit(message.from_user.id, typedeposit, sumgolddeposit)
			else:
				bot.send_message(message.from_user.id, 'Введённая вами сумма не подходит для данного вклада')
		else:
			bot.send_message(message.from_user.id, 'У вас недостаточно средств на счету')
	else:
		bot.send_message(message.from_user.id, 'Сумма должна быть указана в рублях')

# Вывести деньги\ввод карты ГОТОВО
def select_card_withdraw(message):
	global withdraw_card
	withdraw_card = message.text
	countdigit = len([i for i in withdraw_card if i.isdigit()])
	if countdigit == 16:
		msg = bot.send_message(message.from_user.id, 'Теперь введите сумму для вывода')
		bot.register_next_step_handler(msg, select_sum_withdraw)
	else:
		bot.send_message(message.from_user.id, 'Формат карты указан не верно')


# Вывести деньги\ввод суммы - ГОТОВО
def select_sum_withdraw(message):
	withdraw_sum = message.text
	get_balance = db.get_balance(message.from_user.id)

	try: 
		if int(withdraw_sum) <= get_balance and int(withdraw_sum) > 0:
			if int(withdraw_sum) >= 250:
				new_balance = get_balance - int(withdraw_sum)
				db.withdraw(message.from_user.id, new_balance)
				db.add_query(message.from_user.id, withdraw_sum, withdraw_card)
				bot.send_message(message.from_user.id, 'Заявка на вывод срдеств суммой в {}р оформлена успешно!'.format(withdraw_sum))
			else:
				bot.send_message(message.from_user.id, 'Минимальная сумма вывода 250р')
		else:
			bot.send_message(message.from_user.id, 'У вас недостаточно средств на счету')

	except ValueError:
		bot.send_message(message.from_user.id, 'Сумма должна быть указана в рублях')
# Закрыть запрос на вывод
def close_request(message):
	number = message.text # Ловим номер вкалда
	try:
		check = cur.execute("SELECT history FROM payment_query WHERE requestNumber = %s"%(number)).fetchone() # Проверяем существование вклада
	except:
		return bot.send_message(config.admin, 'Номер должен указываться в цифрах, а не в буквах :)')
	try:
		if check[0] == 'Yes':
			return bot.send_message(config.admin, 'Этот вклад уже закрыт!') # Проверка статуса вклада
	except:
		return bot.send_message(config.admin, 'Упсс... Такого запроса не существует')

	db.close_request(number) # Закрываем запрос
	sum = cur.execute("SELECT sum FROM payment_query WHERE requestNumber = %s"%(number)).fetchone() # Cумма запроса
	user_id = cur.execute("SELECT user_id FROM payment_query WHERE requestNumber = %s"%(number)).fetchone() # ID просящего
	balance = db.get_balance(user_id) # Баланц просящего
	balance = balance - sum[0]
	db.withdraw(user_id, balance) # Снять средства
	bot.send_message(config.admin, 'Запрос успешно закрыт')

def get_id_by(message):
	global user_id_by_balance
	user_id_by_balance = message.text # олучить id
	if user_id_by_balance.isdigit() == True:
		pass
	else:
		return bot.send_message(config.admin, 'ID может состоять только из цифр :)')

	check_id = db.check_id(user_id_by_balance)
	if check_id == 'notfound':
		return bot.send_message(config.admin, 'Такого ID нету в нашей базе')
	msg = bot.send_message(config.admin, 'Отлично. Теперь введите сумму перевода')
	bot.register_next_step_handler(msg, get_sum_by)

def get_sum_by(message):
	sum = message.text # получить сумму для пополнения
	if sum.isdigit() == True:
		balance = db.get_balance(user_id_by_balance) # получить баланц
		balance = balance + int(sum)
		db.withdraw(user_id_by_balance, balance) # обновить баланц
		bot.send_message(config.admin, 'Баланц пополнен')
		bot.send_message(user_id_by_balance, 'На ваш счёт начислено {}р'.format(sum))
	else:
		bot.send_message(config.admin, 'Сумма должна указыватья в цифрах :]')

def id_info(message):
	id = message.text
	if id.isdigit() == True:
		idinfo = db.idinfo(id)
		bot.send_message(config.admin, 'Информация по ID {0}\n\n{2} {1}\nДата регистрации - {3}\nБаланц - {4}р'.format(id, idinfo[1], idinfo[2], idinfo[3], idinfo[4]))
	else:
		bot.send(config.admin, 'ID не может содержать букв :}')
bot.polling(none_stop=True, interval=0)