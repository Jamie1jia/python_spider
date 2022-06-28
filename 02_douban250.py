import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def request_douban(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.146 Safari/537.36',
    }

    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def save_to_excel(soup):
    ls = soup.find(class_='grid_view').find_all('li')
    a = np.empty((6,),dtype='str')
    for item in ls:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        item_intr = ''
        if (item.find(class_='inq') != None):
            item_intr = item.find(class_='inq').string
        b = np.array([item_name,item_img,item_index,item_score,item_author,item_intr])
        a = np.append(a, values=b, axis=0)
    return a

def main(page):
    url = 'https://movie.douban.com/top250?start=' + str(page * 25) + '&filter='
    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    dt = pd.DataFrame(save_to_excel(soup).reshape(26,6))
    dt.drop(index=0,inplace=True)
    dt.columns=['名称','图片','排名','评分','作者','简介']
    return dt

if __name__ == '__main__':

    data = pd.DataFrame()
    for i in range(0, 10):
        data = pd.concat([data,main(i)])

data.to_excel(u'豆瓣最受欢迎的250部电影.xlsx',index=False)
