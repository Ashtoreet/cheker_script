import datetime
import requests
from bs4 import BeautifulSoup as bs
import time
import random
import dateparser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class CheckObj:

    def __init__(
            self, key, dict_div={}, ul=None, date_result=None, ogrn=None,
            address=None, boss_name=None, company_name=None, bosses_inn=[]
    ):
        self.key = key
        self.dict_div = dict_div
        self.ul = ul
        self.date_result = date_result
        self.ogrn = ogrn
        self.address = address
        self.boss_name = boss_name
        self.company_name = company_name
        self.bosses_inn = bosses_inn

    def get_data_from_zachestnyibiznes(self, link):
        result = requests.get(link).text
        soup = bs(result, 'lxml')

        self.ogrn = soup.find(id='ogrn').text
        # ogrn = [x for x in pre_ogrn]

        # table = soup.find('table')
        bosses_header = soup.find(text='Учредители').parent.parent
        bosses = bosses_header.find('table')
        bosses_links = bosses.find_all('a')
        bosses_inn = []
        for i in bosses_links:
            if i.get('href').startswith('/fl/'):
                try:
                    int(i.text)
                    self.bosses_inn.append(i.text)
                except ValueError:
                    continue

        print('ogrn', self.ogrn)
        print(bosses_inn)

        return True

    def zachestnyibiznes(self):
        u = 'https://zachestnyibiznes.ru/search?query={}'.format(self.key)
        # proxi = self.get_proxi()
        # header = self.user_agent()
        # result = requests.get(u, proxies={'http': 'http://'+proxi}, headers=header).text
        result = requests.get(u).text
        soup = bs(result, 'lxml')
        table = soup.find('table')
        self.boss_name = table.find(itemprop="founder").text
        link = 'https://zachestnyibiznes.ru{}'.format(table.find('a').get('href'))
        print(link)
        self.company_name = list(table.find('a').children)[0]

        if '/ul/' in link:
            self.ul = True
        else:
            self.ul = False

        print('Это юл? ', self.ul)

        today = datetime.datetime.now()
        date_of_registration = dateparser.parse(table.find(itemprop="foundingDate").text)
        self.date_result = today - date_of_registration

        self.address = list(table.find(itemprop="address").children)[2]
        self.get_data_from_zachestnyibiznes(link)

        print('Дата регистрации: {} дней'.format(self.date_result.days))

        return True

    def egrul(self):
        url = 'https://egrul.nalog.ru/index.html'

        driver = webdriver.Chrome()
        driver.get(url)
        username = driver.find_element_by_id('query')
        for i in self.key:
            time.sleep(.05)
            username.send_keys(i)
        time.sleep(random.randint(2, 7))
        driver.find_element_by_id('btnSearch').click()
        try:
            driver.find_element_by_id('noDataFound')
            driver.close()
            return False
        except NoSuchElementException:
            driver.close()
            return True
