from bs4 import BeautifulSoup
import requests as requests
import json
from urls import url_list
import re
from database import Sqlite
from config import dbName


def get_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)

        json_data = json.loads(data)

        channel_id = json_data['header']['c4TabbedHeaderRenderer']['channelId']
        channel_name = json_data['header']['c4TabbedHeaderRenderer']['title']
        logo = json_data['header']['c4TabbedHeaderRenderer']['avatar']['thumbnails'][2]['url']
        count_of_subscribers = \
            json_data['header']['c4TabbedHeaderRenderer']['subscriberCountText']['accessibility']['accessibilityData'][
                'label']

        return {'channel_id': channel_id,
                'channel_name': channel_name,
                'logo': logo,
                'link': url,
                'count_of_subscribers': count_of_subscribers}
    except Exception as e:
        print(url , e)


class Parser:
    def __init__(self):
        self.db = Sqlite(dbName)

    def initialize(self):
        try:
            self.db.create_youtube_table()
            for url in url_list:
                if not self.db.exists_channel_info(url):
                    self.db.insert_new_channel(get_data(url))

            print('\nDatabase is ready for work!!!')
        except Exception as e:
            print(e)

    def update_information(self):
        try:
            for url in url_list:
                if self.db.exists_channel_info(url):
                    self.db.update_channel_info(get_data(url))
                else:
                    self.db.insert_new_channel(get_data(url))
            print('\nDatabase updated!!!')
        except Exception as e:
            print(e)