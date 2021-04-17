"""3. Написать функцию, которая будет добавлять в
вашу базу данных только новые вакансии с сайта."""
from pymongo import MongoClient

from task_1_get_vacancy import get_vacancy as gv


def insert_the_new_vacancy(vacancy):
    data_inf = gv(vacancy)
    for i in data_inf:
        collection.update_one({'href': {'$eq': i['href']}}, {'$set': i}, upsert=True)


client = MongoClient('localhost', 27017)
db = client['vacancies']
collection = db['new_vacancies']
insert_the_new_vacancy('повар')
