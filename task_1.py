"""1) Написать приложение, которое собирает основные новости с
сайтов news.mail.ru, lenta.ru, yandex.news
Для парсинга использовать xpath. Структура данных должна содержать:
- название источника,
- наименование новости,
- ссылку на новость,
- дата публикации
Нельзя использовать BeautifulSoup"""
import requests
from lxml import html
from pymongo import MongoClient


headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.72 Safari/537.36'
}
client = MongoClient('localhost', 27017)
db = client['news']
collection = db['news_scrap']


def lenta_news():
    info_list = []
    url = "https://lenta.ru/"
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    xpath_for_item = '//section[contains(@class, "row b-top7-for-main")]//div[contains(@class, "item")]'
    items = dom.xpath(xpath_for_item)
    for i in items:
        data = {}
        xpath_i_name = ".//a/text()"
        try:
            data['source'] = 'Lenta.ru'
            data['news_name'] = i.xpath(xpath_i_name)[0].replace(u"\xa0", u' ')
            data['news_url'] = url+i.xpath('.//a/@href')[0]
            data['news_date_time'] = i.xpath('.//a/time/@datetime')[0]
            info_list.append(data)
        except Exception as e:
            print(e)
    return info_list


def news_mail_ru():
    info_list = []
    url = "https://news.mail.ru/"
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    xpath_for_item = '//div[@class="wrapper"]//div[@data-module="TrackBlocks"]//div[contains(@class, "__item")]'
    items = dom.xpath(xpath_for_item)
    for i in items:
        data = {}
        xpath_i_name = './/span[contains(@class, "__title")]/text()'
        try:
            data['source'] = i.xpath(".//a/@href")[0]
            data['news_name'] = i.xpath(xpath_i_name)[0].replace(u"\xa0", u' ')
            data['news_url'] = i.xpath('.//a/@href')[0]
            # date_time = i.xpath('.//span[contains(@class, "js-ago")]//@datetime')
            # data['news_date_time'] = dtp.parser(date_time)
            data['news_date_time'] = i.xpath('//span[contains(@class, "js-ago")]//@datetime')[0].replace('T', ' ')
            info_list.append(data)
        except Exception as e:
            print(e)

    xpath_for_item = '//ul[contains(@data-module, "TrackBlocks")]//li[@class="list_item"]'
    items = dom.xpath(xpath_for_item)
    for i in items:
        data = {}
        xpath_i_name = './/a/text()'
        try:
            data['source'] = i.xpath(".//a/@href")[0]
            data['news_name'] = i.xpath(xpath_i_name)[0].replace(u"\xa0", u' ')
            data['news_url'] = i.xpath('.//a/@href')[0]
            data['news_date_time'] = i.xpath('//span[contains(@class, "js-ago")]//@datetime')[0].replace('T', ' ')
            info_list.append(data)
        except Exception as e:
            print(e)
    return info_list


def yandex_news():
    info_list = []
    url = "https://yandex.com/news/"
    r = requests.get(url, headers=headers)
    dom = html.fromstring(r.text)
    xpath_for_item = '//div[contains(@class, "news-top-flexible-stories")]/div'
    items = dom.xpath(xpath_for_item)
    for i in items:
        data = {}
        xpath_i_name = ".//h2/text()"
        try:
            data['source'] = i.xpath('.//span[contains(@class, "__source")]//a/text()')[0]
            data['news_name'] = i.xpath(xpath_i_name)[0].replace(u"\xa0", u' ')
            data['news_url'] = i.xpath('.//a/@href')[0]
            data['news_date_time'] = i.xpath(".//span[contains(@class, '__time')]/text()")[0]
            info_list.append(data)
        except Exception as e:
            print(e)
    return info_list


def put_news_into_db(collection, info_list):
    for item in info_list:
        collection.update_one({'$and': [{'news_name': {'$eq': item['news_name']}},
                                        {'source': {'$eq': item['source']}}]}, {'$set': item}, upsert=True)


news_mail = news_mail_ru()
put_news_into_db(collection, news_mail)
news_lenta = lenta_news()
put_news_into_db(collection, news_lenta)
news_yandex = yandex_news()
put_news_into_db(collection, news_yandex)
