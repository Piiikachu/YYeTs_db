import sqlite3
import os
import json
from sqlite3.dbapi2 import Cursor

CONFIG_PATH = "config.json"

select_movie = """
SELECT * FROM main.movie_info WHERE cnname LIKE '{}%' OR enname LIKE '{}%' OR aliasname LIKE '{}%';
"""

select_season = """
SELECT * FROM main.season_info WHERE movie_id='{}' order by season_num asc;
"""

select_episode = """
SELECT * FROM main.episode_info WHERE movie_id='{}' and season='{}' and format='{}' order by episode asc;
"""


def getDatabasePath() -> str:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='UTF-8') as f:
            s = json.load(f)['dbPath']
            print('成功读取yyets.db路径: {}'.format(s))
            return s
    else:
        s = input('请输入yyets.db路径，如F:\Download\yyets.db\n')
        if os.path.exists(s) & (os.path.basename(s) == 'yyets.db'):
            with open(CONFIG_PATH, 'w', encoding='UTF-8') as f:
                json.dump({"dbPath": s}, f)
            print('成功配置yyets.db路径: {}'.format(s))
            return s
        else:
            raise FileExistsError('该路径 “{}” 不存在'.format(s))


def connectDb(db_path: str) -> Cursor:
    conn = sqlite3.connect(db_path)
    print('连接到数据库')
    print()
    return conn.cursor()


def checkNum(input: str, max: int):
    if not input.isdigit():
        raise TypeError('请输入数字')
    index = int(input)
    if index not in range(1, max+1):
        raise IndexError('数字超出范围')
    return index


def getURLs(episodes: list):
    pass


def getURL(episode: tuple):
    link = episode[-2]



def search_episode(cur: Cursor, movie_id: str, season_num: str, fmt: str):
    cur.execute(select_episode.format(movie_id, season_num, fmt))
    result = cur.fetchall()
    count = len(result)
    print('共查询到{}个文件', count)
    print('0. 全选，默认磁力')
    for i, episode in enumerate(result):
        _, _, _, episodeNum, _, _, name, fileSize, _, _, _, wayCn, _, _ = episode
        print('{}. 第{}集,{},文件大小：{},下载方式：{}'.format(
            i+1, episodeNum, name, fileSize, wayCn))
    print()
    episodeIndex = input('请选集\n')
    if episodeIndex == "0":
        getURLs(result)
    else:
        index = checkNum(episodeIndex, count)
        getURL(result[index-1])


def search_season(cur: Cursor, movie_id: str):
    cur.execute(select_season.format(movie_id))
    result = cur.fetchall()
    count = len(result)
    if count == 0:
        print("未查询到相关内容")
        return
    print('查询到{}季'.format(count))
    for i, season in enumerate(result):
        print('{}. {},共{}集,可选择格式[{}] '.format(
            i+1, season[3], season[4], season[5]))
    print()
    seasonIndex = input('请选择剧集 1-{}\n'.format(count))
    index = checkNum(seasonIndex, count)
    print()
    print('选择了{}'.format(result[index-1][3]))

    fmtList = season[5].split(',')
    count2 = len(fmtList)
    print()
    print('共查询到{}种格式'.format(count2))
    for i, fmt in enumerate(fmtList):
        print('{}. 格式：{}'.format(i+1, fmt))
    print()
    fmtIndex = input('请选择格式 1-{}\n'.format(count2))
    index2 = checkNum(fmtIndex, count2)
    search_episode(cur, movie_id, result[index-1][2], fmtList[index2-1])


def search(cur: Cursor):
    s = input('请输入剧名:\n')
    cur.execute(select_movie.format(s, s, s))
    result = cur.fetchall()
    count = len(result)
    if count == 0:
        print("未查询到相关内容")
    else:
        print()
        print("共找到{}条记录".format(count))
        for i, line in enumerate(result):
            print(i+1, line[1:-3])
        print()
        movieIndex = input('请输入序号：1-{}\n'.format(count))

        index = checkNum(movieIndex, count)
        print()
        print("查询《{}》:".format(result[index-1][1]))
        search_season(cur, result[index-1][0])


if __name__ == "__main__":
    s = getDatabasePath()
    cur = connectDb(s)

    search(cur)

    cur.close()
