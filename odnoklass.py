import requests
from pprint import pprint
from tqdm import tqdm
import Yandexdrive
import re
from selenium import webdriver
import hashlib
import datetime
import time
import json
import Gdrive
import os


class Odnoklassniki:
    def __init__(self, log_ok, pass_ok, token_yandex, count):
        pbar = tqdm(total=3)
        self.log_ok = log_ok
        self.pass_ok = pass_ok
        self.token_yandex = token_yandex
        self.count = count

        time.sleep(0.5)
        pbar.update(1)

        driver = webdriver.Firefox()
        driver.get("https://connect.ok.ru/oauth/authorize?client_id=512000982149&scope=VALUABLE_ACCESS;LONG_ACCESS_TOKEN&response_type=token&redirect_uri=https://apiok.ru/oauth_callback")

        # Для удобства сохраняем XPath формы авторизации
        username = '//*[@id="field_email"]'
        password = '//*[@id="field_password"]'
        login = '/html/body/div/form/div/div[2]/div/div/div[4]/input'
        press_okey = '/html/body/div/form/div/div[3]/button'

        # Заполняем форму авторизации
        driver.find_element_by_xpath(username).send_keys([log_ok])
        driver.find_element_by_xpath(password).send_keys([pass_ok])
        driver.find_element_by_xpath(login).click()
        driver.find_element_by_xpath(press_okey).click()
        tokens = driver.current_url
        driver.close()

        pbar.update(1)
        time.sleep(0.5)

        res = re.split('&|=', tokens)
        self.access_token = res[1]
        self.session_secret_key = res[3]

        pbar.update(1)

        pbar.close()

        self.ok_upload()

    # Получим json 20 фото, с лайками, максКачественное фото и дата создания(загрузки)
    def ok_upload(self):
        url = 'https://api.ok.ru/fb.do'
        params = {
            'application_key': 'CGINPDKGDIHBABABA',
            'fields': 'photo.LIKE_COUNT,photo.PIC_MAX,photo.CREATED_MS',
            'format': 'json',
            'method': 'photos.getPhotos',
            'sig': '',
            'access_token': self.access_token
        }
        params_copy = dict.copy(params)
        del [params_copy['sig']]
        del [params_copy['access_token']]

        url_for_md5 = ''
        for key,val in params_copy.items():
            url_for_md5 += str(f'{key}={val}')
        url_for_md5 += self.session_secret_key
        params['sig'] = [hashlib.md5(url_for_md5.encode('utf-8')).hexdigest()]
        res = requests.get(url, params=params).json()

        if self.token_yandex == 0:
            send = Gdrive.GoogleDrive(2)
        else:
            # create class in file Yandexdrive.py (при __init__ создается папка)
            send = Yandexdrive.YandexDrive(self.token_yandex, 2)
            time.sleep(1)

        # Получаем ссылки на фото и лайки
        photo_info_list = []
        self.list_name_photos = []
        for inf_photo in res['photos']:
            del(inf_photo['type'])
            del(inf_photo['text_detected'])
            photo_info_list.append(inf_photo)

        self.photo_info = {'photos': {}}
        like_name = []
        count_photo = 0
        pbar = tqdm(total=self.count)
        for dict_photo in photo_info_list[0:self.count]:
            count_photo += 1
            name_photo = f'{dict_photo["like_count"]} likes'
            if name_photo in like_name:
                date_photo = datetime.datetime.utcfromtimestamp(int(dict_photo['created_ms'] / 1000)).strftime('%Y-%m-%d_%H-%M-%S')
                name_photo = f'{name_photo} - {date_photo}'
            add = {f'{count_photo}': {'file_name': name_photo, 'size': 'pic_max'}}

            self.photo_info['photos'].update(add)

            like_name.append(name_photo)
            self.list_name_photos.append(name_photo)

            photo_url = dict_photo["pic_max"]

            # РАЗВЛЕТЛЕНИЕ В КАКОЕ ОБЛОКО ЗАГРУЖАТЬ
            if self.token_yandex == 0:
                send.g_upload(photo_url, name_photo)
            else:
                send.uploadYD(photo_url, name_photo)

            pbar.update(1)
        pbar.close()

        if count_photo < self.count:
            print(f'Вы указали больше фотографий чем имеется в профиле. \n'
                  f'Выгружено {count_photo} из {self.count} запрошенных.')
            time.sleep(5)

        self.json_photo_result()

        if self.token_yandex == 0:
            for name in self.list_name_photos:
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{name}")
                os.remove(path)


    def json_photo_result(self):
        print()
        with open("photo_info_OK.json", "w") as file:
            json.dump(self.photo_info, file, indent=4)

        with open("photo_info_OK.json", "r") as file:
            json_result = file.read()
            print(json_result)
