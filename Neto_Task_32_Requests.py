import requests
import os

From_Dir = 'To_YDisk'


class YaUploader:
    host = 'https://cloud-api.yandex.net'

    def __init__(self, token: str):
        self.token = token

    def upload(self, path_to_disk: str, file_list: list):
        """Метод загружает файлы по списку file_list на Яндекс диск"""

        # url и headers запроса для получения ссылки для загрузки файла (Полигон https://yandex.ru/dev/disk/poligon/ ):
        url = f'{self.host}/v1/disk/resources/upload/'
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'OAuth {self.token}'}

        for file in file_list:
            # Путь (папка/файл) на Яндекс диске; перезапись файла
            params = {'path': f'{path_to_disk}/{file}', 'overwrite': True}

            # получение ccылки для последующей загрузки файла:
            res_get = requests.get(url, headers=headers, params=params)
            link = res_get.json().get('href')

            # загрузка файла на диск:
            res_put = requests.put(link, data=open(f'{From_Dir}/{file}', 'rb'), headers=headers)

            # печать результата операции:
            res_put.raise_for_status()
            if res_put.status_code == 201:
                print(f'<Ok - {file}>')
            else:
                print(f'<Ошибка. Код: {res_get.status_code}>')


if __name__ == '__main__':
    path_to_dir = f'{os.getcwd()}/{From_Dir}'  # путь к папке, откуда берем файлы
    file_list = os.listdir(path_to_dir)

    path_to_disk = f'/Target_dir'  # целевая папка на Яндекс диске

    YANDEX_TOKEN = '***************************************'  # DELETED
    uploader = YaUploader(YANDEX_TOKEN)

    uploader.upload(path_to_disk, file_list)
