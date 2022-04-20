import requests
import json
import time
from tqdm import tqdm

method = 'photos.get'
vk_token = input('Введите токен вконтакте:\n')
V = '5.131'
id_vk = input('Введите ваш vk id:\n')
ya_token = input('Введите токен яндекса:\n')
url_vk = 'https://api.vk.com/method/'+method+'?PARAMS&access_token='+vk_token+'&v='+V
params_vk = {'owner_id' : id_vk, 'album_id' : 'profile', 'extended' : '1'}
url_ya_create_path = 'https://cloud-api.yandex.net/v1/disk/resources'
url_ya_upload_photo = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
headers = {"Authorization": ya_token}

def photo_link():
    res = requests.get(url=url_vk, params=params_vk)
    response = res.json()['response']['items']
    # print(response)
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

def create_path():
    links,sizes,likes = photo_link()
    new_folder = input('Введите название папки:\n')
    params_new_folder = {'path':new_folder}
    resp = requests.put(url=url_ya_create_path, headers=headers, params=params_new_folder)
    return new_folder

def upload_photo():
    links,sizes,likes = photo_link()
    new_folder = create_path()
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


# fields = 'id,media_url'
# access_token = input('Введите долгосрочный токен:\n')
# media_id = input('Введите user_id\n')
# url_insta = 'https://graph.instagram.com/me/media?fields='+fields+'&access_token='+access_token
#
# def photo_link_insta():
#     res = requests.get(url=url_insta)
#     response = res.json()['data']
#     # print(res.json())
#     for media in response:
#         download_url = media['media_url']
#         name = media['id']
#         params_insta = {'path': name, 'overwrite': 'true', 'url': download_url}
#         resp = requests.post(url=url_ya, headers=headers, params=params_insta)
#         print(resp.json())
#
# print(photo_link_insta())