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
        table = PrettyTable(headers)
        table.add_rows(sorted(file_reader))
        print(table)


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
    work_number = input('Укажите рабочий номер телефона')
    phone_number = input('Укажите личный номер телефона: ')
    with open('database.csv', 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file, delimiter=';', lineterminator='\r')
        file_writer.writerow([surname, name, patronymic, organisation, work_number, phone_number])
    print('\nКонтакт успешно добавлен')
    print('1. Вернуться в главное меню\n2. Добавить контакт')
    move = move_menu(['1', '2'])
    if move == '1':
        main_menu()
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


def move_menu(buttons: tuple):
    '''
    Функция для получения и проверки вводных данных от пользователя
    :return: str
    '''
    move = input('\nУкажите номер раздела в который хотите перейти: ')
    while move not in buttons:
        print('Указанный раздел отсутствует, попробуйте еще раз')
        move = input('\nУкажите номер раздела в который хотите перейти: ')
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
