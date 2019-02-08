from key import Key
from ul import Ul
from fl import Fl
import datetime
from docx import Document


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
dict_div = {}


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
    while var is False:
        key = input('Введите ключ: ', )
        try:
            int(key)
            return key
        except ValueError:
            if not key:
                return False
            print('Неверные данные.')
            var = False


def loop_keys():
    keys = {}
    for i in range(4):
        u_input = user_input()
        if u_input:
            key = Key(u_input)
            key.determine_type_of_key()
            name = key.name
            key_str = key.key
            keys[name] = key_str
    return keys
# end data acquisition
# loop_keys() - словарь с данными от пользователя


print('Вводите ключи по одному.')
keys = loop_keys()

innul = keys.get('innul')
ogrn = keys.get('ogrn')
innfl = keys.get('innfl')
ogrnip = keys.get('ogrnip')

tu_ul = (innul, ogrn)
tu_fl = (innfl, ogrnip)

today = datetime.date.today().strftime('%d.%m.%y')

document = Document()

if tu_fl != (None, None) and tu_ul != (None, None):
    print('Check Fl')
    fl = Fl(tu_fl)
    name = fl.services()
    print(fl.info)

    print('Check Ul')
    ul = Ul(tu_ul)
    ul.services()
    print(ul.info)

    document.add_heading('ИНН: {}'.format(fl.innfl), level=1)
    document.add_heading('ОГРНИП: {}'.format(fl.ogrnip), level=1)
    document.add_heading('{}'.format(name), level=2)
    add_infotable(fl.info)
    document.add_heading('ИНН: {}'.format(ul.innul), level=1)
    document.add_heading('ОГРН: {}'.format(ul.ogrn), level=1)
    add_infotable(ul.info)

    filename = '{} - {}, {}.docx'.format(today, fl.innfl, ul.innul)

elif tu_fl != (None, None):
    print('Check only Fl')
    fl = Fl(tu_fl)
    name = fl.services()
    print(fl.info)

    document.add_heading('ИНН: {}'.format(fl.innfl), level=1)
    document.add_heading('ОГРНИП: {}'.format(fl.ogrnip), level=1)
    document.add_heading('{}'.format(name), level=2)

    add_infotable(fl.info)

    filename = '{} - {}.docx'.format(today, fl.innfl)

elif tu_ul != (None, None):
    print('Check only Ul')
    ul = Ul(tu_ul)
    ul.services()
    print(ul.info)

    document.add_heading('ИНН: {}'.format(ul.innul), level=1)
    document.add_heading('ОГРН: {}'.format(ul.ogrn), level=1)
    add_infotable(ul.info)

    filename = '{} - {}.docx'.format(today, ul.innul)

else:
    print('Nothing to check.')



# дорабатываю
# for k, v in dict_div.items():
#     soup = bs(v, 'lxml')
#     head = k
#
#     document.add_heading(head, level=2)
#     try:
#         soup_table = soup.find('table', class_='search-result')
#         print('soup_table is ok!')
#     except Exception as e:
#         print('soup_table is not ok!' + e)
#
#     if soup_table:
#         soup_rows = soup_table.find_all('tr')
#         soup_cols = soup_table.find_all('tr')[1].find_all('td')
#         len_rows = len(soup_rows)
#         len_cols = len(soup_cols)
#
#         doc_table = document.add_table(rows=len_rows, cols=len_cols, style='Table Grid')
#
#         for idx, soup_row in enumerate(soup_rows):
#             soup_cols = soup_row.find_all('td') or soup_row.find_all('th')
#
#             doc_cells = doc_table.rows[idx].cells
#             for i, soup_col in enumerate(soup_cols):
#                 doc_cells[i].text = soup_col.text
#     else:
#         print('ой, тут не таблица')
#     document.add_paragraph()

document.add_page_break()
document.save(filename)
print('сохраняем документ')
