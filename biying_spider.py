import requests
import time
import re
import random
from lxml import etree


class BiYingSpider(object):
    def __init__(self):
        self.status = ""
        self.replace_url_list = []
        self.url = "https://bing.ioliu.cn/?p={}"
        self.url_list = [self.url.format(i) for i in range(1, 94)]
        self.xpath = '/html/body//div[@class="card progressive"]/img/@src'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

    def get_html(self, url, status):
        self.status = status
        if self.status:
            time.sleep(random.randint(4, 9))
        response = requests.get(url=url, headers=self.headers)
        return response.content

    def extraction_data(self, html):
        page_element = etree.HTML(html)
        picture_urls = page_element.xpath(self.xpath)
        return picture_urls

    def replace_url(self, urls):
        for j in urls:
            picture_size = re.findall(r'.*_(\w+)\.jpg', j)
            replace_urls = j.replace(picture_size[0], "1920x1080")
            self.replace_url_list.append(replace_urls)
        return self.replace_url_list

    def save_picture(self, picture, page, num):
        with open("./picture/{}-{}.jpg".format(page+1, num+1), 'wb') as f:
            f.write(picture)
        if num + 1 == 12:
            self.replace_url_list = []
        print("已保存{}_{}.jpg".format(page+1, num+1))


# 主入口函数
def main():
    bys = BiYingSpider()
    for each_url in bys.url_list:
        html = bys.get_html(each_url, True)
        picture_urls = bys.extraction_data(html)
        replace_url_list = bys.replace_url(picture_urls)
        for k in replace_url_list:
            picture = bys.get_html(k, False)
            bys.save_picture(picture, bys.url_list.index(each_url), replace_url_list.index(k))


if __name__ == "__main__":
    main()
