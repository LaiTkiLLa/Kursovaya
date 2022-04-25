import requests
import json
import time
from tqdm import tqdm

def photo_link(vk_token=input('Введите токен вконтакте:\n'),id_vk=input('Введите ваш vk id:\n')):
    method = 'photos.get'
    V = '5.131'
    url_vk = 'https://api.vk.com/method/' + method + '?PARAMS&access_token=' + vk_token + '&v=' + V
    params_vk = {'owner_id': id_vk, 'album_id': 'profile', 'extended': '1'}
    res = requests.get(url=url_vk, params=params_vk)
    response = res.json()['response']['items']
    links = []
    sizes = []
    likes = []
    for result in response:
        size = result['sizes'][-1]['type']
        like = result['likes']['count']
        download_url = result['sizes'][-1]['url']
        links.append(download_url)
        sizes.append(size)
        likes.append(like)
    return links,sizes,likes

def create_path(ya_token=input('Введите токен Яндекса\n'),new_folder=input('Введите название папки\n')):
    links,sizes,likes = photo_link()
    url_ya_create_path = 'https://cloud-api.yandex.net/v1/disk/resources'
    params_new_folder = {'path':new_folder}
    headers = {"Authorization": ya_token}
    resp = requests.put(url=url_ya_create_path, headers=headers, params=params_new_folder)
    return new_folder,headers

def upload_photo():
    url_ya_upload_photo = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    links,sizes,likes = photo_link()
    new_folder,headers = create_path()
    upload_photo = list(zip(links, likes))
    for values in upload_photo:
        params_ya_upload = {'path': f'{new_folder}/{values[1]}', 'overwrite': 'true', 'url': values[0]}
        resp = requests.post(url=url_ya_upload_photo, headers=headers, params=params_ya_upload)
        for i in tqdm([1], 'Процесс загрузки фото'):
            time.sleep(2)
    print(f'Было загружено {len(links)} фотографий')

def save_results():
    upload_photo()
    links,sizes,likes = photo_link()
    likes_sizes = dict(zip(likes,sizes))
    json_list = []
    for like,size in likes_sizes.items():
        file_dict = {}
        file_dict['filename'] = f'{like}.jpg'
        file_dict['size'] = size
        json_list.append(file_dict)
    with open('final.json', 'w') as file:
        json.dump(json_list,file)

save_results()
