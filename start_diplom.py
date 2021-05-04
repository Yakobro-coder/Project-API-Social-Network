import vk_download
import instagram
import odnoklass


print('Приветствую. Это программа "Photo BackUp", для резервного копирования фотографий из Соц.Сетей.\n'
      'Выберите из какой Соц.Сети вы хотите сохранить фотографии.\n'
      'ВКонтакте - 1\n'
      'Одноклассники - 2\n'
      'Инстаграм - 3')
social_networks = int(input('Введите цифру нужного варианта: '))

print('\nВ какое облачное хранилище вы хотите выгрузить фотографии?\n'
      '1 - Yandex Disk\n'
      '2 - Google Drive')
what_drive = int(input('Укажите ответ цифрой: '))


def vk(what_drive):
    print()
    print('Для выгрузки фотографий из ВКонтакте необходимо указать следующие данные:')
    if what_drive == 1:
        token_yandex = input('Введите TOKEN Яндекс диска, для последующей загрузки на него фотографий: ')
        print()
    elif what_drive == 2:
        token_yandex = 0
        print("""Для работы с Google Drive, необходимо получить json файл от OAuth 2.0 Client IDs(от вашего Desktop client)
    с включённым в проекте API G-Drive. Поместите его в корень папки программы. ВАЖНО!!! 
    Измените название вашего .json файла  на 'client_secret'.Это необходимо для работы программы.""")
    else:
        print('Вы указали не корректный вариант.')
        exit()

    access_token = input('Вставьте сюда ваш VK Token: ')

    user_id = input('Введите id(цифры) или короткое имя пользователя VK: ')
    print()

    album_id = int(input('Есть два варианта выгрузки фотографий, укажите цифру\n'
                         '1 - Если хотите выгрузить фотографии со стены\n'
                         '2 - Выгрузить фотографии профиля\n'
                         'Укажите вариант цифрой: '))
    print()

    number_of_photo = int(input('Введите цифрой количество фотографий, которое необходимо выгрузить: '))
    print('Ожидайте...Выгрузка фотографий началась.')
    load_photo = vk_download.Apivk(access_token)
    load_photo.photo_get(token_yandex, user_id, number_of_photo)
    print('Выгрузка завершена.')


def instagram_download(what_drive):
    print()
    print('Для выгрузки фотографий из Instagram необходимо указать следующие данные:')
    if what_drive == 1:
        token_yandex = input('Введите TOKEN Яндекс диска, для последующей загрузки на него фотографий: ')
        print()
    elif what_drive == 2:
        token_yandex = 0
        print("""Для работы с Google Drive, необходимо получить json файл от OAuth 2.0 Client IDs(от вашего Desktop client)
    с включённым в проекте API G-Drive. Поместите его в корень папки программы. ВАЖНО!!! 
    Измените название вашего .json файла  на 'client_secret'.Это необходимо для работы программы.""")
    else:
        print('Вы указали не корректный вариант.')
        exit()

    access_token = input('Вставьте сюда ваш Instagram "Access token": ')
    print()

    number_of_photo = int(input('Введите цифрой количество фотографий, которое необходимо выгрузить: '))
    print('Ожидайте...Выгрузка фотографий началась.')
    send = instagram.Instagram(access_token, token_yandex, number_of_photo)
    print('Выгрузка завершена.')


def ok_download(what_drive):
    print()
    print('Для выгрузки фотографий из Одноклассников необходимо указать следующие данные:')
    if what_drive == 1:
        token_yandex = input('Введите TOKEN Яндекс диска, для последующей загрузки на него фотографий: ')
        print()
    elif what_drive == 2:
        token_yandex = 0
        print("""Для работы с Google Drive, необходимо получить json файл от OAuth 2.0 Client IDs(от вашего Desktop client)
    с включённым в проекте API G-Drive. Поместите его в корень папки программы. ВАЖНО!!! 
    Измените название вашего .json файла  на 'client_secret'.Это необходимо для работы программы.""")
    else:
        print('Вы указали не корректный вариант.')
        exit()

    print('Необходимо авторизоваться в ОДНОКЛАССНИКАХ.')
    log_ok = input('Введите логин: ')
    pass_ok = input('Введите пароль: ')
    print()

    number_of_photo = int(input('Введите цифрой количество фотографий, которое необходимо выгрузить: '))
    print('Ожидайте...Выгрузка фотографий началась.')
    send = odnoklass.Odnoklassniki(log_ok, pass_ok, token_yandex, number_of_photo)
    print('Выгрузка завершена.')


if social_networks == 1:
    vk(what_drive)
elif social_networks == 2:
    ok_download(what_drive)
elif social_networks == 3:
    instagram_download(what_drive)