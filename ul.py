from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import time


class Ul(object):
    """docstring for Ul."""
    def __init__(self, object, name=None, address=None, info=None):
        self.innul = object[0]
        self.ogrn = object[1]
        self.name = name
        self.address = address
        self.info = info

    # доработать
    # def check_using_service(self):
    #     # service_url = 'https://egrul.nalog.ru'
    #     service_url = 'file:///Users/Ksihris/projects/pro/service_pro/ser.html'
    #     driver = webdriver.Chrome()
    #
    #     driver.get(service_url)
    #     username = self.input_key(driver, "ogrninnul", self.innul)
    #     self.cap_loop(username, driver, 'captcha')
    #
    #     driver.get('file:///Users/Ksihris/projects/pro/service_pro/ser_ur.html')
    #     text = driver.find_element_by_id('resultContent').find_elements_by_tag_name('td')
    #
    #     if self.ogrn is None:
    #         print('огрн нет')
    #         self.ogrn = text[2].text
    #     else:
    #         print('огрн есть')
    #
    #     self.name = text[0].text
    #     self.address = text[1].text
    #
    #     user_input = input('Close?: ',)
    #     driver.close()


    def cap(self, driver):
        captcha = driver.find_element_by_id('captcha')
        f = [x for x in input('введите капчу: ')]
        for i in f:
            time.sleep(.05)
            captcha.send_keys(i)
        return True

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
            time.sleep(5)
            return True
        except NoSuchElementException:
            driver.find_element_by_class_name(id_name).click()
            time.sleep(5)
            return True

    def input_key(self, driver, form_id, key):
        username = driver.find_element_by_id(form_id)
        for i in key:
            time.sleep(.05)
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
            rows = driver.find_elements_by_id(id)
            text = [row.text for row in rows]

    def cap_loop(self, username, driver, id, btn_id=None):
        er = True
        while er:
            self.cap(driver)
            if btn_id:
                self.button(driver, btn_id)
            else:
                username.submit()
            try:
                er = driver.find_element_by_id(id).text
                print(er)
            except NoSuchElementException:
                er = False
        print('Цифры с картинки введены верно')



    def services(self):

        key = [x for x in self.innul]
        ogrn = [x for x in self.ogrn]
        # driver = webdriver.Firefox(executable_path='C:\\Python\geckodriver.exe')
        driver = webdriver.Chrome()

        driver.get('https://fedresurs.ru')
        username = driver.find_element_by_css_selector("input[name='searchString']")
        for i in key:
            time.sleep(.05)
            username.send_keys(i)
        driver.find_element_by_class_name("btn").click()
        fedresurs = self.get_text(driver, 'search-result')
        # ctl00_MainContent_upnCompanyList
# ctl00_MainContent_tdContent

        driver.get('https://service.nalog.ru/uwsfind.do')
        username = self.input_key(driver, 'ogrnUl', ogrn)
        self.cap_loop(username, driver, 'captcha', 'btnSearch')
        second = self.get_text(driver, 'pnlResults')

        driver.get('https://service.nalog.ru/disqualified.do')
        username = self.input_key(driver, 'orgInn', key)
        self.cap_loop(username, driver, 'captcha', 'float-right')
        third = self.get_text(driver, 'resultPanel')

        driver.get('http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html')
        username = self.input_key(driver, 'searchString', key)
        username.submit()
        time.sleep(3)
        try:
            fourth = driver.find_element_by_css_selector('table.searchDocTable').text
        except NoSuchElementException:
            fourth = 'Ничего не найдено.'

        driver.get('https://service.nalog.ru/svl.do')
        username = self.input_key(driver, 'svlform_inn', key)
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/form/div[2]/button").click()
        fifth = driver.find_element_by_class_name('container').text

        driver.get('http://bankrot.fedresurs.ru/DebtorsSearch.aspx')
        username = self.input_key(driver, 'ctl00_cphBody_OrganizationCode1_CodeTextBox', key)
        self.button(driver, 'ctl00_cphBody_btnSearch')
        sixth = self.get_text(driver, 'ctl00_cphBody_upList')

        driver.get('https://service.nalog.ru/zd.do')
        username = self.input_key(driver, 'inn', key)
        captcha = driver.find_element_by_id('captcha')
        self.cap_loop(username, driver, 'captcha', 'btn_send')
        seventh = self.get_text(driver, 'pnlResults')

        driver.get('https://service.nalog.ru/bi.do')
        self.radio_click(driver, 'unirad_0')
        username = self.input_key(driver, 'innPRS', key)
        self.bik(driver, 'bikPRS')
        self.cap_loop(username, driver, 'captcha', 'btnSearch')
        eighth = self.get_text(driver, 'pnlResultData')

        self.info = (
                ('https://fedresurs.ru', fedresurs),
                ('https://service.nalog.ru/uwsfind.do', second),
                ('https://service.nalog.ru/disqualified.do', third),
                ('http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html', fourth),
                ('https://service.nalog.ru/svl.do', fifth),
                ('http://bankrot.fedresurs.ru/DebtorsSearch.aspx', sixth),
                ('https://service.nalog.ru/zd.do', seventh),
                ('https://service.nalog.ru/bi.do', eighth)
                )
        # print(input('close?: ', ))
        driver.close()
