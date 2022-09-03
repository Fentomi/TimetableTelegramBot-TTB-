from multiprocessing.resource_sharer import stop
from bs4 import BeautifulSoup
from datetime import date
import requests

def get_html():
    try:
        res = requests.get('https://ruz.narfu.ru/?timetable&group=16555')
        if res.status_code == 200:
            html = res.text
            return html
        else:
            return ('[ERROR] Ошибка получения html страницы.')
    except:
        return ('[ERROR] Ошибка получения html страницы.')

def get_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup

def mainparser():
    html = get_html()
    if type(html) == str:
        return html
    else:
        soup = get_soup(html)
        day_today = date.today()
        return day_today

if __name__ == '__main__':
    mainparser()