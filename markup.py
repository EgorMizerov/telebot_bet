from telebot import types

main_menu = '🏠 Главное меню'

# Start Markup
start_markup = types.ReplyKeyboardMarkup(True)
start_button_deposits = '🏦 Вклады'
start_button_faq = '❓ О сервисе'
start_button_cabinet = '🔐 Кабинет'
start_markup.row(start_button_cabinet)
start_markup.row(start_button_deposits, start_button_faq)

# Admin Markup
admin_markup = types.ReplyKeyboardMarkup(True)
admin_button_users_deposits = 'Вклады пользователей'
admin_button_restart = 'Обновить'
admin_button_withdrawal_requests = 'Запросы на вывод'
admin_button_close_request = 'Закрыть запрос'
admin_buttont_top_up_balance = 'Пополнить баланс'
admin_markup.row(admin_button_users_deposits)
admin_markup.row(admin_button_withdrawal_requests, admin_button_close_request)
admin_markup.row(admin_buttont_top_up_balance, admin_button_restart, main_menu)

# Analytical Markup
analytical_markup = types.ReplyKeyboardMarkup(True)
analytical_button_name = 'Информация по ID'
analytical_button_id = 'ID пользователей'
analytical_button_users = 'Кол-во пользователей'
analytical_button_deposits = 'Кол-во вкладов'
analytical_button_balance = 'Сумма всех баланцов'
analytical_markup.row(analytical_button_id, analytical_button_name)
analytical_markup.row(analytical_button_deposits)
analytical_markup.row(analytical_button_users, main_menu, analytical_button_balance)


# FAQ Markup
faq_markup = types.InlineKeyboardMarkup()
faq_cb_faq_data = 'faq_cb_faq'
faq_cb_activity_data = 'faq_cb_activity'
faq_button_faq = types.InlineKeyboardButton(text = 'FAQ', callback_data = faq_cb_faq_data)
faq_button_activity = types.InlineKeyboardButton(text = 'Деятельность', callback_data = faq_cb_activity_data)
faq_markup.add(faq_button_faq, faq_button_activity)

# Кабинет Markup
cabinet_markup = types.ReplyKeyboardMarkup(True)
cabinet_button_top_up = '➕ Пополнить'
cabinet_button_balance = '💵 Баланц'
cabinet_button_withdraw = '➖ Вывести'
cabinet_button_my_deposits = 'Мои вклады'
cabinet_button_conclusion_history = 'История выводов'
cabinet_markup.row(cabinet_button_top_up, cabinet_button_balance, cabinet_button_withdraw)
cabinet_markup.row(cabinet_button_my_deposits, cabinet_button_conclusion_history)
cabinet_markup.row(main_menu)

# Вклады Markup
deposits_markup = types.InlineKeyboardMarkup()
deposits_cb_bronze_data = 'deposits_cb_bronze'
deposits_cb_silver_data = 'deposits_cb_silver'
deposits_cb_gold_data = 'deposits_cb_gold'
deposits_button_make_bronze_deposit = types.InlineKeyboardButton(text = 'Бронзовый', callback_data = deposits_cb_bronze_data)
deposits_button_make_silver_deposit = types.InlineKeyboardButton(text = 'Серебряный', callback_data = deposits_cb_silver_data)
deposits_button_make_gold_deposit = types.InlineKeyboardButton(text = 'Золотой', callback_data = deposits_cb_gold_data)
deposits_markup.add(deposits_button_make_bronze_deposit, deposits_button_make_silver_deposit)
deposits_markup.add(deposits_button_make_gold_deposit)