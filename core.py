import json
from os import path

CONFIG_PATH = 'config.json'


def getDBPath() -> str:
    if path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='UTF-8') as f:
            config: dict = json.load(f)
            if 'dbPath' in config.keys():
                dbPath = config['dbPath']
                print(f'成功读取yyets.db路径: {dbPath}')
                return dbPath
    return None
