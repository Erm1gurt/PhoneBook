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


def main_menu():
    '''
    Функция реализующая главное меню
    :return: None
    '''
    func = {'1': views_contact, '2': add_contact, '3': edit_contact, '4': search_contact}
    print('Электронный справочник\n\tГлавное меню')
    print('1. Список контактов\n2. Добавить контакт\n3. Изменить контакт\n4. Найти контакт')
    move_menu = input('\nУкажите номер раздела в который хотите перейти: ')
    if move_menu not in list(func):
        raise ValueError('Выбранный пункт меню отсутствует')
    func[move_menu]()

if __name__ == '__main__':
    main_menu()