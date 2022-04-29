import sqlite3


class Sqlite:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def create_youtube_table(self):
        self.cur.execute('Create Table if not exists youtube('
                         'id integer PRIMARY KEY AUTOINCREMENT NOT NULL,'
                         'channel_id varchar(255),'
                         'channel_name varchar(255),'
                         'link varchar(255),'
                         'logo varchar(255),'
                         'count_of_subscribers varchar(255)'
                         ')'
                         )

    def insert_new_channel(self, data):
        self.cur.execute(
            'Insert into youtube(channel_id, channel_name, link, logo, count_of_subscribers) values(?,?,?,?,?)',
            (data['channel_id'], data['channel_name'], data['link'], data['logo'], data['count_of_subscribers']))
        self.conn.commit()

    def update_channel_info(self, data):
        self.cur.execute(
            f"Update youtube "
            f"Set channel_name='{data['channel_name']}', "
            f"channel_id='{data['channel_id']}', "
            f"logo='{data['logo']}', "
            f"count_of_subscribers = '{data['count_of_subscribers']}'"
            f"where link='{data['link']}';"
        )
        self.conn.commit()

    def exists_channel_info(self, url):
        self.cur.execute(
            f"Select count(*) from youtube where link = '{url}'"
        )
        return self.cur.fetchone()[0] > 0
