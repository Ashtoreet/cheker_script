from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import time


class Fl(object):
    """docstring for Fl."""
    def __init__(self, object, fio=None, info=None):
        self.innfl = object[0]
        self.ogrnip = object[1]
        self.fio = fio
        self.info = info

    def cap(self, driver):
        captcha = driver.find_element_by_id('captcha')
        f = [x for x in input('введите капчу: ')]
        for i in f:
            time.sleep(.1)
            captcha.send_keys(i)
        return True

    def bik(self, driver, id_name):
        bikn = driver.find_element_by_id(id_name)
        bik = [x for x in '000000000']
        for i in bik:
            time.sleep(.1)
            bikn.send_keys(i)
        return True

    def button(self, driver, id_name):
        try:
            driver.find_element_by_id(id_name).click()
            time.sleep(3)
            return True
        except NoSuchElementException:
            driver.find_element_by_class_name(id_name).click()
            time.sleep(3)
            return True

    def input_key(self, driver, form_id, key):
        username = driver.find_element_by_id(form_id)
        for i in key:
            time.sleep(.1)
            username.send_keys(i)
        return username

    def radio_click(self, driver, id):
        driver.find_element_by_id(id).click()
        time.sleep(2)
        return True

    def get_text(self, driver, id):
        time.sleep(5)
        try:
            text = driver.find_element_by_id(id).text
            return text
        except NoSuchElementException:
            rows = driver.find_elements_by_id('listItemContent')
            text = [row.text for row in rows]
            return text

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

    # def check_using_service(self):
    #     # service_url = 'https://egrul.nalog.ru'
    #     service_url = 'file:///Users/Ksihris/projects/pro/service_pro/ser.html'
    #     driver = webdriver.Chrome()
    #
    #     driver.get(service_url)
    #     # driver.find_element_by_link_text("Индивидуальный предприниматель/КФХ").click()
    #     username = self.input_key(driver, "ogrninnfl", self.innfl)
    #
    #     self.cap_loop(username, driver, 'captcha')
    #
    #     driver.get('file:///Users/Ksihris/projects/pro/service_pro/ser2.html')
    #     text = driver.find_element_by_id('resultContent').find_elements_by_tag_name('td')
    #
    #     if self.ogrnip is None:
    #         print('огрн нет')
    #         self.ogrnip = text[1].text
    #     else:
    #         print('огрн есть')
    #
    #     self.fio = text[0].text
    #     print(text[0].text.capitalize().format())
    #
    #     user_input = input('Close?: ',)
    #     driver.close()

    def services(self):
        key = [x for x in self.innfl]
        ogrnip = [x for x in self.ogrnip]
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox(executable_path='C:\\Python\geckodriver.exe')

        # 1
        driver.get('http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html')
        username = self.input_key(driver, 'searchString', key)
        username.submit()
        time.sleep(4)
        try:
            first = driver.find_element_by_css_selector('table.searchDocTable').text
        except NoSuchElementException:
            first = 'Ничего не найдено.'

        # 2
        driver.get('https://service.nalog.ru/bi.do')
        self.radio_click(driver, 'unirad_0')
        username = self.input_key(driver, "innPRS", key)
        self.bik(driver, "bikPRS")
        self.cap_loop(username, driver, 'btnSearch')
        second = self.get_text(driver, 'pnlResultData')

        # 3
        driver.get('http://se.fedresurs.ru/IndividualEntrepreneurs')
        self.input_key(driver, 'ctl00_MainContent_txtCode', key)
        self.button(driver, 'ctl00_MainContent_btnSearch')
        time.sleep(5)
        try:
            link = driver.find_element_by_class_name('fn')
            name = link.text
            link.click()
            time.sleep(5)
            third = self.get_text(driver, 'tabs')
            print(name)
        except NoSuchElementException:
            third = driver.find_element_by_id('ctl00_MainContent_upnIndEntrepreneurList').text
            name = None

        # 4
        driver.get('http://bankrot.fedresurs.ru/DebtorsSearch.aspx')
        time.sleep(2)
        self.radio_click(driver, 'ctl00_cphBody_rblDebtorType_1')
        time.sleep(3)
        self.input_key(driver, 'ctl00_cphBody_PersonCode1_CodeTextBox', key)
        self.button(driver, 'ctl00_cphBody_btnSearch')
        fourth = self.get_text(driver, 'ctl00_cphBody_upList')

        # 6
        driver.get('https://service.nalog.ru/uwsfind.do')
        self.radio_click(driver, 'unirad_1')
        username = self.input_key(driver, 'ogrnIp', ogrnip)
        self.cap_loop(username, driver, 'btnSearch')
        name = driver.find_element_by_class_name('uws-result-item-value').text
        print(name)
        sixth = self.get_text(driver, 'pnlResult')

        # 5, работает только с третьим пунктом(берет там name)
        if name:
            driver.get('http://bankrot.fedresurs.ru/DisqualificantsList.aspx')
            self.input_key(driver, 'ctl00_cphBody_tbFio', name)
            self.button(driver, 'ctl00_cphBody_btnSearch')
            fifth = self.get_text(driver, 'ctl00_cphBody_upDisqList')
        else:
            fifth = 'Имя не определено'

        # 7, работает только с третьим пунктом(берет там name)
        if name:
            driver.get('https://service.nalog.ru/disqualified.do')
            userfam = name.split()[0]
            print(userfam)
            usernam = name.split()[1]
            print(usernam)
            self.input_key(driver, 'fam', userfam)
            username = self.input_key(driver, 'nam', usernam)
            self.cap_loop(username, driver, 'btn-ok')
            seventh = self.get_text(driver, 'resultPanel')
        else:
            seventh = 'Имя не определено'

        self.info = (
                    ('http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html : ', first),
                    ('https://service.nalog.ru/bi.do', second),
                    ('https://service.nalog.ru/disqualified.do', third),
                    ('http://bankrot.fedresurs.ru/DebtorsSearch.aspx', fourth),
                    ('http://bankrot.fedresurs.ru/DisqualificantsList.aspx', fifth),
                    ('https://service.nalog.ru/uwsfind.do', sixth if sixth else 'ошибка ввода'),
                    ('https://service.nalog.ru/disqualified.do', seventh)
            )
        # print(input('close?: ', ))
        driver.close()
        return name
