import requests
import json
from lxml import html
import os
import random

urlsrs = 'urls.txt'

def get_urllist(urls):
    urllist = []
    with open(urls) as urlfile:
        urllist = urlfile.read().splitlines()
    return urllist
    
def getrequest(url):
    responses = requests.get(url)
    html1 = responses.text
    tree = html.fromstring(html1)
    return html1, tree

def makedir():
    result = getrequest(url)
    n = random.randint(0,300) #посмотри может есть какие идентификаторы объявления
    start_json_template = "    window.__YOULA_STATE__ = "

    if start_json_template in result[0]:
        foldername = result[1].xpath('//title/text()')[0].split('–')[0]
        if os.path.exists(foldername) == False:     
            foldername = result[1].xpath('//title/text()')[0].split('–')[0]
            os.mkdir(foldername)        
        else:
            foldername = result[1].xpath('//title/text()')[0].split('–')[0]+str(n)
            os.mkdir(foldername)
        os.chdir(foldername)

def get_json():
    result_to_json = getrequest(url)
    start_json_template = "    window.__YOULA_STATE__ = "
    if start_json_template in result_to_json[0]:    
        start = result_to_json[0].index(start_json_template) + len(start_json_template)
        end = result_to_json[0].index('    window.__YOULA_TEST__ = ', start)
        json_raw = result_to_json[0][start:end].strip()[:-1]
        json1 = json.loads(json_raw)
        return json1    
    
def savephotos():
    photos = []
    for photo in get_json()['entities']['products'][0]['images']:
        photos.append(photo['url'])

    print(photos)
    for photka in photos:
        filename = photka.split('/')[-1]
        with open(filename, 'wb') as imgf:
            imgf.write(requests.get(photka).content)     
    save_description() #созраняем описание в папке объявления
    os.chdir('..') #переходим на уровень выше в исходную папку

def save_description():
    desc_raw = get_json()['entities']['products'][0]['description']
    desc = desc_raw.encode('utf-8').decode('utf-8')
    with open('текст_объявления.txt', 'w', encoding='utf-8') as textob:
        textob.write(desc)
    
for url in get_urllist(urlsrs):
    makedir()
    savephotos()
