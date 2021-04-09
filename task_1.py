"""
Посмотреть документацию к API GitHub, разобраться
как вывестисписок репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.
"""
import requests
import json


def list_repo(link, user):
    r = requests.get(f'{link}/users/{user}/repos')
    return list(x['name'] for x in r.json())


print(list_repo('https://api.github.com', 'EgorNi'))

user_name = 'EgorNi'
url = 'https://api.github.com'
rr = requests.get(f'{url}/users/{user_name}/repos')

with open('data.json', 'w') as f:
    json.dump(rr.json(), f)
