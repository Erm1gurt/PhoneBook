import csv
import math

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
        self.search_contacts = []
        self.all_pages = 0
        self.search_all_pages = 0
        self.page_menu = [f'{key}. {value}' for key, value in self.page_actions.items()]

    def reader(self) -> None:
        """
        Функция считывает файл базы данных, сохраняет заголовок и список контактов
        """
        with open('database.csv', 'r', encoding='utf-8') as file:
            self.headers = file.readline().strip().split(';')
            self.contacts = sorted(csv.reader(file, delimiter=';'))

    def writer(self, info: list | tuple = None, flag: bool = False) -> None:
        """
        Функция записывает информацию внесенную пользователем в БД
        :param info: Cписок данных для записи
        :param flag: Флаг, указывающий, что будут внесены изменения в БД
        """
        if not flag:
            with open('database.csv', 'a', encoding='utf-8') as file:
                file_writer = csv.writer(file, delimiter=';', lineterminator='\r')
                file_writer.writerow(info)
        elif flag:
            with open('database.csv', 'w', encoding='utf-8') as file:
                file_writer = csv.writer(file, delimiter=';', lineterminator='\r')
                file_writer.writerow(self.headers)
                file_writer.writerows(self.contacts)

    @staticmethod
    def move_menu(buttons: tuple | list, flag: str = 'menu') -> str:
        """
        Функция, реализующая получение информации от пользователя о перемещении по меню, страницам справочника
        или о выборе контакта для изменения
        :param buttons: Кортеж или список состоящий из "кнопок" меню, номеров страниц справочника или контакта
        :param flag: Флаг, определяющий с чем работает функция, с "кнопками" меню, номерами контактов или
        страницами справочника
        :return: Строку, с желаемым действием пользователя
        """
        if flag == 'menu':
            enter_massage = f'\nУкажите номер раздела в который хотите перейти: '
            error_massage = f'Указанный раздел отсутствует, попробуйте еще раз'
        elif flag == 'page':
            enter_massage = f'Укажите номер страницы: '
            error_massage = f'Такой страницы не существует, попробуйте еще раз'
        elif flag == 'contact':
            enter_massage = f'Укажите номер контакта: '
            error_massage = f'Такого контакта не существует, попробуйте еще раз'
        move = input(enter_massage)
        while move not in buttons:
            print(error_massage)
            move = input(enter_massage)
        return move

    def main_menu(self) -> None:
        """
        Функция реализующая главное меню справочника, с помощью нее пользователь выбирает, какой функцией он хочет
        воспользоваться
        """
        func = {'1': PhoneBook.views_contact,
                '2': PhoneBook.add_contact,
                '3': PhoneBook.edit_contact,
                '4': PhoneBook.search_contact}
        print('\nЭлектронный справочник\n\tГлавное меню')
        print('1. Список контактов\n2. Добавить контакт\n3. Изменить контакт\n4. Найти контакт')
        move = PhoneBook.move_menu(tuple(func))

        func[move](self)

    def views_contact(self) -> None:
        """
        Функция, реализующая меню постраничного вывода записей из справочника на экран
        """
        self.all_pages = math.ceil(len(self.contacts) / 10)
        print('\nСписок контактов')
        PhoneBook.view_table(self, page_number=1)

    def add_contact(self) -> None:
        """
        Функция, реализующая добавление контактов в справочник пользователем
        """
        print('\nДобавить контакт')
        info = PhoneBook.filling_information()
        if PhoneBook.contact_match(self, info):
            print('\nТакой контакт уже существует\n')
        else:
            PhoneBook.writer(self, info)
            self.contacts.append(info)
            self.contacts.sort()
            print('\nКонтакт успешно добавлен')
        print('1. Вернуться в главное меню\n2. Добавить контакт')
        move = PhoneBook.move_menu(['1', '2'])
        if move == '1':
            PhoneBook.main_menu(self)
        else:
            PhoneBook.add_contact(self)

    def edit_contact(self) -> None:
        """
        Функция реализующая меню изменения контакта
        :return: None
        """
        print('\nИзменить контакт')
        print('Для изменения, найдите необходимый контакт')
        data = PhoneBook.search_engine(self)
        if data:
            print('\nУкажите номер контакта, который нужно изменить: ')
            num_list = []
            for n, contact in enumerate(data, 1):
                num_list.append(str(n))
                print(f'{n}: {" | ".join(contact)}')
            move = int(PhoneBook.move_menu(num_list, flag='contact'))
            contact = data[move - 1]
            print('Укажите данные которые нужно изменить, если поле менять не нужно, оставьте его пустым:')
            info = PhoneBook.filling_information(data=contact)
            if PhoneBook.contact_match(self, info):
                print('\nТакой контакт уже существует\n')
            else:
                self.contacts.remove(contact)
                self.contacts.append(info)
                self.contacts.sort()
                PhoneBook.writer(self, flag=True)
                print('Контакт успешно изменен')
            print('1. Вернуться в главное меню\n2. Изменить контакт')
            move = PhoneBook.move_menu(['1', '2'])
            if move == '1':
                PhoneBook.main_menu(self)
            else:
                PhoneBook.edit_contact(self)
        else:
            print('\nКонтакт с такми данными не найден, попробуйте еще раз')
            PhoneBook.edit_contact(self)

    def search_contact(self) -> None:
        """
        Функция, реализующая меню поиска контактов.
        Полученный результат выводится на экран с помощью представления таблицы
        """
        print('\nНайти контакт')
        self.search_contacts = PhoneBook.search_engine(self)
        self.search_all_pages = math.ceil(len(self.search_contacts) / 10)
        PhoneBook.view_table(self, page_number=1, flag=False)

    def view_table(self, page_number: int, flag: bool = True) -> None:
        """
        Функция, выводящая таблицы с данными контактов
        :param page_number: Номер страницы, которую нужно вывести на экран
        :param flag: Флаг, указывающий на то, будет ли выводиться вся таблица или только данные из поиска
        """
        start = (page_number - 1) * 10
        end = page_number * 10
        all_pages = self.all_pages if flag else self.search_all_pages
        contacts = self.contacts[start:end] if flag else self.search_contacts[start:end]
        table = PrettyTable(self.headers)
        table.clear_rows()
        table.add_rows(contacts)

        print(f'Страница {min(page_number, all_pages)} из {all_pages}: ')
        print(table)

        if all_pages < 2:
            page_menu_list = self.page_menu[-1:]
            page_num_list = tuple(self.page_actions)[-1:]
        elif page_number == 1:
            page_menu_list = self.page_menu[2:]
            page_num_list = tuple(self.page_actions)[2:]
        elif page_number == all_pages:
            page_menu_list = [elem for elem in self.page_menu if
                              'Последняя страница' not in elem and 'Следующая страница' not in elem]
            page_num_list = tuple(elem for elem in self.page_actions
                                  if 'Последняя страница' not in self.page_actions[elem]
                                  and 'Следующая страница' not in self.page_actions[elem])
        else:
            page_menu_list = self.page_menu
            page_num_list = tuple(self.page_actions)

        page_menu_list_str = ' | '.join(page_menu_list)

        print(page_menu_list_str)
        move = PhoneBook.move_menu(page_num_list, flag='page')
        if move != '4':
            PhoneBook.jump_page(self, move, page_number, flag=flag)
        else:
            PhoneBook.main_menu(self)

    def jump_page(self, move: str, previous_page: int, flag: bool = True) -> None:
        """
        Функция, осуществляющая переход по страницам справочника
        :param move: Действие, которое хочет совершить пользователь
        :param previous_page: Номер предыдущей страницы справочника
        :param flag: Флаг, указывающий на то, полная это таблица или поисковая
        """
        if move == '-1':
            PhoneBook.view_table(self, previous_page - 1)
        if move == '0':
            PhoneBook.view_table(self, page_number=1)
        elif move == '1':
            PhoneBook.view_table(self, page_number=previous_page + 1)
        elif move == '2':
            page_list = tuple(map(str, range(1, self.all_pages + 1)))
            page_number = int(PhoneBook.move_menu(page_list, flag='page'))
            PhoneBook.view_table(self, page_number=page_number)
        elif move == '3':
            all_pages = self.all_pages if flag else self.search_all_pages
            PhoneBook.view_table(self, all_pages)

    def contact_match(self, new_contact: list) -> bool:
        """
        Функция, проверяющая на совпадение нового контакта с уже существующими
        :param new_contact: Список с данными о новом контакте
        :return: Булевое значение, указывающие на наличие или отсутствие совпадений
        """
        return new_contact in self.contacts

    @staticmethod
    def filling_information(data: list = None) -> list:
        """
        Функция запрашивает данные о контакте у пользователя
        :param data: Необязательный аргумент, передается если фунция вызвается для изменения контакта, принимает
        старую информацию о контакте
        :return: Список данных введеных пользователем о контакте
        """
        surname, name, patronymic, organisation, work_number, phone_number = data or [None] * 6

        surname = PhoneBook.setter('Укажите фамилию: ', surname).capitalize()
        name = PhoneBook.setter('Укажите имя: ', name).capitalize()
        patronymic = PhoneBook.setter('Укажите отчество: ', patronymic).capitalize()
        organisation = PhoneBook.setter('Укажите организацию: ', organisation, flag='org')
        work_number = PhoneBook.setter('Укажите рабочий номер телефона: ', work_number, flag='num')
        phone_number = PhoneBook.setter('Укажите личный номер телефона: ', phone_number, flag='num')

        return [surname, name, patronymic, organisation, work_number, phone_number]

    @staticmethod
    def setter(info: str, field: str, flag: str = 'fio') -> str:
        """
        Функция осуществляющая уcтановку значения полю
        :param info: Строка, которая будет выведена у пользователя на экран при запросе ввода
        :param field: Старая информация о поле в справочнике, передается в случае изменения информации о контакте,
        иначе передается None
        :param flag: Флаг, указывающий на тип поля, с которым осуществляется взаимодействие
        :return: Возвращает строку для поля справочника
        """
        setter_move = {'fio': [' может содержать только буквы и', str.isalpha],
                       'num': [' может содержать только цифры и', str.isdigit],
                       'org': ['', bool]}
        if field is None:
            field_data = input(info)
            while not setter_move[flag][1](field_data):
                print(f'Данное поле{setter_move[flag][0]} не может быть пустым, введите корректные данные')
                field_data = input(info)
        else:
            field_data = input(info) or field
            while field_data and not setter_move[flag][1](field_data):
                print(f'Данное поле{setter_move[flag][0]}, введите корректные данные')
                field_data = input(info) or field
        return field_data

    def search_engine(self) -> list[list]:
        """
        Поисковая функция, запрашивает у пользователя данные для поиска. Поиск осуществялется на основании частичных
        совпадений, если пользователь внес несколько параметров для поиска, то все должны частично совпадать с любым
        из имеющихся параметров в таблице (аналогичное явление в поиске можно наблюдать в телефонной книге iPhone)
        :return: Возвращает список совпадений
        """
        print('Поиск может осуществляться по нескольким параметрам, в этом случае указывайте их через пробел')
        search_query = input('Введите данные для поиска: ').split()
        result = []
        for line in self.contacts:
            line_string = ' '.join(line).lower()
            counter = len(search_query)
            for query in search_query:
                if query.lower() in line_string:
                    counter -= 1
            if not counter:
                result.append(line)
        return result


if __name__ == '__main__':
    obj = PhoneBook()
    obj.reader()
    PhoneBook.main_menu(obj)
