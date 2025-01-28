import telebot
from telebot import types

# Замените на ваш токен
TOKEN = 'token-80c'
bot = telebot.TeleBot(TOKEN)

# Создадим словарь для хранения состояний пользователей
user_state = {}

# Функция для обновления состояния пользователя
def update_user_state(user_id, state):
    user_state[user_id] = state

# Функция для получения состояния пользователя
def get_user_state(user_id):
    return user_state.get(user_id, None)

# Функция для создания клавиатуры
def create_keyboard(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
    for btn in buttons:
        markup.add(types.KeyboardButton(btn))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_keyboard(["Меню 1", "Меню 2"])
    bot.send_message(message.chat.id, text=f"Выбор меню", reply_markup=markup)
    update_user_state(message.chat.id, 'start')

   
# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def func(message):

    state = get_user_state(message.chat.id)

    #Обработчик кнопки назад
    if message.text == "Назад":
        if state in ['podmenu 1', 'podmenu 2']:
            markup = create_keyboard(["Меню 1", "Меню 2"])
            bot.send_message(message.chat.id, text="Вернулись в главное меню", reply_markup=markup)
            update_user_state(message.chat.id, 'start')

        elif state in ['podmenu 1.1.1', 'podmenu 1.2.1']:
            markup = create_keyboard(["Подменю 1.1", "Подменю 1.2", "Назад"])
            bot.send_message(message.chat.id, text="Вернулись в подменю 1.1 - 1.2", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 1')

        elif state in ['podmenu 2.1.1', 'podmenu 2.2.1']:
            markup = create_keyboard(["Подменю 2.1", "Подменю 2.2", "Назад"])
            bot.send_message(message.chat.id, text="Вернулись в подменю 2.1-2.2", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 2')

        elif state == 'pusto':
            markup = create_keyboard(["Меню 1", "Меню 2"])
            bot.send_message(message.chat.id, text="Вернулись в главное меню", reply_markup=markup)
            update_user_state(message.chat.id, 'start')
    
    #Обработчик состояния start      
    elif state == 'start':
        if message.text == "Меню 1":
            markup = create_keyboard(["Подменю 1.1", "Подменю 1.2", "Назад"])
            bot.send_message(message.chat.id, text=f"Выбрали {message.text}", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 1')

        elif message.text == "Меню 2":
            markup = create_keyboard(["Подменю 2.1", "Подменю 2.2", "Назад"])
            bot.send_message(message.chat.id, text=f"Выбрали {message.text}", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 2')

    elif state in ['podmenu 1', 'podmenu 2']:
        if message.text == "Подменю 1.1":
            markup = create_keyboard(["Подменю 1.1.1", "Назад"])
            bot.send_message(message.chat.id, text=f"Выбрали {message.text}", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 1.1.1')

        elif message.text == "Подменю 1.2":
            markup = create_keyboard(["Подменю 1.2.1", "Назад"])
            bot.send_message(message.chat.id, text=f"Выбрали {message.text}", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 1.2.1')

        elif message.text == "Подменю 2.1":
            markup = create_keyboard(["Подменю 2.1.1", "Назад"])
            bot.send_message(message.chat.id, text=f"Выбрали {message.text}", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 2.1.1')

        elif message.text == "Подменю 2.2":
            markup = create_keyboard(["Подменю 2.2.1", "Назад"])
            bot.send_message(message.chat.id, text=f"Выбрали {message.text}", reply_markup=markup)
            update_user_state(message.chat.id, 'podmenu 2.2.1')


    elif state in ['podmenu 1.1.1', 'podmenu 1.2.1', 'podmenu 2.1.1', 'podmenu 2.2.1']:
        if message.text in ["Подменю 1.1.1", "Подменю 1.2.1", "Подменю 2.1.1", "Подменю 2.2.1"]:
            markup = create_keyboard(["Назад"])
            bot.send_message(message.chat.id, text=f"Выбрали {message.text} здесь ничего нет", reply_markup=markup)
            update_user_state(message.chat.id, 'pusto')


bot.polling(non_stop=True)
