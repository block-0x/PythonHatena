import os
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re


class HatenaScraper(object):

    def __init__(self, user_name, csv_file_name):
        self.youtube_url = "http://b.hatena.ne.jp/"
        self.user_name = "text?safe=on&q=Python&users=50"
        self.csv_file_name = "sample"
        self.csv_file_path = os.path.join(os.getcwd(), self.csv_file_name+'.csv')
        self.channel_videos_url = os.path.join(self.youtube_url, 'search', self.user_name)
        self.titles = []
        self.video_urls = []
        self.good_counts = []

    def run(self):
        self.get_page_source()
        self.parse_video_title_and_url()
        self.save_as_csv_file()

    def get_page_source(self):
        '''
        YoutubeChannelページの
        最下部までスクロールしたページソースを取得
        '''
        self.driver = webdriver.Chrome()
        self.driver.get(self.channel_videos_url)
        self.current_html = self.driver.page_source

        actions = ActionChains(self.driver)
        actions.perform()
        actions.reset_actions()

        while True:
            for j in range(100):
                actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            sleep(3)
            html = self.driver.page_source
            if self.current_html != html:
                self.current_html=html
            else:
                break

    def parse_video_title_and_url(self):
        '''
        タイトルと動画URLを抽出
        '''
        soup = BeautifulSoup(self.current_html, 'html.parser')
        for i in soup.find_all("a"):
            title = (i.get("title"))
            url = (i.get("href"))
            good_count_text = (i.get("title"))
            if title is None:
                continue
            elif url is None:
                continue
            elif good_count_text is None:
                continue
            good_count_text = title.replace('　', ' ')
            good_count_int = re.findall('[0-9]+', good_count_text)
            if len(good_count_int) > 1:
                good_count = good_count_int[-1]
            else:
                good_count_arry = good_count_int
                good_count = ','.join(good_count_arry)
                print(good_count)
            if "/entry/s/" in url:
                self.titles.append(title)
                self.video_urls.append(url)
                self.good_counts.append(good_count)

    def save_as_csv_file(self):
        '''
        CSVファイルとして保存
        '''
        data = {
         "title": self.titles,
         "url": self.video_urls,
         "good_count": self.good_counts
        }
        pd.DataFrame(data).to_csv(self.csv_file_path,index=False)


if __name__ == "__main__":
    scraper = HatenaScraper(user_name="text?safe=on&q=Python&users=50", csv_file_name="text?safe=on&q=Python&users=50")
    scraper.run()