import datetime
import requests
from pprint import pprint
import time
import json
from tqdm import tqdm
import Yandexdrive
import Gdrive
import os


class Apivk:
    url = 'https://api.vk.com/method/'

    def __init__(self, access_token):
        now_data_time = datetime.datetime.now()
        now_data_time = now_data_time.strftime("%d-%m-%Y_%H.%M")
        self.now_data = f'Backup_photo_VK_{now_data_time}'
        self.token = access_token
        self.params = {
            'access_token': self.token,
            'v': '5.130'
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def photo_get(self, token_yandex, user_id=None, count=5, album_id=2):
        self.token_yandex = token_yandex
        if user_id == None:
            user_id = self.owner_id
        else:
            params = {'user_ids': user_id}
            user_id = requests.get(self.url + 'users.get', params={**self.params, **params}).json()['response'][0]['id']

        if album_id == 1:
            album_id = 'wall'
        elif album_id == 2:
            album_id = 'profile'

        params = {
            'owner_id': user_id,
            'album_id': album_id,
            'extended': '1',
            'count': count,
            'photo_sizes': 0,
            'rev': '1'
        }
        list_photos = requests.get(self.url + 'photos.get', params={**self.params, **params})
        if 'error' in list_photos.json():
            print('Нет доступа к фото.', '"error_msg":', list_photos.json()['error']['error_msg'])
            exit()

        # Create folder
        # Если Яндекс токен не указан(token == 0) то работаем с Gdrive
        # Если токен указан(token != 0) работаем с YaDisk
        if self.token_yandex == 0:
            send = Gdrive.GoogleDrive(1)
        else:
            # create class in file Yandexdrive.py (при __init__ создается папка)
            send = Yandexdrive.YandexDrive(self.token_yandex, 1)


        like_name = []
        self.list_name_photos = []
        self.photo_info = {'photos': {}}
        count_photo = 0
        pbar = tqdm(total=count)
        for dict_foto in list_photos.json()['response']['items']:
            count_photo += 1
            self.name_photo = f"{dict_foto['likes']['count']} likes"
            # Если имя(одинаковое) по кол-ву likes уже имеется, то добавляется дата.
            if self.name_photo in like_name:
                date_photo = datetime.datetime.utcfromtimestamp(int(dict_foto['date'])).strftime('%Y-%m-%d_%H-%M-%S')
                self.name_photo = f'{self.name_photo} - {date_photo}'
            add = {f'{count_photo}': {'file_name': self.name_photo,'size': dict_foto['sizes'][-1]['type']}}
            self.photo_info['photos'].update(add)
            # Добавляем имя файла в список
            like_name.append(self.name_photo)
            # Список имён файлов которые создадутся в папке, и позже будут удалены после загрузки на GDrive
            self.list_name_photos.append(self.name_photo)

            self.photo_url = dict_foto['sizes'][-1]['url']

            # РАЗВЛЕТЛЕНИЕ В КАКОЕ ОБЛОКО ЗАГРУЖАТЬ
            if self.token_yandex == 0:
                send.g_upload(self.photo_url, self.name_photo)
            else:
                send.uploadYD(self.photo_url, self.name_photo)

            pbar.update(1)
        pbar.close()

        if count_photo < count:
            print(f'Вы указали больше фотографий чем имеется в профиле. \n'
                  f'Выгружено {count_photo} из {count} запрошенных.')
            time.sleep(5)

        self.json_photo_result()

        # Удаление файлов после загрузки на GDrive
        if self.token_yandex == 0:
            for name in self.list_name_photos:
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{name}")
                os.remove(path)


    def json_photo_result(self):
        print()
        with open("photo_info_VK.json", "w") as file:
            json.dump(self.photo_info, file, indent=4)

        with open("photo_info_VK.json", "r") as file:
            json_result = file.read()
            print(json_result)
