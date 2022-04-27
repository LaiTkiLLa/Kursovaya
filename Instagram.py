import requests
import json
import time
from tqdm import tqdm

def photo_link(access_token_instagram = input('Введите долгосрочный токен инстаграм:\n')):
    fields = 'id,media_url'
    url_insta = 'https://graph.instagram.com/me/media?fields=' + fields + '&access_token=' + access_token_instagram
    res = requests.get(url=url_insta)
    response = res.json()['data']
    links = []
    names = []
    for media in response:
        download_url = media['media_url']
        name = media['id']
        links.append(download_url)
        names.append(name)
    return links, names

def create_path(new_folder = input('Введите название папки:\n'),ya_token = input('Введите токен яндекса:\n')):
    links,names = photo_link()
    headers = {"Authorization": ya_token}
    url_ya_create_path = 'https://cloud-api.yandex.net/v1/disk/resources'
    params_new_folder = {'path':new_folder}
    resp = requests.put(url=url_ya_create_path, headers=headers, params=params_new_folder)
    return new_folder, headers

def upload_photo_insta():
    links,names = photo_link()
    new_folder, headers = create_path()
    url_ya_upload_photo = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    upload_photo = list(zip(links, names))
    for values in upload_photo:
        params_insta = {'path': f'{new_folder}/{values[1]}', 'overwrite': 'true', 'url': values[0]}
        resp = requests.post(url=url_ya_upload_photo, headers=headers, params=params_insta)
        for i in tqdm([1], 'Процесс загрузки фото'):
            time.sleep(2)
    print(f'Было загружено {len(links)} фотографий')

def save_results():
    upload_photo_insta()
    links,names = photo_link()
    links_names = dict(zip(links,names))
    json_list = []
    for link,name in links_names.items():
        file_dict = {}
        file_dict['filename'] = f'{link}.jpg'
        file_dict['name'] = name
        json_list.append(file_dict)
    with open('final.json', 'w') as file:
        json.dump(json_list,file)

save_results()
