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

    def reader(self) -> None:
        """
        Функция считывает файл базы данных, сохраняет заголовок и список контактов
        """
        with open('database.csv', 'r', encoding='utf-8') as file:
            self.headers = file.readline().strip().split(';')
            self.contacts = sorted(csv.reader(file, delimiter=';'))

    def writer(self, info: list | tuple = None, flag: bool = False) -> None:
        """
        Функция записывает информацию внесенную пользовател в БД
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
                file_writer.writerow(self.contacts)

    def views_contact(self) -> None:
        """
        Функция реализующая меню постраничного вывода записей из справочника на экран
        """
        PhoneBook.reader(self)
        self.all_pages = len(self.contacts) // 10 + bool(len(self.contacts) % 10)
        print('\nСписок контактов')
        PhoneBook.view_table(self, page_number=1)

    def view_table(self, page_number: int) -> None:
        """
        Функция выводящая таблицы с данными
        :param page_number: Номер страницы, которую нужно вывести на экран
        """
        start = (page_number != 1) * (page_number - 1) * 10
        end = 10 * page_number
        table = PrettyTable(self.headers)
        table.clear_rows()
        table.add_rows(self.contacts[start:end])

        print(f'Страница {page_number} из {self.all_pages}: ')
        print(table)

        if self.all_pages == 1 or self.all_pages == 0:
            page_menu_list = self.page_menu[-1]
            page_num_list = tuple(self.page_actions)[-1]
        elif page_number == 1:
            page_menu_list = ' | '.join(self.page_menu[2:])
            page_num_list = tuple(self.page_actions)[2:]
        elif page_number == self.all_pages:
            page_menu_list = ' | '.join(elem for elem in self.page_menu if 'Последняя страница' not in elem
                                        and 'Следующая страница' not in elem)
            page_num_list = tuple(elem for elem in self.page_actions
                                  if 'Последняя страница' not in self.page_actions[elem]
                                  and 'Следующая страница' not in self.page_actions[elem])
        else:
            page_menu_list = ' | '.join(self.page_menu)
            page_num_list = tuple(self.page_actions)

        print(page_menu_list)
        move = PhoneBook.move_menu(page_num_list, flag='page')
        if move != '4':
            PhoneBook.jump_page(self, move, page_number)
        else:
            PhoneBook.main_menu(self)

    def jump_page(self, move: str, previous_page: int) -> None:
        """
        Функция осуществляющая переход по страницам справочника
        :param move: Действие, которое хочет совершить пользователь
        :param previous_page: Номер предыдущей страницы справочника
        """
        if move == '-1':
            PhoneBook.view_table(self, previous_page - 1)
        if move == '0':
            PhoneBook.view_table(self, page_number=1)
        elif move == '1':
            PhoneBook.view_table(self, page_number=previous_page + 1)
        elif move == '2':
            page_list = tuple(map(str, range(1, self.all_pages + 1)))
            page_number = int(PhoneBook.move_menu(page_list, menu='page'))
            PhoneBook.view_table(self, page_number=page_number)
        elif move == '3':
            PhoneBook.view_table(self, self.all_pages)

    @staticmethod
    def move_menu(buttons: tuple | list, flag: str = 'menu') -> str:
        """
        Функция реализующая получение информации от пользователя, о перемещении по меню или страницам справочника
        :param buttons: кортеж или список состоящий из "кнопок" меню или номеров страниц справочника
        :param flag: флаг, определяющий с чем работает функция, с "кнопками" меню, номерами контактов или
        страниц справочника
        :return: str
        """
        if flag == 'menu':
            enter_massage = f'\nУкажите номер раздела в который хотите перейти: '
            error_massage = f'Указанный раздел отсутствует, попробуйте еще раз'
        elif flag == 'page':
            enter_massage = f'Укажите номер страницы: '
            error_massage = f'Такой страницы не существует, попробуйте еще раз'
        elif flag == 'contact':
            enter_massage = f'Укажите номер контакта: '
            error_massage = f'Такой контакта не существует, попробуйте еще раз'
        move = input(enter_massage)
        while move not in buttons:
            print(error_massage)
            move = input(enter_massage)
        return move

    @staticmethod
    def setter(info: str, field: str | bool, flag: str = 'fio') -> str:
        """
        Функция осуществляющая утановку значения полю
        :param info: Строка, которая будет выведена у пользователя на экран при запросе ввода
        :param field: Старая информация о поле в справочнике, передается в случае изменения информации о контакте,
        иначе передается False
        :return: Возвращает строку для поля справочника
        """
        setter_move = {'fio': [' может содержать только буквы и', str.isalpha],
                       'num': [' может содержать только цифры и', str.isdigit],
                       'org': ['', bool]}
        if not field:
            field_data = input(info).capitalize()
            while not setter_move[flag][1](field_data):
                print(f'Данное поле{setter_move[flag][0]} не может быть пустым, введите корректные данные')
                field_data = input(info).capitalize()
        else:
            field_data = input(info).capitalize() or field
            while field_data and not setter_move[flag][1](field_data):
                print(f'Данное поле{setter_move[flag][0]}, введите корректные данные')
                field_data = input(info).capitalize() or field
        return field_data

    @staticmethod
    def filling_information(data: list = None) -> list:
        """
        Функция запрашивает данные о контакте у пользователя
        :param data: Необязательный аргумент, передается если фунция вызвается для изменения контакта, принимает
        старую информацию о контакте
        :return: Список данных введеных пользователем о контакте
        """
        surname, name, patronymic, organisation, work_number, phone_number = data or [False] * 6
        surname = PhoneBook.setter('Укажите фамилию: ', surname)
        name = PhoneBook.setter('Укажите имя: ', name)
        patronymic = PhoneBook.setter('Укажите отчество: ', patronymic)
        organisation = PhoneBook.setter('Укажите ораганизацию: ', organisation, flag='org')
        work_number = PhoneBook.setter('Укажите рабочий номер телефона: ', work_number, flag='num')
        phone_number = PhoneBook.setter('Укажите личный номер телефона: ', phone_number, flag='num')

        return [surname, name, patronymic, organisation, work_number, phone_number]

    def add_contact(self) -> None:
        """
        Функция реализующая добавление контактов в справочник пользователем
        """
        print('\nДобавить контакт')
        info = PhoneBook.filling_information()
        PhoneBook.writer(self, info)
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
        PhoneBook.reader(self)
        data = PhoneBook.search_engine(self)
        if data:
            print('\nУкажите номер контакта, который нужно изменить: ')
            num_list = []
            for n, elem in enumerate(data, 1):
                num_list.append(str(n))
                print(f'{n}: {" | ".join(elem)}')
            move = int(PhoneBook.move_menu(num_list, flag='contact'))
            contact = data[move-1]
            print('Укажите данные которые нужно изменить, если поле менять не нужно, оставьте его пустым:')
            info = PhoneBook.filling_information(data=contact)
            self.contacts.remove(contact)
            self.contacts.append(info)
            PhoneBook.writer(flag=True)
        else:
            print('\nКонтакт с такми данными не найден, попробуйте еще раз')
            PhoneBook.edit_contact(self)

    def search_contact(self) -> None:
        """
        Функция для поиска контактов. Вызывает поисковую функцию, которая осуществляет поиск и возвращает результат.
        Полученный результат выводится на экран с помощью представления таблицы
        """
        PhoneBook.reader(self)
        print('\nНайти контакт')
        self.contacts = PhoneBook.search_engine(self)
        self.all_pages = len(self.contacts) // 10 + bool(len(self.contacts) % 10)
        PhoneBook.view_table(self, page_number=1)

    def search_engine(self) -> list[list]:
        """
        Поисковая функция, запрашивает у пользователя данные для поиска. Поиск осуществялется на основании частичных
        совпадений, если пользователь внес несколько параметров для поиска, то оба должны частично совпадать с любым
        из имеющихся параметров в таблице (аналогичное явление в поиске можно наблюдать в телефонной книге iPhone)
        :return: Возвращает список совпадений
        """
        print('Поиск может осуществляться по нескольким параметрам, в этом случае указывайте их через пробел')
        search_query = input('Введите данные для поиска: ').split()
        result = []
        for line in self.contacts:
            line_string = ' '.join(line)
            counter = len(search_query)
            for query in search_query:
                if query in line_string:
                    counter -= 1
            if not counter:
                result.append(line)
        return result

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


if __name__ == '__main__':
    obj = PhoneBook()
    PhoneBook.main_menu(obj)
