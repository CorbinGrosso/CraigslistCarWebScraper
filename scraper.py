from requests import get
from bs4 import BeautifulSoup
import json


class DateTime:
    def __init__(self, datetime):
        self.year = int(datetime[:4])
        self.month = int(datetime[5:7])
        self.day = int(datetime[8:10])
        self.hour = int(datetime[11:13])
        self.minute = int(datetime[14:16])


def import_database():
    with open('Car_Model_List.json', 'r') as f:
        lines = f.readlines()
    lines = ''.join(lines)
    lines = json.loads(lines)
    return lines['results']


def filter_car_types(info):
    output = []
    for car in info:
        if car['Make'].lower() in makers:
            car_categories = car['Category'].split(',')
            for category in categories:
                category = ''.join(i for i in category.strip().lower() if not i.isdigit())
                if category in categories:
                    if car['Model'].lower() not in output:
                        output.append(car['Model'].lower())
    return output


def to_int(num):
    output = ''
    for i in num:
        if i.isdigit():
            output+=i 
    return int(output)


def get_all_relevant_posts_on_page(link):
    response = get(link)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    posts = html_soup.find_all('li', class_= 'result-row')
    
    for post in posts:
        price = post.a.text.strip()
        if price == '':
            continue
        price = to_int(price)
        if price >= min_price and price <= max_price:
            title = post.find('a', class_='result-title hdrlnk').text.lower()
            if 'sold' in title:
                continue
            if 'rent' in title:
                continue
            acceptable_car=False
            for car in valid_cars:
                if car in title:
                    acceptable_car=True
            if not acceptable_car:
                continue
            url = post.find('a', class_='result-title hdrlnk')['href']
            time_posted = DateTime(post.find('time', class_= 'result-date')['datetime'])
            if time_posted.year != 2021 or time_posted.month < 4:
                continue
            print(title)
            print(f"{time_posted.month}/{time_posted.day}/{time_posted.year}")
            print(url)
            print(price)
            print()
    next_page = html_soup.find('a', class_='button next')
    if next_page is not None:
        next_page = base_url + next_page['href']
        if next_page != link:
            get_all_relevant_posts_on_page(next_page)


max_price=4000
min_price=300
base_url="https://southjersey.craigslist.org"
search_url="https://southjersey.craigslist.org/d/cars-trucks/search/cta"
makers=['honda', 'toyota', 'acura', 'lexus', 'infiniti', 'nissan']
categories=['suv']
car_info = import_database()
valid_cars = filter_car_types(car_info)

get_all_relevant_posts_on_page(search_url)