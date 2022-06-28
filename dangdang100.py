import requests
import re
import json
import pandas as pd


def request_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(e)
        return None

def parse_result(html):
    pattern = re.compile(
        '<li.*?list_num.*?(\d+)\.</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span class="price_n">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)
    return items

def main(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html = request_dandan(url)
    items = parse_result(html)
    dt = pd.DataFrame(columns=['排名','书名','图片地址','作者','推荐指数','五星评分次数','价格'],data=list(items))
    return dt
        
if __name__ == "__main__":
    data = pd.DataFrame()
    for i in range(1, 6):  
        data = pd.concat([data,main(i)])
    data.to_excel('book.xlsx')
