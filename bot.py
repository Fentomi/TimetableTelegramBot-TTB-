from auth_data import *
from my_parsers import parser_morning
from telebot import TeleBot
import time

def main():
    bot = TeleBot(token=token) 
    @bot.message_handler(commands=['start']) 
    def start(message):
        chat_id = message.chat.id
        day_today = time.strftime('%A', time.gmtime(time.time())) 
        count_today = False 
        while True:
            now_hours_time = int(time.strftime('%H', time.gmtime(time.time()))) + 3 
            if now_hours_time >= 5 and now_hours_time <= 7 and count_today == False:
                text = parser_morning(url, header)
                bot.send_message(chat_id=chat_id, text=text, parse_mode='html')
                count_today = True
            if day_today != time.strftime('%A', time.gmtime(time.time())): 
                day_today = time.strftime('%A', time.gmtime(time.time()))
                count_today = False
            time.sleep(3600)

    bot.polling()

if __name__ == '__main__':
    main()
