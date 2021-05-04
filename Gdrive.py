from __future__ import print_function
import os
import os.path
import pprint
import time
import datetime

import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


# Код из файла(инструкции) от Google Quickstart.py
class GoogleDrive():
    def __init__(self, social_networks):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)
        self.create_folder(social_networks)


    def create_folder(self, social_networks):
        # Создание ПАПКИ на диске
        now_data_time = datetime.datetime.now()
        now_data_time = now_data_time.strftime("%d-%m-%Y_%H.%M")
        if social_networks == 1:
            text = 'Backup_photo_VK_'
        elif social_networks ==2:
            text = 'Backup_photo_OK_'
        elif social_networks ==3:
            text = 'Backup_photo_instagram_'
        now_data = f'{text}{now_data_time}'

        file_metadata = {
            'name': now_data,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        self.service.files().create(body=file_metadata).execute()
        time.sleep(0.5)


        # Получаем ID папки
        results = self.service.files().list(
            pageSize=1, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])


        self.folder_id = items[0]['id']



    def g_upload(self, photo_url, name_photo):
        # Загрузка файла осуществлена с помощью загрузки файла на ПК, после чего идёт загрузка самого файла
        # на GDrive, после загрузки всех файлов в облако, файлы с ПК удаляются.
        with open(f"{name_photo}", 'wb') as f:
            url_file = requests.get(photo_url)
            f.write(url_file.content)

        file_path = f"{name_photo}"
        file_metadata = {
            'name': name_photo,
            'parents': [self.folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
