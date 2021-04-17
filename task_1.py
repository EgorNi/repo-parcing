"""1. Развернуть у себя на компьютере/виртуальной машине/хостинге
MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД."""
import json
from pymongo import MongoClient
from pprint import pprint


def insert_to_mongo(file):
    with open(file, encoding='utf-8') as f:
        file_data = json.load(f)
    f2 = collection.insert_many(file_data)
    return f2


client = MongoClient('localhost', 27017)
db = client['vacancies']
collection = db['new_vacancies']
insert_to_mongo('hh_data engineer_result.json')
result = collection.find({})
for i in result:
    pprint(i)
