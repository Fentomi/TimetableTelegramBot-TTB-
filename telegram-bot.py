import telebot
from bs4 import BeautifulSoup
from datetime import date
import requests
import groupparser
from groupparser import parser
from auth_data import token

def telegram_bot(token):
    bot = telebot.TeleBot(token)
    @bot.message_handler(commands=['start']) 
    def start(message):
        bot.send_message(message.chat.id, '[INFO] Пытаюсь зайти на сайт...')
        day_today = parser()
        print(day_today)
        bot.send_message(message.chat.id, day_today)
    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)
    