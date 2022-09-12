import telebot
from groupparser import parser, timemorning
from auth_data import token
import time

#функция проверяет изменения и присылает 
def timetable_difference(bot, message):
    timetable_difference = parser() #функция находит изменения в расписании в форме текста изменений. и даты.
    if timetable_difference != 'nothing':
        bot.send_message(message.chat.id, timetable_difference)

#функция проверяет, наступило ли утро, и в случае этого отправляет расписание на сегодня и завтра.
def morning_message(bot, message):
    if timemorning(time.time()) == True:
        #timetable_morning = morning_parser()
        bot.send_message(message.chat.id, timetable_morning)



def telegram_bot(token):
    bot = telebot.TeleBot(token)
    @bot.message_handler(commands=['start']) 
    def start(message):
        while True:
            timetable_difference(bot, message)
            #morning_message(bot, message)
            time.sleep(3600)
    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)
    