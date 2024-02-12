import csv
from prettytable import PrettyTable


def views_contact():
    '''
    Функция выводящая контакты
    :return: None
    '''
    print('\nСписок контактов')
    with open('database.csv', 'r', encoding='utf-8') as file:
        headers = file.readline().strip().split(';')
        file_reader = csv.reader(file, delimiter=';')
        contacts = sorted(file_reader)
    print(len(contacts))
    table = PrettyTable(headers)
    all_pages = len(contacts) // 10 + bool(len(contacts) % 10)

    def view_table(page_number: int = 1) -> None:
        start = (page_number != 1) * (page_number - 1) * 10
        end = 10 * page_number
        table.clear_rows()
        print(start, end)
        table.add_rows(contacts[start:end])
        print(f'Страница {page_number} из {all_pages}')
        print(table)
        page_menu_dict = {'-1': ['Предыдущая страница', jump_page],
                          '0': ['Первая страница', jump_page],
                          '1': ['Следующая страница', jump_page],
                          '2': ['Перейти на указанную страницу', jump_page],
                          '3': ['Последняя страница', jump_page],
                          '4': ['Главное меню', main_menu]}
        page_menu = [f'{key}. {value[0]}' for key, value in page_menu_dict.items()]
        if page_number == 1:
            page_menu_list = ' | '.join(list(page_menu[2:]))
            page_num_list = tuple(page_menu_dict)[2:]
        else:
            page_menu_list = ' | '.join(list(page_menu))
            page_num_list = tuple(page_menu_dict)
        print(page_menu_list)
        move = move_menu(page_num_list)
        if move != '4':
            page_menu_dict[move][1](move, page_number)
        else:
            main_menu()

    def jump_page(move, previous_page):
        if move == '-1':
            view_table(previous_page - 1)
        if move == '0':
            view_table(1)
        elif move == '1':
            view_table(previous_page + 1)
        elif move == '2':
            page_list = tuple(map(str, range(1, all_pages + 1)))
            page_number = int(move_menu(page_list, menu=False))
            view_table(page_number)
        elif move == '3':
            view_table(all_pages)

    view_table()


def add_contact():
    '''
    Функция добавляющая контакты
    :return: None
    '''
    print('\nДобавить контакт')
    surname = input('Укажите фамилию: ')
    name = input('Укажите имя: ')
    patronymic = input('Укажите отчество: ')
    organisation = input('Укажите ораганизацию: ')
    work_number = input('Укажите рабочий номер телефона: ')
    phone_number = input('Укажите личный номер телефона: ')
    with open('database.csv', 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=';', lineterminator='\r')
        file_writer.writerow([surname, name, patronymic, organisation, work_number, phone_number])
    print('\nКонтакт успешно добавлен')
    print('1. Вернуться в главное меню\n2. Добавить контакт')
    move = move_menu(['1', '2'])
    if move == '1':
        main_menu()
    else:
        add_contact()


def edit_contact():
    '''
    Функция изменяющая контакты
    :return: None
    '''
    print('\nИзменить контакт')


def search_contact():
    '''
    Функция для поиска контактов
    :return: None
    '''
    print('\nНайти контакт')


def move_menu(buttons: tuple, menu=True):
    '''
    Функция для получения и проверки вводных данных от пользователя
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


def main_menu():
    '''
    Функция реализующая главное меню
    :return: None
    '''
    func = {'1': views_contact, '2': add_contact, '3': edit_contact, '4': search_contact}
    print('\nЭлектронный справочник\n\tГлавное меню')
    print('1. Список контактов\n2. Добавить контакт\n3. Изменить контакт\n4. Найти контакт')
    move = move_menu(tuple(func))
    func[move]()


if __name__ == '__main__':
    main_menu()
