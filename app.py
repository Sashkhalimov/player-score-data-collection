import time
import requests
import schedule
import soccerdata as sd
from yarl import URL
from pprint import pprint

from loguru import logger

import settings

fbref = sd.FBref(leagues=['ENG-Premier League'], seasons='22-23')

url = URL(settings.BASE_API_URL) / 'api' / 'player'

def update_players_data():
    logger.debug('chto ugodno')
    stats = fbref.read_player_season_stats(stat_type='standard')
    r = requests.post(str(url), json=stats.to_json(orient='index'))


def save_data():
    all_players = []
    stats = fbref.read_player_season_stats(stat_type='standard')
    players = stats.to_dict(orient='index')
    for key, value in players.items():
        player = {}
        player['name'] = key[3]
        player['team'] = key[2]
        for j, k in value.items():
            player['_'.join(' '.join(j).split()).lower().replace('%', '_percent').replace('/', '_in_').replace('+', '_plus_').replace('-', '_minus_')] = k
        del player['born']
        player['age'] = player.pop('age')[:2]
        all_players.append(player)
    save_stat_type('possession', all_players)


def save_stat_type(stat_type, all_players):
    stats = fbref.read_player_season_stats(stat_type=stat_type)
    players = stats.to_dict(orient='index')
    for key, value in players.items():
        name = key[3]
        player = {}
        for j, k in value.items():
            if j[0][0].isdigit():
                player['n' + j[0]] = k
            else:
                player[('_'.join(' '.join(j).split()).lower().replace('%', '_percent').replace('/', '_in_').replace('+', '_plus_').replace('-', '_minus_'))] = k
        del player['pos']
        del player['age']
        del player['born']
        del player['nation']
        for human in all_players:
            if human['name'] == name:
                human.update(player)

        pprint(player)

save_data()

schedule.every().minute.do(update_players_data)


while True:
    schedule.run_pending()
    time.sleep(1)
