import requests
from pprint import pprint
from tqdm import tqdm
import Yandexdrive
import Gdrive
import json
import os

class Instagram:
    def __init__(self, access_token, token_yandex, count):
        # Получения id пользователя по токену
        url_id = 'https://graph.instagram.com/me'
        self.access_token = access_token
        self.token_yandex = token_yandex
        self.count = count
        params = {
            'fields': 'id,username',
            'access_token': self.access_token
        }
        answer = requests.get(url_id, params=params).json()
        user_id = answer['id']

        self.get_photo()


    def get_photo(self):
        # Получения списка фотографий
        url_photo = f'https://graph.instagram.com/me/media'
        params = {
            'access_token': self.access_token
        }
        answer = requests.get(url_photo, params=params).json()

        # Получение списка id каждого медиа файла(от самого свежего к старому)
        list_id_photos = []
        self.list_name_photos = []
        for dict_id in answer['data']:
            list_id_photos.append(int(dict_id['id']))


        # Если Яндекс токен не указан(token == 0) то работаем с Gdrive
        # Если токен указан(token != 0) работаем с YaDisk
        if self.token_yandex == 0:
            send = Gdrive.GoogleDrive(3)
        else:
            # create class in file Yandexdrive.py (при __init__ создается папка)
            send = Yandexdrive.YandexDrive(self.token_yandex, 3)


        # Получение ссылки на фото по id
        self.photo_info = {'photos': {}}
        pbar = tqdm(total=self.count)
        for id in list_id_photos[0:self.count]:
            photo_id = id
            url_id_photo = f'https://graph.instagram.com/{photo_id}'
            params = {
                'fields': 'id,media_type,media_url,timestamp',
                'access_token': self.access_token
            }
            answer = requests.get(url_id_photo, params=params).json()

            name_photo = answer['timestamp'][0:answer['timestamp'].find('+')]
            name_photo = name_photo.replace('T', '_').replace(':', '-')

            photo_url = answer['media_url']

            add = {f'{photo_id}': {'name_photo': name_photo, 'photo_url': photo_url}}
            self.photo_info['photos'].update(add)

            self.list_name_photos.append(name_photo)

            # РАЗВЛЕТЛЕНИЕ В КАКОЕ ОБЛОКО ЗАГРУЖАТЬ
            if self.token_yandex == 0:
                send.g_upload(photo_url, name_photo)
            else:
                send.uploadYD(photo_url, name_photo)


            pbar.update(1)
        pbar.close()

        self.json_photo_result()

        if self.token_yandex == 0:
            for name in self.list_name_photos:
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{name}")
                os.remove(path)


    def json_photo_result(self):
        print()
        with open("photo_info_Inst.json", "w") as file:
            json.dump(self.photo_info, file, indent=4)

        with open("photo_info_Inst.json", "r") as file:
            json_result = file.read()
            print(json_result)