from cgitb import html
from bs4 import BeautifulSoup
import time
import os
from datetime import date
import requests

#функция обновляет каждый час на случай краха сайта index.html 
def check_index(html): 
    work_dir = os.getcwd() 
    html_path = work_dir + '\site\index.html'
    html_info =  os.lstat(html_path, dir_fd=None)
    time_modification = html_info[8] 
    time_current = time.time() 
    time_difference = time_current - time_modification
    if time_difference > 3600:
        with open('site/index.html', 'w', encoding='utf-8') as OpenFile:
            OpenFile.write(html)


def get_html(link): #
    res = requests.get(link)
    if res.status_code == 200:
        html = res.text
        check_index(html)
        return html
    else:
        with open('site/index.html', encoding='utf-8') as OpenFile:
            html = OpenFile.read()
            return html.text

def parser(): #основное тело парсера, из которого вызываются другие функции.
    while True:
        html = get_html('https://ruz.narfu.ru/?timetable&group=16555') #здесь можно менять ссылку для другой группы этого же самого сайта.
        soup = BeautifulSoup(html, 'lxml')
        day_today = date.today()
        return day_today

if __name__ == '__main__':
    parser()