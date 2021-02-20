import json
import os
import sqlite3
from sqlite3.dbapi2 import Cursor


class SqlError(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return repr('SQL Error occurred, msg: '+self.msg)


class AppCore():
    def __init__(self) -> None:
        self.CONFIG_PATH = 'config.json'
        self.config = self.getConfig()
        self.conn = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def getConfig(self) -> dict:
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, 'r', encoding='UTF-8') as f:
                config: dict = json.load(f)
                return config
        return {}

    def setConfig(self, config: dict):
        with open(self.CONFIG_PATH, 'w', encoding='UTF-8') as f:
            json.dump(config, f, indent=4)

    def getDBPath(self) -> str:
        if 'dbPath' in self.config.keys():
            return self.config['dbPath']
        return None

    def setDBPath(self, path: str):
        self.config['dbPath'] = path
        self.setConfig(self.config)

    def connect(self):
        dbPath = self.getDBPath()
        if dbPath is not None and os.path.exists(dbPath):
            self.conn = sqlite3.connect(dbPath)
        else:
            raise SqlError(f'连接到数据库失败，请检查数据库路径 {dbPath}')

    def query(self, sql: str) -> list:
        if self.conn is not None:
            result = self.conn.cursor().execute(sql)
            return result.fetchall()
        else:
            raise SqlError(f'未连接到数据库')

    def queryMovie(self, name: str) -> list:
        if name.isalnum():
            sql = f"SELECT * FROM movie_info WHERE enname LIKE '{name}%' "
        else:
            sql = f"SELECT * FROM movie_info WHERE cnname LIKE '{name}%' OR aliasname LIKE '{name}%' "
        movies = self.query(sql)
        return movies

    def querySeason(self, movieId: str) -> list:
        sql = f"SELECT * FROM season_info WHERE movie_id='{movieId}' order by season_num"
        seasons = self.query(sql)
        return seasons

    def queryEpisode(self, movieId: str, seasonNum: str, format: str) -> list:
        sql = f"SELECT * FROM episode_info WHERE movie_id='{movieId}' AND season='{seasonNum}' AND format='{format}' order by episode "
        print(sql)
        episodes = self.query(sql)
        return episodes


if __name__ == '__main__':
    core = AppCore()
    core.connect()
    print(core.queryMovie('friend'))
