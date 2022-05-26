#!/usr/bin/python3
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox


URL = r'https://leetcode.com/problemset/algorithms/?page='
MAX_PAGE = 42
NAME_CLASS = [
    'h-5 hover:text-primary-s dark:hover:text-dark-primary-s',
    'h-5 hover:text-primary-s dark:hover:text-dark-primary-s opacity-60'
]
ACCEPTANCE_STYLE = [
    'box-sizing:border-box;flex:100 0 auto;min-width:0px;width:100px',
    'box-sizing: border-box; flex: 100 0 auto; min-width: 0px; width: 100px;'
]
DIFFICULTY_CLASS = ['text-olive dark:text-dark-olive',
                    'text-yellow dark:text-dark-yellow',
                    'text-pink dark:text-dark-pink'
                    ]
PARSE_DATA = {
    'id': [],
    'title': [],
    'acceptance': [],
    'difficulty': []
}


def parse_leetcode(driver, delay):
    for page in range(1, MAX_PAGE + 1):
        url_page = f"{URL}{page}"
        print(url_page)
        driver.get(url_page)
        time.sleep(delay)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        title = soup.find_all('a', class_=NAME_CLASS)
        acceptance = soup.find_all(style=ACCEPTANCE_STYLE)
        difficulty = soup.find_all('span', class_=DIFFICULTY_CLASS)

        if not len(title) == len(acceptance) == len(difficulty):
            driver.close()
            exit('Что-то пошло не так. '
                 'Проверьте имена классов, по которым идет поиск.')

        for index in range(len(title)):
            id_title, name = title[index].text.split('.')
            accept = acceptance[index].text[:-1]
            PARSE_DATA['id'].append(int(id_title))
            PARSE_DATA['title'].append(name)
            PARSE_DATA['acceptance'].append(accept)
            PARSE_DATA['difficulty'].append(difficulty[index].text)

    driver.close()
    df = pd.DataFrame(PARSE_DATA)
    df.to_csv('leetcode.csv', sep='\t', encoding='utf-8')


if __name__ == '__main__':
    parse_leetcode(driver=Firefox(), delay=5)
