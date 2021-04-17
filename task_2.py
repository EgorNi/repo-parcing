"""2. Написать функцию, которая производит поиск и выводит на
экран вакансии с заработной платой больше введённой суммы, а
также использование одновременно мин/макс зарплаты.
Необязательно - возможность выбрать вакансии без указанных зарплат"""
from pymongo import MongoClient
from pprint import pprint



def seek_the_vacancy(numb):
    for answer in collection.find({'price_min': {'$gt': numb}}):
        pprint(answer)


def seek_the_vacancy2(numb):
    for answer in collection.find({'$or': [{'price_max': {'$gt': numb}}, {'price_min': {'$gt': numb}}]}):
        pprint(answer)


client = MongoClient('localhost', 27017)
db = client['vacancies']
collection = db['new_vacancies']
# salary = input('enter the required salary: ')
seek_the_vacancy(200000)
# seek_the_vacancy2(200000)
