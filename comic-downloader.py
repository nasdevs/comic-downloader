'''
@author : Nasrullah
@github : github.com/nasdevs
'''

import re, os, requests

from requests.exceptions import ConnectionError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
from tqdm.auto import tqdm

def download_chapter(urls, 
                     pattern=None,
                     tag='div',
                     tag_attribute=None,
                     name_tag_attribute=None,
                     tag_img='img',
                     img_attribute='src', 
                     path='./'):
    
    os.makedirs(path, exist_ok=True)
    
    for url in tqdm(urls):
        title = ''.join(re.findall(pattern, url))            
        file_path = path + title + '.pdf'
        
        if os.path.exists(file_path) and os.stat(file_path).st_size != 0:
            print(title, ': File is exists.')
            continue
            
        print('Downloading :', title)
        r = requests.get(str(url))
        soup = BeautifulSoup(r.content, 'html.parser')
        

        img_urls = [img_url.get(img_attribute) for img_url in soup.find(tag, {tag_attribute: name_tag_attribute}).find_all(tag_img)]

        result = []

        for image in tqdm(img_urls):
            while True:
                try:
                    img_req = requests.get(str(image), stream=True)
                except ConnectionError as e:
                    print(e)
                    continue
                except UnidentifiedImageError as e:
                    print(e)
                    continue

                result.append(Image.open(img_req.raw).convert('RGB'))
                break

        result[0].save(file_path, save_all=True, append_images=result[1:])
        
        print('------------------------------------------------------------------')

        
def example():
    web = 'https://komiku.id/'
    url = web+'manga/eleceed/'

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    chapters = [web+ch.find('a').get('href') for ch in soup.find_all('td', {'class': 'judulseries'})][::-1]
    
    download_chapter(urls = chapters,
                 pattern = 'ch/(.*)/',
                 tag = 'section',
                 tag_attribute = 'id',
                 name_tag_attribute = 'Baca_Komik',
                 tag_img = 'img',
                 img_attribute = 'src', 
                 path='eleceed/')
    print('Done!')
    
if __name__=='__main__':
    example()
