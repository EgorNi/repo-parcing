import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pprint import pprint


def get_content(request):
    url = "https://vk.com/tokyofashion"
    options = Options()
    options.add_argument("start-maximized")
    driver_path = "./chromedriver"
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get(url)
    time.sleep(3)
    lens_field = driver.find_element_by_xpath(".//a[contains(@class, 'tab_search')]").get_attribute('href')
    driver.get(lens_field)
    time.sleep(1)
    search_field = driver.find_element_by_id("wall_search")
    search_field.send_keys(request + Keys.ENTER)
    while True:
        try:
            button_not_now = driver.find_element_by_xpath('.//a[@class="JoinForm__notNow"]')
            button_not_now.click()
        except Exception as e:
            print(e)
        finally:
            driver.find_element_by_tag_name('html').send_keys(Keys.END)
            time.sleep(3)
            end_of_wall = driver.find_element_by_id('fw_load_more')
            stopscroll = end_of_wall.get_attribute('style')
            if stopscroll == 'display: none;':
                break
    content = driver.find_elements_by_xpath("//div[contains(@class, '_post_content')]")
    data = []
    for i in content:
        try:
            content_info = {}
            content_info['date_of_post'] = i.find_element_by_class_name("rel_date").text
            content_info['post_content'] = i.find_element_by_class_name("wall_post_text").text.replace('\n', '')
            content_info['post_url'] = i.find_element_by_class_name("post_link").get_attribute('href')
            content_info['count_likes'] = i.find_element_by_xpath(".//a[contains(@class, '_like')]//div[@class="
                                                                  "'like_button_count']").text
            content_info['count_shares'] = i.find_element_by_xpath(".//a[contains(@class, '_share')]//div[@class="
                                                                   "'like_button_count']").text
            # content_info['count_views'] = i.find_element_by_xpath('.//div[contains(@class, "_views _views")]').\
            #     get_attribute('title')
            # get_images = i.find_elements_by_xpath('.a//[contains(@aria-label, "Original")]')
            # images_list = []
            # for image in get_images:
            #     image_link = image.get_attribute('aria-label').split()[2]
            #     images_list.append(image_link)
            #     data.append(images_list)
            data.append(content_info)
        except Exception as e:
            print(e)
    driver.quit()
    return data


def put_data_into_db(db, contnt):
    for item in contnt:
        db.update_one({'$and': [{'post_content': {'$eq': item['post_content']}},
                                {'post_url': {'$eq': item['post_url']}}]}, {'$set': item}, upsert=True)


search_request = input('enter your request: ')
get_post = get_content(search_request)
pprint(get_post)

client = MongoClient('localhost', 27017)
db = client['tokyo_fashion_posts']
collection = db['posts']
put_data_into_db(collection, get_post)
