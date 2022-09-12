from bs4 import BeautifulSoup
import time
import datetime
import requests
import lxml

#функция сравнивает время на компьютере и возвращает True, если утреннее время
def timemorning(nowtime): #time.time в аргументе
    nowtime_struct = time.gmtime(nowtime)
    hours = nowtime_struct[3]+3
    if hours >= 4 and hours <= 8:
        return True
    else:
        return False

#функция достанет из строчки "понедельник, 12.09.2022" дату для определения текущего дня.
def check_day(get_data): 
    new_text = get_data.split()
    return new_text[1]

#получает сегодняшнюю дату и преобразует ее в удобную для обработки форму.
def today_repair_date():
    time_struct = time.gmtime(time.time())
    year = time_struct[0]
    month = time_struct[1]
    day = time_struct[2]
    today = str(datetime.date(day=day, month=month, year=year))
    num_list = today.split('-')
    repair_data = f'{num_list[2]}.{num_list[1]}.{num_list[0]}'
    return repair_data

#функция получает строку формы "2022-09-12" и преобразует в "12.09.2022"
def repair_data(today):
    num_list = today.split('-')
    repair_data = f'{num_list[2]}.{num_list[1]}.{num_list[0]}'
    return repair_data

#функция принимает объект супа на неделю и делает отсортированный по датам список с колонками.
def list_sort(timetable_week):
    list_sort = list() #создание списка с датами недели.
    dates = timetable_week.find_all('div', 'dayofweek')
    for i in dates:
        date = check_day(i.get_text())
        list_sort.append(date)

    list_sort_bs4 = [0,1,2,3,4,5] #создание второго список bs4, который будет заполнен в соответствии с первым списком.
    list_cols_one = timetable_week.find_all('div', class_='list col-md-2')
    list_col_one_today = timetable_week.find('div', class_='list col-md-2 today')
    list_col_one_last = timetable_week.find('div', class_='list last col-md-2')
    list_cols_one.append(list_col_one_today)
    list_cols_one.append(list_col_one_last)
    for elem in list_cols_one:
        date1 = check_day(elem.find('div', class_='dayofweek').get_text())
        for i in list_sort:
            if date1 == i:
                num = list_sort.index(i)
                list_sort_bs4[num] = elem
    return list_sort_bs4

#функция будет получать html и выдавать колонки пар новой версии
def create_list_cols_one(html_one):
    soup_one = BeautifulSoup(html_one, 'lxml')
    timetable_one_week1 = soup_one.find('div', class_='row tab-pane active')
    return list_sort(timetable_one_week1)

#функция будет получать html и выдавать колонку пар старой версии
def create_list_cols_two(html_two):
    soup_two = BeautifulSoup(html_two, 'lxml')
    timetable_two_week1 = soup_two.find('div', class_='row tab-pane active')
    return list_sort(timetable_two_week1)

#функция сравнивает столбцы расписания первого и второго html'я на предмет изменений.
def check_html_difference(html_one, html_two): #(html-one сайт)(html-two последняя сохраненная версия)
    today = today_repair_date()
    list_cols_one = create_list_cols_one(html_one)
    list_cols_two = create_list_cols_two(html_two)

    count = 0 #счетчики, который будет считать повторения после получения схожей даты. будем анали-
    #зировать только сегодняшнюю и завтрашнюю дату на наличие обновлений.

    while count < 2:
        for list_col_one in list_cols_one:
            get_data = check_day(list_col_one.find('div', class_='dayofweek').get_text())
            if count == 1:
                list_col_yesterday_one = list_col_one
                count += 1
            if get_data == today:
                first_check_day = get_data
                list_col_today_one = list_col_one
                count += 1

    count = 0 #обнуляем счетчик

    while count < 2:
        for list_col_two in list_cols_two: #цикл сохраняет два объекта супа- сегодняшний и следующий после него.
            get_data = check_day(list_col_two.find('div', class_='dayofweek').get_text())
            if count == 1:
                list_col_yesterday_two = list_col_two
                count += 1
            if get_data == first_check_day:
                list_col_today_two = list_col_two
                count += 1
    
    #если изменений нет:
    if list_col_today_one == list_col_today_two and list_col_yesterday_one == list_col_yesterday_two:
        return 'нет изменений, милорд!'
    #если изменения в первом дне:
    elif list_col_today_one != list_col_today_two and list_col_yesterday_one == list_col_yesterday_two:
        print('сработало это условие!')
        with open('test3.txt', 'w', encoding='utf-8') as file:
            file.write(f"""Изменения коснулись сегодня, {get_data}.
Сегодняшний день старого расписания= {list_col_today_one.get_text()}
Сегодняшний день нового расписания={list_col_today_two.get_text()}
""")
        return 'изменения сегодня блять!'
    #если изменения завтра:
    elif list_col_today_one == list_col_today_two and list_col_yesterday_one != list_col_yesterday_two:
        return 'изменения на завтра завези, бля'
    #если изменения в обоих днях:
    elif list_col_today_one != list_col_today_two and list_col_yesterday_one != list_col_yesterday_two:
        return 'изменения в двух днях, еблан!'



        
def get_html(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    res = requests.get(link, headers=headers)
    res.encoding='utf-8'
    if res.status_code == 200:
        html_one = res.text
        return html_one
    else:
        with open('site/index.html', encoding='utf-8') as OpenFile:
            html = OpenFile.read()
            return html.text

def parser(): #основное тело парсера, из которого вызываются другие функции.
    html_one = get_html('https://ruz.narfu.ru/?timetable&group=16555') #здесь можно менять ссылку для другой группы этого же самого сайта.
    with open(r'site\index.html', encoding='utf-8') as OpenFile:
        html_two = OpenFile.read()
    return check_html_difference(html_one, html_two)

if __name__ == '__main__':
    parser()