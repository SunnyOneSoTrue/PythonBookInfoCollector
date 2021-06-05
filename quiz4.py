import random
import requests
from bs4 import BeautifulSoup
from time import sleep
import sqlite3 as sql

conn = sql.connect("books.sqlite3")
c = conn.cursor()

c.execute('''create table if not exists books
(id integer primary key autoincrement, title varchar(50), author varchar(25), status varchar(25))''')

page_num = 1
full_list = []

while page_num <= 5:

    url = f'https://wordery.com/classic-crime-FFC?viewBy=grid&resultsPerPage=20&page={page_num}&leadTime[]=any'
    r = requests.get(url)
    content = r.text

    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all('div', {'class': 'c-book__body'})

    for each in items:
        new_list = ()

        title = each.a.text
        title = title.replace('\n', '')

        new_list += (title,)

        author = each.find('span', {'class', 'c-book__by'}).a.text
        new_list += (author,)

        available = each.find('span', {'class', 'c-book__atb'}).text
        available = available[1: 22]
        new_list += (avaible,)

        full_list.append(new_list)

    page_num += 1
    rand_num = random.randint(15, 20)
    sleep(rand_num)

c.executemany("insert into book_info(title, author, status) values(?, ?, ?)", full_list)
conn.commit()

conn.close()



