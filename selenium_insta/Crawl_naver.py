import requests
import csv
from bs4 import BeautifulSoup


def crawl_naver():
    result_list = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={category}&date={date}&page={page}'
    response = requests.get(headers=headers, url=url)

    soup = BeautifulSoup(response.text, 'html.parser')

    tags = soup.select('.type06_headline li')
    for tag in tags:
        title = tag.select('a')[-1].text.strip()
        writing = tag.select('.writing')[0].text
        content = tag.select('.lede')[0].text
        date = tag.select('.date')[0].text
        result_list.append([title, content, writing, date])

    return result_list


output = crawl_naver(103, 20230101, 1)
with open('news.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output)
