from service import Service
from chek_obj import CheckObj
import datetime
from docx import Document
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs

services = (
    'https://fedresurs.ru',
    'https://service.nalog.ru/uwsfind.do',
    'https://service.nalog.ru/disqualified.do',
    'http://zakupki.gov.ru/epz/dishonestsupplier/quicksearch/search.html',
    'https://service.nalog.ru/svl.do',
    'http://bankrot.fedresurs.ru/DebtorsSearch.aspx',
    'https://service.nalog.ru/zd.do',
    'https://service.nalog.ru/bi.do',
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


def add_infotable(info):
    table = document.add_table(rows=1, cols=2, style='Table Grid')
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Источник'
    hdr_cells[1].text = 'Результат'

    for k, v in info:
        row_cells = table.add_row().cells
        row_cells[0].text = k
        if v:
            row_cells[1].text = v
        else:
            row_cells[1].text = 'Пусто'


# data acquisition
def user_input():
    var = False
    print('Программа заработала, для выхода нажмите Ctrl + C.')

    while var is False:
        key = input('Введите ключ: ', )
        try:
            int(key)
            checkobj = CheckObj([x for x in key])

            if len(key) is 10 or len(key) is 13:
                print('ul = True')
                return(key, True)
            elif len(key) is 12 or len(key) is 15:
                if checkobj.egrul() is True:
                    print('ul = True')
                    return(key, True)
                else:
                    print('ul = False')
                    return(key, False)
            else:
                print('Неверные данные.')
                var = False
        except ValueError:
            if not key:
                return False
            print('Неверные данные.')
            var = False

# document = Document()


dict_data = []
key, ul = user_input()

checkobj = CheckObj(key)
checkobj.zachestnyibiznes()
service = Service(key, ul)
if ul is False:
    print("Это физик")

    service.fiz(checkobj.boss_name, key)
    dict_data.append(service.dict_service)

else:
    print('Это не физик')

    ogrn = [x for x in checkobj.ogrn]
    list_key = [x for x in key]
    print(checkobj.bosses_inn)
    """
    доработать
    for i in checkobj.bosses_inn:
        print(i)
        checkobj_f_boss = CheckObj(key)
        ul = checkobj_f_boss.egrul()
        service_f_boss = Service(i, ul)

        checkobj_f_boss.zachestnyibiznes()
        i = [x for x in i]
        service_f_boss.fiz(checkobj_f_boss.boss_name, i)
        dict_data.append(service_f_boss.dict_service)
        print(input('продолжить?', ))
    """

    if checkobj.date_result.days < 60:

        print('меньше 60 дней')
        if ul is True:
            service.ur_min(list_key, ogrn)
        else:
            service.ip_min(list_key, ogrn)
    else:
        print('больше 60 дней')
        if ul is True:
            service.ur_min(list_key, ogrn)
            service.ur_max(checkobj.boss_name, list_key)

        else:
            service.ip_min(list_key, ogrn)
            service.ip_max(list_key, checkobj.boss_name)

    dict_data.append(service.dict_service)

#
#
#
#
# str_ogrn = ''.join(ogrn)
#

#
# document.add_heading('{}'.format(company_name), level=1)
# document.add_heading('ИНН: {}'.format(key), level=2)
# document.add_heading('ОГРН: {}'.format(str_ogrn), level=2)
# document.add_heading('{}'.format(boss_name), level=2)
#

# # filename = '{}.docx'.format(today)
#
#
print('начинаем собирать документ')
document = Document()
today = datetime.date.today().strftime('%d.%m.%y')
filename = '{} - {}.docx'.format(key, today)

if ul is False:
    document.add_heading('{}'.format(checkobj.boss_name, level=1))
    document.add_heading('ИНН: {}'.format(checkobj.key), level=2)
    filename = '{} - {}.docx'.format(checkobj.key, today)
else:
    document.add_heading('{}'.format(checkobj.company_name), level=1)
    document.add_heading('ИНН: {}'.format(checkobj.key), level=2)
    document.add_heading('ОГРН: {}'.format(''.join(checkobj.ogrn)), level=2)
    document.add_heading('{}'.format(checkobj.boss_name), level=2)

for data in dict_data:
    index_header = 0
    for k, v in service.dict_service.items():
        soup = bs(v, 'lxml')

        head = headers[index_header]
        index_header += 1

        document.add_heading(head, level=2)
        try:
            # soup_table = soup.find('table', class_='search-result')
            soup_tables = soup.find_all('table')
            print('soup_table is ok!')
        except Exception as e:
            print('soup_table is not ok!' + e)

        if soup_tables:
            for soup_table in soup_tables:
                soup_rows = soup_table.find_all('tr')
                try:
                    soup_cols = soup_table.find_all('tr')[1].find_all('td')
                except IndexError:
                    soup_cols = soup_table.find_all('tr')[0].find_all('td')

                len_rows = len(soup_rows)
                len_cols = len(soup_cols)

                doc_table = document.add_table(rows=len_rows, cols=len_cols, style='Table Grid')

                for idx, soup_row in enumerate(soup_rows):
                    soup_cols = soup_row.find_all('td') or soup_row.find_all('th')
                    # print('idx -', idx, 'cols -', soup_cols, 'rows - ', soup_rows)
                    # print('idx', idx)
                    doc_cells = doc_table.rows[idx].cells
                    # print(doc_cells, type(doc_cells))
                    for i, soup_col in enumerate(soup_cols):
                        # print('i', i)
                        doc_cells[i].text = soup_col.text
        else:
            try:
                nf = soup.find('p').text
            except NoSuchElementException:
                nf = soup.get_text()
            except AttributeError:
                nf = soup.get_text()

            document.add_paragraph(nf)
            # print('ой, тут не таблица')
        document.add_paragraph()

document.add_page_break()
document.save(filename)


print('сохраняем документ')
