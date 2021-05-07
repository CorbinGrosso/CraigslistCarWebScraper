from requests import get
from bs4 import BeautifulSoup


class DateTime:
    def __init__(self, datetime):
        self.year = int(datetime[:4])
        self.month = int(datetime[5:7])
        self.day = int(datetime[8:10])
        self.hour = int(datetime[11:13])
        self.minute = int(datetime[14:16])


def get_all_relevant_posts_on_page(link):
    response = get(link)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    posts = html_soup.find_all('li', class_= 'result-row')
    
    for post in posts:
        price = int(''.join(filter(str.isdigit, post.a.text.strip())))
        if price >= min_price and price <= max_price:
            title = post.find('a', class_='result-title hdrlnk').text
            if 'sold' in title.lower():
                continue
            url = post.find('a', class_='result-title hdrlnk')['href']
            time_posted = DateTime(post.find('time', class_= 'result-date')['datetime'])
            if time_posted.year != 2021 or time_posted.month < 5:
                continue
            print(title)
            print(f"{time_posted.month}/{time_posted.day}/{time_posted.year}")
            print(url)
            print(price)
            print()


max_price=4000
min_price=1

get_all_relevant_posts_on_page("https://southjersey.craigslist.org/search/cta?query=suv&purveyor-input=all")