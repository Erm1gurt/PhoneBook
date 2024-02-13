import csv
from prettytable import PrettyTable


class PhoneBook:
    def __init__(self):
        self.page_actions = {'-1': 'Предыдущая страница',
                             '0': 'Первая страница',
                             '1': 'Следующая страница',
                             '2': 'Перейти на указанную страницу',
                             '3': 'Последняя страница',
                             '4': 'Главное меню'}
        self.headers = []
        self.contacts = []
        self.all_pages = 0
        self.page_menu = [f'{key}. {value}' for key, value in self.page_actions.items()]

    def reader(self):
        with open('database.csv', 'r', encoding='utf-8') as file:
            self.headers = file.readline().strip().split(';')
            self.contacts = sorted(csv.reader(file, delimiter=';'))

    @staticmethod
    def writer(info):
        with open('database.csv', 'a', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=';', lineterminator='\r')
            file_writer.writerow(info)

    def views_contact(self):
        PhoneBook.reader(self)
        self.all_pages = len(self.contacts) // 10 + bool(len(self.contacts) % 10)
        print('\nСписок контактов')
        PhoneBook.view_table(self, page_number=1)

    def view_table(self, page_number):
        start = (page_number != 1) * (page_number - 1) * 10
        end = 10 * page_number
        table = PrettyTable(self.headers)
        table.clear_rows()
        table.add_rows(self.contacts[start:end])

        print(f'Страница {page_number} из {self.all_pages}: ')
        print(table)

        if page_number == 1:
            page_menu_list = ' | '.join(self.page_menu[2:])
            page_num_list = tuple(self.page_actions)[2:]
        elif page_number == self.all_pages:
            page_menu_list = ' | '.join(elem for elem in self.page_menu if 'Последняя страница' not in elem)
            page_num_list = tuple(elem for elem in self.page_actions
                                  if 'Последняя страница' not in self.page_actions[elem])
        else:
            page_menu_list = ' | '.join(self.page_menu)
            page_num_list = tuple(self.page_actions)

        print(page_menu_list)
        move = PhoneBook.move_menu(page_num_list)
        if move != '4':
            PhoneBook.jump_page(self, move, page_number)
        else:
            PhoneBook.main_menu(self)

    def jump_page(self, move, previous_page):
        if move == '-1':
            PhoneBook.view_table(self, previous_page - 1)
        if move == '0':
            PhoneBook.view_table(self, page_number=1)
        elif move == '1':
            PhoneBook.view_table(self, page_number=previous_page + 1)
        elif move == '2':
            page_list = tuple(map(str, range(1, self.all_pages + 1)))
            page_number = int(PhoneBook.move_menu(page_list, menu=False))
            PhoneBook.view_table(self, page_number=page_number)
        elif move == '3':
            PhoneBook.view_table(self, self.all_pages)

    @staticmethod
    def move_menu(buttons: tuple, menu: bool = True) -> str:
        '''
        Функция реализующая получение информации от пользователя, о перемещении по меню или страницам справочника
        :param buttons: кортеж состоящий из "кнопок" меню или номеров страниц справочника
        :param menu: флаг, определяющий с чем работает функция, с "кнопками" меню или номерами страниц справочника
        :return: str
        '''
        enter_massage = f'\nУкажите номер раздела в который хотите перейти: ' if menu else f'Укажите номер страницы: '
        error_massage = f'Указанный раздел отсутствует, попробуйте еще раз' if menu \
            else f'Такой страницы не существует, попробуйте еще раз'
        move = input(enter_massage)
        while move not in buttons:
            print(error_massage)
            move = input(enter_massage)
        return move

    @staticmethod
    def filling_information():
        surname = input('Укажите фамилию: ').capitalize()
        name = input('Укажите имя: ').capitalize()
        patronymic = input('Укажите отчество: ').capitalize()
        organisation = input('Укажите ораганизацию: ')
        work_number = input('Укажите рабочий номер телефона: ')
        phone_number = input('Укажите личный номер телефона: ')

        return surname, name, patronymic, organisation, work_number, phone_number

    def add_contact(self) -> None:
        '''
        Функция реализующая добавление контактов в справочник пользователем
        '''
        print('\nДобавить контакт')
        info = PhoneBook.filling_information()
        PhoneBook.writer(info)
        print('\nКонтакт успешно добавлен')
        print('1. Вернуться в главное меню\n2. Добавить контакт')
        move = PhoneBook.move_menu(['1', '2'])
        if move == '1':
            PhoneBook.main_menu(self)
        else:
            PhoneBook.add_contact(self)

    def edit_contact(self):
        '''
        Функция изменяющая контакты
        :return: None
        '''
        print('\nИзменить контакт')

    def search_contact(self):
        '''
        Функция для поиска контактов
        :return: None
        '''
        PhoneBook.reader(self)
        print('\nНайти контакт')
        PhoneBook.search_engine(self)

    def search_engine(self):
        print('Поиск может осуществляться по нескольким параметрам, в таком случае указывайте их через пробел')
        search_query = input('Введите данные для поиска: ').split()
        for line in self.contacts:
            line = ' '.join(line)
            for query in search_query:
                if query in line:
                    print(line)
                    break


    def main_menu(self) -> None:
        '''
        Функция реализующая главное меню справочника, с помощью нее пользователь выбирает, какой функцией он хочет
        воспользоваться
        '''
        func = {'1': PhoneBook.views_contact,
                '2': PhoneBook.add_contact,
                '3': PhoneBook.edit_contact,
                '4': PhoneBook.search_contact}
        print('\nЭлектронный справочник\n\tГлавное меню')
        print('1. Список контактов\n2. Добавить контакт\n3. Изменить контакт\n4. Найти контакт')
        move = PhoneBook.move_menu(tuple(func))

        func[move](self)


if __name__ == '__main__':
    obj = PhoneBook()
    PhoneBook.main_menu(obj)
