import traceback
import telebot
from extensions import Convert, APIExeption
from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '''Чтобы начать работу введите команду боту 
    в следующим формате:
    <имя валюты> <в какую валюту перевести> <количество>
            
            Увидеть все доступные валюты: 
            введите команду /values'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()

    try:
        if len(values) != 3:
            raise APIExeption(f"Неверное количество параметров!")
        answer = Convert.get_price(*values)
    except APIExeption as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        base, quote, amount = message.text.split()
        bot.send_message(message.chat.id, answer)


if __name__ == '__main__':

    bot.polling()

