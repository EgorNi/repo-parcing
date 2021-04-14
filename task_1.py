"""Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы) с сайтов Superjob и HH.
Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv."""
import json
import time
import requests
import pandas as pd
import traceback
import sys
from bs4 import BeautifulSoup as bs


def get(link, header, options):
    r = requests.get(link, headers=header, params=options)
    return r


def save_json(f_name, inf):
    with open(f_name, 'w', encoding='utf8') as f:
        json.dump(inf, f, indent=2, ensure_ascii=False)


def load_json(f_name):
    with open(f_name, 'r', encoding='utf8') as f:
        return json.load(f)


name_of_vacancy = input('enter vacancy name: ')
url = "https://hh.ru/search/vacancy"
params = {'text': name_of_vacancy, 'clusters': 'true', 'enable_snippets': 'true'}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}
resp = get(url, headers, params)
soup = bs(resp, 'html.parser')
next_button = True
vacancy_info = []
i = 0
while True:
    items = soup.find_all(attrs={'class': 'vacancy-serp__vacancy-title'})
    for item in items:
        data = {}
        a = item.find('a', attrs={'class': 'bloko-link'})
        data['href'] = a.attrs['href']
        data['name'] = a.text
        data['city/region'] = item.find(attrs={'data-qa': 'vacancy-serp-vacancy-address'}).text
        a = item.find('a', attrs={'class': 'bloko-link bloko-link_secondary'})
        company = a.text.replace('\xa0', '')
        data['company'] = company
        try:
            price = item.find(attrs={'class': 'vacancy-serp-item_sidebar'}).text.replace('\u202f', '').split()
            if price[0] == 'от':
                data['price_min'] = price[1]
                data['price_max'] = '-'
            elif price[0] == 'до':
                data['price_min'] = '-'
                data['price_max'] = price[1]
            else:
                data['price_min'] = price[0]
                data['price_max'] = price[2]
                data['currency'] = price[-1]
            data['site_from'] = resp.url
        except Exception as e:
            e_type, e_val, e_tb = sys.exc_info()
            err = f"Error on page{params['page']} with object №{i}, name: {data['name']}"
            with open(f"hh_('name_of_vacancy)_errors.txt", 'a', encoding='utf8') as f:
                print(err)
                traceback.print_exception(e_type, e_val, e_tb)

        vacancy_info.append(data)
        i += 1
    if next_button is None:
        break
    params['page'] += 1
    resp = get(url, headers, params)
    soup = bs(resp, 'html.parser')
    next_button = soup.find('a', attrs={'data-qa': 'pager-next'})
    time.sleep(0.1)

save_json(f'hh_{name_of_vacancy}_result.json', vacancy_info)
data_2 = load_json(f'hh_{name_of_vacancy}_result.json')
df = pd.DataFrame(data_2)
pd.options.display.width = 1100
pd.options.display.max_colwidth = 15
with pd.options_context('display.max_rows', None, 'display.max_columns', None):
    print(df)
