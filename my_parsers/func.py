import requests
from bs4 import BeautifulSoup
from time import strftime, gmtime, time

#переменная, в которой нуждаются многие.
dayweek_today = strftime('%A', gmtime(time()))

#функция, извлекающая html-код из страницы или последней сохраненной версии.
def html_get(url, header) -> str:
    res = requests.get(url, headers=header)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        html = res.text
    elif url == 'https://ruz.narfu.ru/?timetable&group=16555':
        with open(r'cache\timetable.html') as file:
            html = file.read
    elif url == 'https://www.gismeteo.ru/weather-severodvinsk-3914/':
        with open(r'cache\weather.html') as file:
            html = file.read
    return html

def repair_dayofweek(dayofweek) -> str:
    dayofweek_split = dayofweek.split(',')
    dayofweek_repair = ''
    for i in dayofweek_split:
        new = ''.join(i.split()) + ' '
        dayofweek_repair += new
    return dayofweek_repair

def timetable_text_generator(paras=list, text=str) -> str:
    for para in paras:
        num_para = para.find('span', class_='num_para').get_text()
        time_para = 'пустая пара'
        kindOfWork = ''
        discipline = ''
        auditorium = ''
        group = ''
        try:
            time_para_one = para.find('span', class_='time_para').get_text()
            kindOfWork = para.find('span', class_='kindOfWork').get_text()
            discipline = para.find('span', class_='discipline').get_text()
            auditorium_b = para.find('span', class_='auditorium').find('b').get_text()
            auditorium_other = para.find('span', class_='auditorium').find('b').next_sibling
            time_para = time_para_one.lstrip()
            auditorium_other = ''.join(auditorium_other.split())
            auditorium_other_split = auditorium_other.split(',')
            auditorium = auditorium_b + ', ' + auditorium_other_split[-1]
        except:
            print('что-то пошло не так')
        try:
            group = para.find('span', class_='group').get_text()
        except:
            print('мы нашли предателя!')
        if time_para != '' and discipline != '':
            text += f'{num_para}) <u>[{time_para}]</u>\n{kindOfWork}\n<pre>{discipline}</pre>\n{auditorium}\n<i>{group}</i>\n\n'
        else:
            text += f'{num_para}) [{time_para}]\n\n'

    return text

def save_file(html, text='timetable/weather'):
    with open(f'cache\{text}.html', 'w', encoding='utf-8') as file:
        file.write(html) 

def wind_info(wind_list) -> list:
    wild_num = 0
    count = 0
    for wind in wind_list:
        num = wind.get_text()
        num = ''.join(num.split(' '))
        try:
            num = int(num)
        except:
            list_num = num.split('-')
            a = int(list_num[0])
            b = int(list_num[1])
            num = round((b+a)/2)
        if count == 0:
            min_num = num
            max_num = num
            count += 1
        if min_num > num:
            min_num = num
        elif max_num < num:
            max_num = num
        wild_num += num
    
    mean_wild = round(wild_num/len(wind_list), 2)

    wind_info = [mean_wild, min_num, max_num]
    return wind_info   