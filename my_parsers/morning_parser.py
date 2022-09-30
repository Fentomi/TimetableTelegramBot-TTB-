from .func import html_get, repair_dayofweek, save_file, timetable_text_generator
from bs4 import BeautifulSoup

def parser_morning(url, header) -> str:
    html = html_get(url, header)
    soup = BeautifulSoup(html, 'lxml')

    col = soup.find('div', class_='row tab-pane active').find('div', class_='list col-md-2 today')
    try:
        dayofweek = col.find('div', class_='dayofweek').get_text()
        paras = col.find_all('div', class_='timetable_sheet')
    except AttributeError:
        return 'нет расписания на сегодня.'

    dayofweek = col.find('div', class_='dayofweek').get_text()
    dayofweek_repair = repair_dayofweek(dayofweek)
    text = f'{dayofweek_repair}\n\n'

    paras = col.find_all('div', class_='timetable_sheet')
    text = timetable_text_generator(paras, text)

    save_file(html, 'timetable')

    return text

if __name__ == '__main__':
    print(parser_morning())