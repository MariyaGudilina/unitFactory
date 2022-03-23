import telebot
from config import exchanges, TOKEN
from utils import Convertor, ConvertionExseption


# API работает в ограниченном режиме

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def send_welcome(message: telebot.types.Message):
    text = f"Введите запрос в виде - <название валюты исходное>" \
           f" <название валюты перевод> <количество исходной валюты>" \
           f" Пример" \
           f" <доллар><рубль><10> \nУвидеть список доступных валют команда: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    val = message.text.split(' ')
    try:
        if len(val) != 3:
            raise ConvertionExseption('Неверное количество параметров!')
        text = Convertor.convert(*val)

    except ConvertionExseption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось отправить команду\n{e}')
    else:
        bot.reply_to(message, text)




    #


bot.polling(none_stop=True)
