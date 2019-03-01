import datetime
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import time
import random
import dateparser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Service:
    services = (
        'http://se.fedresurs.ru',
        'https://service.nalog.ru/uwsfind.do',
        'https://service.nalog.ru/disqualified.do',
        'http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html',
        'https://service.nalog.ru/svl.do',
        'http://bankrot.fedresurs.ru/DebtorsSearch.aspx',
        'https://service.nalog.ru/zd.do',
        'https://service.nalog.ru/bi.do',
        'http://bankrot.fedresurs.ru/DisqualificantsList.aspx',

        'https://zachestnyibiznes.ru',
    )

    headers = (
        'Федресурс',
        'Сведения о юридических лицах и индивидуальных предпринимателях, '
        'в отношении которых представлены документы для государственной регистрации',
        'Поиск сведений в реестре дисквалифицированных лиц',
        'Портал Закупок Результаты поиска',
        'Сведения о лицах, в отношении которых факт невозможности участия '
        '(осуществления руководства) в организации установлен (подтвержден) в судебном порядке',
        'Единый федеральный реестр сведений о банкротстве. Должники.',
        'Сведения о юридических лицах, имеющих задолженность по уплате налогов и/или'
        ' не представляющих налоговую отчетность более года',
        'Система информирования банков о состоянии обработки электронных документов (311-П, 440-П)',
        'Единый федеральный реестр сведений о банкротстве. Дисквалифицированные лица.',
    )

    def __init__(self, key, ul, dict_service={}):
        self.key = key
        self.dict_service = dict_service
        self.ul = ul

    def bik(self, driver, id_name):
        bikn = driver.find_element_by_id(id_name)
        bik = [x for x in '000000000']
        for i in bik:
            time.sleep(.05)
            bikn.send_keys(i)
        return True

    def button(self, driver, id_name):
        try:
            driver.find_element_by_id(id_name).click()
            time.sleep(random.randint(2, 7))
            return True
        except NoSuchElementException:
            driver.find_element_by_class_name(id_name).click()
            time.sleep(random.randint(2, 7))
            return True

    def input_key(self, driver, form_id, key):
        username = driver.find_element_by_id(form_id)
        time.sleep(random.randint(3, 7))
        for i in key:
            time.sleep(.06)
            username.send_keys(i)
        return username

    def radio_click(self, driver, id):
        driver.find_element_by_id(id).click()
        time.sleep(random.randint(2, 7))
        return True

    def get_text(self, driver, id):
        time.sleep(random.randint(2, 7))
        try:
            html = driver.find_element_by_id(id).get_attribute('innerHTML')
            return html
        except NoSuchElementException:
            html = driver.find_element_by_class_name(id).get_attribute('innerHTML')
            return html

    def cap(self, driver):
        captcha = driver.find_element_by_id('captcha')
        f = [x for x in input('введите капчу: ')]
        for i in f:
            time.sleep(.05)
            captcha.send_keys(i)
        return True

    def cap_loop(self, username, driver, btn_id=None):
        er = True
        while er:
            self.cap(driver)
            if btn_id:
                self.button(driver, btn_id)
            else:
                username.submit()
            try:
                er = driver.find_element_by_id('errors_captcha').text
                print(er)
            except NoSuchElementException:
                er = False
        print('Цифры с картинки введены верно')

    def get_proxi(self):
        proxy = requests.get('https://free-proxy-list.net/').text
        soup = bs(proxy, 'lxml')
        table = soup.find('table', id='proxylisttable').find('tbody')
        f = []
        for i in table:
            url = i.findAll('td')[0].text
            port = i.findAll('td')[1].text
            f.append(url+':'+port)
            proxi = random.choice(f)
        return proxi

    def url(self, proxi, link):
        ua = UserAgent()
        header = {'User-Agent': str(ua.chrome)}
        ya = link
        res = requests.get(ya, proxies={'http': 'http://'+proxi}).text
        return res

    def user_agent(self):
        # ua = UserAgent()
        header = {'User-Agent':str(UserAgent().chrome)}
        return header

    def se_fedresurs(self, driver, key):
        """
        http://se.fedresurs.ru
        """
        url = self.services[0]
        driver.get(url)
        self.input_key(driver, 'ctl00_tbCompanySearch', key)
        self.button(driver, 'ctl00_Button2')
        result = driver.find_element_by_id('ctl00_MainContent_upnCompanyList')
        result.find_element_by_class_name('title').click()
        self.dict_service[url] = self.get_text(driver, 'columntext')
        print('se_fedresurs')

    def nalog_uwsfind_do(self, driver, ogrn):
        """
        https://service.nalog.ru/uwsfind.do
        доделать строку для физ
        """
        url = self.services[1]
        driver.get(url)

        if self.ul is True:

            username = self.input_key(driver, 'ogrnUl', ogrn)
            self.cap_loop(username, driver, 'btnSearch')
            table = self.get_text(driver, 'tableResultData')
            if table:
                self.dict_service[url] = table
            else:
                self.dict_service[url] = self.get_text(driver, 'pnlResult')
        else:
            self.radio_click(driver, 'unirad_1')
            username = self.input_key(driver, 'ogrnIp', ogrn)
            self.cap_loop(username, driver, 'btnSearch')

            self.dict_service[url] = self.get_text(driver, 'pnlResult')
        print('nalog_uwsfind_do')
        return self.dict_service

    def nalog_disqualified_do(self, driver, boss_name):
        """
        https://service.nalog.ru/disqualified.do
        доделать иф элсе для физ
        """
        url = self.services[2]
        driver.get(url)
        if self.ul is True:
            username = self.input_key(driver, 'orgInn', self.key)
            self.cap_loop(username, driver, 'float-right')
            self.dict_service[url] = self.get_text(driver, 'resultPanel')
        else:
            if boss_name:
                userfam = boss_name.split()[0]
                print(userfam)
                usernam = boss_name.split()[1]
                print(usernam)
                userotch = boss_name.split()[2]
                print(userotch)
                time.sleep(random.randint(3, 7))
                self.input_key(driver, 'otch', userotch)
                time.sleep(random.randint(3, 7))
                self.input_key(driver, 'fam', userfam)
                time.sleep(random.randint(3, 7))
                username = self.input_key(driver, 'nam', usernam)
                self.cap_loop(username, driver, 'btn-ok')
                self.dict_service[url] = self.get_text(driver, 'resultPanel')
            else:
                print('Имя не определено')
        print('nalog_disqualified_do')

    def zakupki(self, driver, key):
        """
        http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html
        """
        url = self.services[3]
        driver.get(url)
        username = self.input_key(driver, 'searchString', key)
        username.submit()
        time.sleep(random.randint(2, 7))
        try:
            self.dict_service[url] = self.get_text(driver, 'margBtm10')
        except NoSuchElementException:
            print('Поиск не дал результатов.')
        print('zakupki')

    def nalog_svl_do(self, driver, key):
        """
        https://service.nalog.ru/svl.do
        """
        url = self.services[4]
        driver.get(url)
        username = self.input_key(driver, 'svlform_inn', key)
        self.cap_loop(username, driver, 'btn-ok')
        try:
            self.dict_service[url] = self.get_text(driver, 'container')
        except NoSuchElementException:
            self.dict_service[url] = self.get_text(driver, 'panel')
        print('nalog_svl_do')

    def bankrot_fedresurs_debtorssearch(self, driver, key):
        """
        http://bankrot.fedresurs.ru/DebtorsSearch.aspx
        """
        url = self.services[5]
        driver.get(url)
        if self.ul is True:
            self.input_key(driver, 'ctl00_cphBody_OrganizationCode1_CodeTextBox', key)
            self.button(driver, 'ctl00_cphBody_btnSearch')
            self.dict_service[url] = self.get_text(driver, 'ctl00_cphBody_upList')
        else:
            time.sleep(random.randint(2, 7))
            self.radio_click(driver, 'ctl00_cphBody_rblDebtorType_1')
            time.sleep(random.randint(2, 7))
            self.input_key(driver, 'ctl00_cphBody_PersonCode1_CodeTextBox', key)
            self.button(driver, 'ctl00_cphBody_btnSearch')
            self.dict_service[url] = self.get_text(driver, 'ctl00_cphBody_upList')
        print('bankrot_fedresurs_debtorssearch')

    def nalog_zd_do(self, driver, key):
        """
        https://service.nalog.ru/zd.do
        """
        url = self.services[6]
        driver.get(url)
        username = self.input_key(driver, 'inn', key)
        self.cap_loop(username, driver, 'btn_send')
        self.dict_service[url] = self.get_text(driver, 'pnlResults')
        print('nalog_zd_do')

    def nalog_bi_do(self, driver, key):
        """
        https://service.nalog.ru/bi.do
        """
        url = self.services[7]
        driver.get(url)
        self.radio_click(driver, 'unirad_0')
        username = self.input_key(driver, 'innPRS', key)
        self.bik(driver, 'bikPRS')
        self.cap_loop(username, driver, 'btnSearch')
        self.dict_service[url] = self.get_text(driver, 'pnlResultData')
        print('nalog_bi_do')

    def bankrot_fedresurs_disqualificantslist(self, driver, boss_name):
        """
        http://bankrot.fedresurs.ru/DisqualificantsList.aspx
        """

        if boss_name:
            url = self.services[8]
            driver.get(url)
            self.input_key(driver, 'ctl00_cphBody_tbFio', boss_name)
            self.button(driver, 'ctl00_cphBody_btnSearch')
            self.dict_service[url] = self.get_text(driver, 'ctl00_cphBody_upDisqList')
        else:
            print('Имя не определено')
        print('bankrot_fedresurs_disqualificantslist')

    def fiz(self, boss_name, key, driver):
        """
        Физ
        'Поиск сведений в реестре дисквалифицированных лиц',
        'https://service.nalog.ru/disqualified.do'
        'Единый федеральный реестр сведений о банкротстве',
        'http://bankrot.fedresurs.ru/DebtorsSearch.aspx'
        """
        print('serv fiz start')

        self.nalog_disqualified_do(driver, boss_name)
        # self.bankrot_fedresurs_debtorssearch(driver, key)
        print('serv fiz end')

        return True

    def ip_min(self, key, ogrn, driver):
        """
        Ип мин
        Физ +
        'Сведения о юридических лицах и индивидуальных предпринимателях,
         в отношении которых представлены документы для государственной регистрации',
        'https://service.nalog.ru/uwsfind.do'
        'Система информирования банков о состоянии обработки электронных документов
         (311-П, 440-П)',
        'https://service.nalog.ru/bi.do'
        'Портал Закупок Результаты поиска',
        'http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html'
        """
        print('serv ip_min start')

        self.nalog_uwsfind_do(driver, ogrn)
        self.nalog_bi_do(driver, key)
        self.zakupki(driver, key)

        print('serv ip_min end')

        return True

    def ip_max(self, key, boss_name, driver):
        """
        ИП мах
        Ип мин +
        'Единый федеральный реестр юридически значимых сведений о
         фактах деятельности юридических лиц, индивидуальных предпринимателей и
          иных субъектов экономической деятельности
        http://se.fedresurs.ru
        'Поиск сведений в реестре дисквалифицированных лиц',
        'https://service.nalog.ru/disqualified.do'
        """
        print('serv ip_max start')

        self.se_fedresurs(driver, key)
        self.nalog_disqualified_do(driver, boss_name)
        print('serv ip_max start')

        return True

    def ur_min(self, key, ogrn, driver):
        """
        Юр мин
        'Сведения о юридических лицах и индивидуальных предпринимателях,
         в отношении которых представлены документы для государственной регистрации',
        'https://service.nalog.ru/uwsfind.do'
        'Портал Закупок Результаты поиска',
        'http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html'
        'Система информирования банков о состоянии обработки электронных документов
         (311-П, 440-П)',
        ‌'https://service.nalog.ru/bi.do'
        """
        print('serv ur_min start')

        self.nalog_uwsfind_do(driver, ogrn)
        self.zakupki(driver, key)
        self.nalog_bi_do(driver, key)
        print('serv ur_min end')

        return True

    def ur_max(self, boss_name, key, driver):
        """
        Юр мах
        Юр мин +
        'Поиск сведений в реестре дисквалифицированных лиц',
        'https://service.nalog.ru/disqualified.do'
        'Сведения о лицах, в отношении которых факт невозможности участия
         \(осуществления руководства\) в организации установлен \(подтвержден\)
          в судебном порядке',
        'https://service.nalog.ru/svl.do'
        'Единый федеральный реестр сведений о банкротстве',
        'http://bankrot.fedresurs.ru/DebtorsSearch.aspx'
        'Сведения о юридических лицах, имеющих задолженность
         по уплате налогов и/или не представляющих налоговую отчетность более года',
        'https://service.nalog.ru/zd.do'
        """
        print('serv ur_max start')

        self.nalog_disqualified_do(driver, boss_name)
        self.nalog_svl_do(driver, key)
        # self.bankrot_fedresurs_debtorssearch(driver, key)
        self.nalog_zd_do(driver, key)
        # self.bankrot_fedresurs_disqualificantslist(driver, boss_name)
        print('serv ur_max end')

        return True
