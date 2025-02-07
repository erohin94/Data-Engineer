# Заметки тг-бот

# Декоратор @bot.message_handler

Декоратор `@bot.message_handler` используется в библиотеке pyTelegramBotAPI (также известной как telebot) для обработки входящих сообщений в боте Telegram.

Позволяет задать обработчик для различных типов сообщений, которые может получить бот, таких как текстовые сообщения, фото, документы, кнопки и т. д.

**commands** — список команд, для которых бот будет вызывать обработчик. Например, `commands=['start', 'help']` обработает команду `/start` или `/help`.

Когда пользователь отправляет команду `/start` боту, срабатывает функция `handle_start`.

Параметр `message` — это объект, который содержит информацию о сообщении, отправленном пользователем. В частности, он включает в себя такие данные, как ID чата, текст сообщения, ID отправителя и другие детали.

`bot.send_message` — это метод, который отправляет сообщение в чат, откуда пришла команда.

`message.chat.id` — это идентификатор чата, в который нужно отправить ответ. Это поле получает из объекта message, чтобы отправить сообщение обратно в тот же чат.

```
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот.")
```

**func** — функция, которая принимает объект `message` и должна вернуть `True`, если обработчик должен сработать для данного сообщения. Например, `lambda message: message.text == 'Привет'` — сработает, если в сообщении будет текст `"Привет"`.

```
@bot.message_handler(func=lambda message: 'привет' in message.text.lower())
def handle_greeting(message):
    bot.send_message(message.chat.id, "Привет! Как дела?")
```

**content_types** — список типов содержимого, которые будут обрабатываться. Примеры типов: `'text'`, `'photo'`, `'document'`, `'location'`, `'audio'` и т. д. Например, `content_types=['photo']` будет обрабатывать только фото.

```
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "Отличное фото!")
```

**regexp** — можно использовать регулярные выражения для фильтрации сообщений. Это позволяет обрабатывать текстовые сообщения, которые соответствуют определенному шаблону.

```
import re

@bot.message_handler(regexp=r'\d{10}')
def handle_phone_number(message):
    bot.send_message(message.chat.id, "Это похоже на номер телефона.")
```

# Состояния пользователя, для ТГ бота

**Обновление состояния**

`state` - Cостояние пользователя.

`states` - Список, который будет хранить последовательность состояний этого пользователя.

`chat_id` - Идентификатор чата пользователя, ключ для хранения информации о его состоянии.

`attempts` - Счётчик количества попыток (начинается с 0).

```
user_states = {}

def update_user_state(chat_id, state):
    if chat_id not in user_states:
        user_states[chat_id] = {'states': [], 'attempts': 0}
    user_states[chat_id]['states'].append(state)
```

```
update_user_state(12345, 'START')
```

```
user_states[12345]
```
![image](https://github.com/user-attachments/assets/ba7ee1a6-dd8a-4d85-957d-38c7bca3fe3c)

```
update_user_state(12345, 'PROCESSING')
```

```
user_states[12345]
```

![image](https://github.com/user-attachments/assets/3fb5ca5b-ea4a-48ec-a4f5-1de0ac92e070)

```
update_user_state(67890, 'START')
```

```
user_states
```

![image](https://github.com/user-attachments/assets/5b0ae932-35cc-47db-8908-79b5f9af33a0)














































