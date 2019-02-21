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

    def __init__(self, key, dict_div={}, ul=None):
        self.key = key
        self.dict_div = dict_div
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
        for i in key:
            time.sleep(.05)
            username.send_keys(i)
        return username

    def radio_click(self, driver, id):
        driver.find_element_by_id(id).click()
        time.sleep(random.randint(2, 7))
        return True

    def get_text(self, driver, id):
        time.sleep(random.randint(2, 7))
        try:
            # text = driver.find_element_by_id(id).text
            html = driver.find_element_by_id(id).get_attribute('innerHTML')
            return html
        except NoSuchElementException:
            html = driver.find_element_by_class_name(id).get_attribute('innerHTML')
            # rows = driver.find_elements_by_id(id)
            # text = [row.text for row in rows]
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
        header = {'User-Agent':str(ua.chrome)}
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
        self.dict_div[url] = self.get_text(driver, 'columntext')
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
                self.dict_div[url] = table
            else:
                self.dict_div[url] = self.get_text(driver, 'pnlResult')
        else:
            self.radio_click(driver, 'unirad_1')
            username = self.input_key(driver, 'ogrnIp', ogrn)
            self.cap_loop(username, driver, 'btnSearch')

            self.dict_div[url] = self.get_text(driver, 'pnlResult')
        print('nalog_uwsfind_do')
        return self.dict_div

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
            self.dict_div[url] = self.get_text(driver, 'resultPanel')
        else:
            if boss_name:
                userfam = boss_name.split()[0]
                print(userfam)
                usernam = boss_name.split()[1]
                print(usernam)
                userotch = boss_name.split()[2]
                print(userotch)
                self.input_key(driver, 'otch', userotch)
                self.input_key(driver, 'fam', userfam)
                username = self.input_key(driver, 'nam', usernam)
                self.cap_loop(username, driver, 'btn-ok')
                self.dict_div[url] = self.get_text(driver, 'resultPanel')
            else:
                print('Имя не определено')
        print('nalog_disqualified_do')

    def zakupki(self, driver, key):
        """
        http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html
        """
        url = self.services[3]
        # 'http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html'
        driver.get(url)
        username = self.input_key(driver, 'searchString', key)
        username.submit()
        time.sleep(random.randint(2, 7))
        try:
            # fourth = driver.find_element_by_css_selector('table.searchDocTable').text
            self.dict_div[url] = self.get_text(driver, 'margBtm10')
        except NoSuchElementException:
            print('Поиск не дал результатов.')
        print('zakupki')

    def nalog_svl_do(self, driver, key):
        """
        https://service.nalog.ru/svl.do
        """
        url = self.services[4]
        # 'https://service.nalog.ru/svl.do'
        driver.get(url)
        username = self.input_key(driver, 'svlform_inn', key)
        self.cap_loop(username, driver, 'btn-ok')
        try:
            # fifth = driver.find_element_by_class_name('container').text
            self.dict_div[url] = self.get_text(driver, 'container')
        except NoSuchElementException:
            # fifth = driver.find_element_by_class_name('panel').text
            self.dict_div[url] = self.get_text(driver, 'panel')
        print('nalog_svl_do')

    def bankrot_fedresurs_debtorssearch(self, driver, key):
        """
        http://bankrot.fedresurs.ru/DebtorsSearch.aspx
        """
        url = self.services[5]
        driver.get(url)
        if self.ul is True:
            # 'http://bankrot.fedresurs.ru/DebtorsSearch.aspx'
            self.input_key(driver, 'ctl00_cphBody_OrganizationCode1_CodeTextBox', key)
            self.button(driver, 'ctl00_cphBody_btnSearch')
            self.dict_div[url] = self.get_text(driver, 'ctl00_cphBody_upList')
        else:
            time.sleep(random.randint(2, 7))
            self.radio_click(driver, 'ctl00_cphBody_rblDebtorType_1')
            time.sleep(random.randint(2, 7))
            self.input_key(driver, 'ctl00_cphBody_PersonCode1_CodeTextBox', key)
            self.button(driver, 'ctl00_cphBody_btnSearch')
            self.dict_div[url] = self.get_text(driver, 'ctl00_cphBody_upList')
        print('bankrot_fedresurs_debtorssearch')

    def nalog_zd_do(self, driver, key):
        """
        https://service.nalog.ru/zd.do
        """
        url = self.services[6]
        # 'https://service.nalog.ru/zd.do'
        driver.get(url)
        username = self.input_key(driver, 'inn', key)
        # captcha = driver.find_element_by_id('captcha')
        self.cap_loop(username, driver, 'btn_send')
        # seventh = self.get_text(driver, 'pnlResults')
        self.dict_div[url] = self.get_text(driver, 'pnlResults')
        print('nalog_zd_do')

    def nalog_bi_do(self, driver, key):
        """
        https://service.nalog.ru/bi.do
        """
        url = self.services[7]
        # 'https://service.nalog.ru/bi.do'
        driver.get(url)
        self.radio_click(driver, 'unirad_0')
        username = self.input_key(driver, 'innPRS', key)
        self.bik(driver, 'bikPRS')
        self.cap_loop(username, driver, 'btnSearch')
        # eighth = self.get_text(driver, 'pnlResultData')
        self.dict_div[url] = self.get_text(driver, 'pnlResultData')
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
            self.dict_div[url] = self.get_text(driver, 'ctl00_cphBody_upDisqList')
        else:
            print('Имя не определено')
        print('bankrot_fedresurs_disqualificantslist')

    def fiz(self, boss_name, key):
        """
        Физ
        'Поиск сведений в реестре дисквалифицированных лиц',
        'https://service.nalog.ru/disqualified.do'
        'Единый федеральный реестр сведений о банкротстве',
        'http://bankrot.fedresurs.ru/DebtorsSearch.aspx'
        """
        driver = webdriver.Chrome()

        self.nalog_disqualified_do(driver, boss_name)
        # self.bankrot_fedresurs_debtorssearch(driver, key)

        driver.close()
        return True

    def ip_min(self, key, ogrn):
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
        driver = webdriver.Chrome()

        self.nalog_uwsfind_do(driver, ogrn)
        self.nalog_bi_do(driver, key)
        self.zakupki(driver, key)

        driver.close()
        return True

    def ip_max(self, key, boss_name):
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
        driver = webdriver.Chrome()

        self.se_fedresurs(driver, key)
        self.nalog_disqualified_do(driver, boss_name)

        driver.close()
        return True

    def ur_min(self, key, ogrn):
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
        driver = webdriver.Chrome()

        self.nalog_uwsfind_do(driver, ogrn)
        self.zakupki(driver, key)
        self.nalog_bi_do(driver, key)

        driver.close()
        return True

    def ur_max(self, boss_name, key):
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
        driver = webdriver.Chrome()

        self.nalog_disqualified_do(driver, boss_name)
        self.nalog_svl_do(driver, key)
        # self.bankrot_fedresurs_debtorssearch(driver, key)
        self.nalog_zd_do(driver, key)
        # self.bankrot_fedresurs_disqualificantslist(driver, boss_name)

        driver.close()
        return True

    def get_data_from_zachestnyibiznes(self, link):
        result = requests.get(link).text
        soup = bs(result, 'lxml')

        inn = soup.find(id='inn').text

        pre_ogrn = soup.find(id='ogrn').text
        ogrn = [x for x in pre_ogrn]

        table = soup.find('table')
        bosses_header = soup.find(text='Учредители').parent.parent
        bosses = bosses_header.find('table')
        bosses_links = bosses.find_all('a')
        bosses_inn = []
        for i in bosses_links:
            if i.get('href').startswith('/fl/'):
                try:
                    int(i.text)
                    bosses_inn.append(i.text)
                except ValueError:
                    continue

        print('inn', inn)
        print('ogrn', ogrn)
        # print(bosses)
        print(bosses_inn)

        return(inn, ogrn, bosses_inn)

    def zachestnyibiznes(self):
        u = 'https://zachestnyibiznes.ru/search?query={}'.format(self.key)
        # proxi = self.get_proxi()
        # header = self.user_agent()
        #
        # result = requests.get(u, proxies={'http': 'http://'+proxi}, headers=header).text
        result = requests.get(u).text
        soup = bs(result, 'lxml')
        table = soup.find('table')
        boss_name = table.find(itemprop="founder").text
        link = 'https://zachestnyibiznes.ru{}'.format(table.find('a').get('href'))
        print(link)
        company_name = list(table.find('a').children)[0]

        if '/ul/' in link:
            self.ul = True
        else:
            self.ul = False

        print('Это юл? ', self.ul)

        today = datetime.datetime.now()
        date_of_registration = dateparser.parse(table.find(itemprop="foundingDate").text)
        date_result = today - date_of_registration

        address = list(table.find(itemprop="address").children)[2]
        inn, ogrn, bosses_inn = self.get_data_from_zachestnyibiznes(link)

        print('Дата регистрации: {} дней'.format(date_result.days))
        list_key = [x for x in self.key]
        for i in bosses_inn:
            print(i)
            i = [x for x in i]
            self.fiz(boss_name, i)

        if date_result.days < 60:
            """
            # days = 30
            # ogrn = '1197746013563'
    
            # if days < 60:
            """
            print('меньше 60 дней')
            if self.ul is True:
                self.ur_min(list_key, ogrn)
            else:
                self.ip_min(list_key, ogrn)
        else:
            print('больше 60 дней')
            if self.ul is True:
                self.ur_min(list_key, ogrn)
                self.ur_max(boss_name, list_key)

            else:
                self.ip_min(list_key, ogrn)
                self.ip_max(list_key, boss_name)

        return(self.ul, inn, ogrn, address, boss_name, company_name, bosses_inn, self.dict_div)
        # return True


if __name__ == '__main__':
    service = Service('7704471520')

    service.zachestnyibiznes()
    print(service.dict_div.keys())
