import datetime
import requests
from pprint import pprint
import time


class YandexDrive:
    def __init__(self, tokenYD, social_networks):
        now_data_time = datetime.datetime.now()
        now_data_time = now_data_time.strftime("%d-%m-%Y_%H.%M")
        if social_networks == 1:
            text = 'Backup_photo_VK_'
        elif social_networks ==2:
            text = 'Backup_photo_OK_'
        elif social_networks ==3:
            text = 'Backup_photo_instagram_'
        self.now_data = f'{text}{now_data_time}'
        self.tokenYD = tokenYD
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.tokenYD}'}
        self._create_path()

    def _create_path(self):
        # Создаем папку для хранения ФОТО
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': self.now_data}
        response = requests.put(url, headers=self.headers,params=params).json()
        print(f'Ссылка на папку: https://disk.yandex.ru/client/disk/{self.now_data}')

    def uploadYD(self, photo_url, name_photo):
        # Получения ссылки для загрузки файла, по ссылке.
        self.photo_url = photo_url
        self.name_photo = name_photo
        url_uploade = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'url': self.photo_url, 'path': f'{self.now_data}/{self.name_photo}'}
        response = requests.post(url_uploade, headers=self.headers, params=params).json()
        time.sleep(1)
