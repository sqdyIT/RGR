import telebot
import sqlite3
from telebot import types

TOKEN = "6899923236:AAGlizl8WwXRs-BT1Aa3AEA0q9P2ECNILgs"
bot = telebot.TeleBot(TOKEN)


keyboard = types.InlineKeyboardMarkup(row_width=2)
BPMN_button = types.InlineKeyboardButton('Диаграмма BPMN', callback_data='bpmn')
dashboard_button = types.InlineKeyboardButton('Дашборд', callback_data='dashboard')
help_button = types.InlineKeyboardButton('Помощь', callback_data='help')
order_button = types.InlineKeyboardButton('Начать инвестировать', callback_data='order')
keyboard.add(BPMN_button, help_button, dashboard_button, order_button)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот управляет процессом инвестиций. '
                         'Отправьте /help, чтобы узнать доступные команды.')
@bot.message_handler(commands=['help'])

def help(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

# Обработка кнопки 'Диаграмма BPMN'
def BPMN_but(message):
    bpmn_markup = types.InlineKeyboardMarkup(row_width=1)
    button9 = types.InlineKeyboardButton('Описание BPMN', callback_data='bpmn_function1')
    bpmn_markup.add(button9)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=bpmn_markup)

# Ответ на запрос о создателе
def About_(message):
    bot.reply_to(message, 'Максим 2ИБ-1')

# кнопки для действий с Дашбордом
def Dashboard_but(message):
    dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
    button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
    dashboard_markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)

# кнопки для действий с помощью
def Help_but(message):
    help_markup = types.InlineKeyboardMarkup(row_width=1)
    button15 = types.InlineKeyboardButton('Как пользоваться ботом', callback_data='help_function1')
    button16 = types.InlineKeyboardButton('Контакты поддержки', callback_data='help_function2')
    help_markup.add(button15, button16)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=help_markup)

# кнопки для действий с оформлением заказа
def Order_but(message):
    order_handler(message)

CALLBACK_D = {
    "Диаграмма BPMN" : BPMN_but,
    "Создатель" : About_,
    "Дашборд" : Dashboard_but,
    "Помощь": Help_but,
    "Оформить заказ" : Order_but
     }


CALLBACK_D_BUTTON = {
    "bpmn" : BPMN_but,
    "dashboard" : Dashboard_but,
    "help": Help_but,
    "order" : Order_but,
     }

@bot.message_handler(func=lambda message: True)
def home_screen(message):
    if message.text in CALLBACK_D:
        CALLBACK_D[message.text](message)
    else:
        # Обработка иных сообщений
        bot.reply_to(message, 'Не понимаю /help', reply_markup=keyboard)

def order_handler(message):
    bot.send_message(message.chat.id, 'Введите ваше имя:')
    bot.register_next_step_handler(message, enter_invest_name)

def enter_invest_name(message):
    order = {}
    order['invest_name'] = message.text
    bot.send_message(message.chat.id, f'Отлично, {message.text}! Во что инвестируем:')
    bot.register_next_step_handler(message, enter_invest_profile, order)

#Обработчик для ввода места подачи груза
def enter_invest_profile(message, order):
    order['invest_profile'] = message.text
    bot.send_message(message.chat.id, f'Сумма: {message.text}. Рубли')
    bot.register_next_step_handler(message, enter_sum, order)

#Обработчик для ввода пункта назначения
def enter_sum(message, order):
    order['sum'] = message.text
    bot.send_message(message.chat.id, f'Пункт назначения: {message.text}. Заказ оформлен!')
    # отчет
    report = f'Отчет по вложению:\n\n' \
             f'Имя инвестора: {order["invest_name"]}\n' \
             f'Тип инвестиции: {order["invest_profile"]}\n' \
             f'Вкладывамая сумма: {order["sum"]}\n'

    # Отправка отчета пользователю
    bot.send_message(message.chat.id, report)
    # Создание подключения к базе данных SQLite
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Создание таблицы для заказов, если ее еще нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invest_name TEXT,
            invest_profile TEXT,
            sum TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO orders (invest_name, invest_profile, sum)
        VALUES (?, ?, ?)
    ''', (order['invest_name'], order['invest_profile'], order['sum']))
    conn.commit()

#INSERT INTO table_name
#VALUES (value1, value2, value3, ...);


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in CALLBACK_D_BUTTON:
        CALLBACK_D_BUTTON[call.data](call.message)

    #текстовое описание bpmn
    elif call.data == 'bpmn_function1':
        bot.send_message(call.message.chat.id,
                         'Диаграммы BPMN (Business Process Model and Notation) представляют собой стандартный '
                         'графический язык, разработанный для моделирования бизнес-процессов в организации. '
                         'Этот инструмент обеспечивает единый и понятный способ визуализации бизнес-процессов, '
                         'что помогает более эффективно понимать, анализировать и оптимизировать деятельность компании')

        bpmn_function_markup = types.InlineKeyboardMarkup(row_width=1)

        button11 = types.InlineKeyboardButton('Как телеграм бот может помочь в процессе '
                                              'обработки инвестиций', callback_data='bpmn_function3')

        bpmn_function_markup.add(button11)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=bpmn_function_markup)

    elif call.data == 'bpmn_function3':
        bot.send_message(call.message.chat.id, 'Телеграм-бот может значительно упростить и ускорить процесс обработки инвестиций. '
                                               'Вот несколько способов, как он может быть полезен:'
                                               'Получение заказов: Клиенты могут отправлять заказы через бота, '
                                               'Управление бюджетом: пользователь должен иметь возможность корректировать бюджет.'
                                               'Интеграция с платежными системами: Для удобства клиентов бот может интегрироваться с '
                                               'платежными системами, позволяя им оплачивать услуги напрямую через телеграм.'
                                               'Обратная связь и поддержка: Клиенты могут общаться с ботом для задания вопросов, '
                                               'уточнения деталей заказа или предоставления обратной связи.')

        #кнопки дашборда
    elif call.data == 'dashboard':
        dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
        button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
        dashboard_markup.add(button1, button2)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)
    elif call.data == 'dashboard_function1':
        bot.send_message(call.message.chat.id, 'Дашборд предназначен для визуализации и анализа данных об инвестициях. '
                                               'Содержит пять ключевых графиков, предоставляющих информацию о различных аспектах рынка')

        dashboard_function_markup = types.InlineKeyboardMarkup(row_width=1)

        button3 = types.InlineKeyboardButton('График 1', callback_data='dashboard_function3')
        button4 = types.InlineKeyboardButton('График 2', callback_data='dashboard_function4')
        button5 = types.InlineKeyboardButton('График 3', callback_data='dashboard_function5')
        dashboard_function_markup.add(button3, button4, button5, button6, button7, button8)
        bot.send_message(call.message.chat.id, 'Выберите график:', reply_markup=dashboard_function_markup)

    elif call.data == 'dashboard_function2':
        bot.send_message(call.message.chat.id, 'Ссылка на GitHub: https://github.com/sqdyIT/RGR')
    elif call.data == 'dashboard_function3':
        image1_url = 'https://raw.githubusercontent.com/sqdyIT/RGR/graphik1.jpg'
        bot.send_photo(call.message.chat.id, image1_url, caption='Это круговой график')
    elif call.data == 'dashboard_function4':
        image2_url = 'https://raw.githubusercontent.com/sqdyIT/RGR/graphik2.jpg'
        bot.send_photo(call.message.chat.id, image2_url, caption='Это временной график')
    elif call.data == 'dashboard_function5':
        image3_url = 'https://raw.githubusercontent.com/sqdyIT/RGR/graphik3.jpg'
        bot.send_photo(call.message.chat.id, image3_url, caption='Это точечный график')

bot.infinity_polling()