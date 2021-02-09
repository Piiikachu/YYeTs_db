import pandas as pd
import json

# tools for parsing raw data
# input: 'resouce.csv' file from @BennyThink
# output: sql files that can be import to the database

df1 = pd.read_csv('resource.csv')

data1 = json.loads(df1.loc[0, 'data'])

insert_season = """
INSERT INTO main.season_info (movie_id,season_num,season_cn,episode_count,formats)
VALUES ('{}','{}','{}','{}','{}');
"""

insert_episode = """
INSERT INTO main.episode_info (movie_id,season,episode,format,item_id,name,file_size,yyets_trans,dateline,way,way_cn,address,password)
VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");
"""

with open('season.sql', 'w', encoding='utf-8') as s, open('episode.sql', 'w', encoding='utf-8') as e:
    jsonObjs = df1['data'].map(json.loads)
    for i, obj in enumerate(jsonObjs):
        # print('{}/17517,  {}%'.format(i, i/17517))
        id_ = obj['data']['info']['id']
        mlist: list = obj['data']['list']

        for season in mlist:
            num: str = season['season_num']
            cn: str = season['season_cn']
            items: dict = season['items']
            mformat: list = season['formats']
            formats: str = ','.join(mformat)
            sql_season = insert_season.format(
                str(id_), num, cn, len(items), formats)
            s.write(sql_season)
            for f in mformat:
                for item in items[f]:
                    itemId = item['itemid']
                    episode = item['episode']
                    name = item['name']
                    size = item['size']
                    yyets = item['yyets_trans']
                    dateline = item['dateline']
                    if item['files'] != None:
                        for i, mfile in enumerate(item['files']):
                            way = mfile['way']
                            way_cn = mfile['way_cn']
                            address = mfile['address']
                            password = mfile['passwd']
                            sql_episode = insert_episode.format(str(id_), num, episode, f, itemId,
                                                                name, size, yyets, dateline, way, way_cn, address, password)
                            e.write(sql_episode)
