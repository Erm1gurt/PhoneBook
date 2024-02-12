def views_contact():
    '''
    Функция выводящая контакты
    :return: None
    '''
    print('Список контактов')


def add_contact():
    '''
    Функция добавляющая контакты
    :return: None
    '''
    print('Добавить контакт')


def edit_contact():
    '''
    Функция изменяющая контакты
    :return: None
    '''
    print('Изменить контакт')


def search_contact():
    '''
    Функция для поиска контактов
    :return: None
    '''
    print('Найти контакт')


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
    print('Электронный справочник\n\tГлавное меню')
    print('1. Список контактов\n2. Добавить контакт\n3. Изменить контакт\n4. Найти контакт')
    move = move_menu(tuple(func))
    func[move]()


if __name__ == '__main__':
    main_menu()
