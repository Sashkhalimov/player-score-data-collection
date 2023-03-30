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

        if int(value[('Playing Time', 'MP')]) > 3:
            for j, k in value.items():
                player[('_'.join(' '.join(j).split()).lower().replace('%', '_percent').replace('+/-', '_plus_minus_').replace('/', '_in_').replace('+', '_plus_').replace('-', '_minus_'). replace('(', '').replace(')', '').replace(':', '_').replace('#', '_'))] = k
            edit_player(player)
            all_players.append(player)

    save_stat_type('possession', all_players)
    save_stat_type('playing_time', all_players)
    save_stat_type('passing', all_players)
    save_stat_type('passing_types', all_players)
    save_stat_type('goal_shot_creation', all_players)

    if player['pos'] == 'GK':
        save_stat_type('keeper', all_players)
        save_stat_type('keeper_adv', all_players)
    elif player['pos'] == 'DF':
        save_stat_type('misc', all_players)
        save_stat_type('defense', all_players)
    elif player['pos'] == 'MF':
        save_stat_type('misc', all_players)
        save_stat_type('shooting', all_players)
        save_stat_type('defense', all_players)
    elif player['pos'] == 'FW':
        save_stat_type('shooting', all_players)
    pprint(all_players)



def save_stat_type(stat_type, all_players):
    stats = fbref.read_player_season_stats(stat_type=stat_type)
    players = stats.to_dict(orient='index')

    for key, value in players.items():
        name = key[3]
        player = {}
        for j, k in value.items():
            j = '_'.join(' '.join(j).split()).lower().replace('%', '_percent').replace('+/-', '_plus_minus_').replace('/', '_in_').replace('+', '_plus_').replace('-', '_minus_').replace('(', '').replace(')', '').replace(':', '_').replace('#', '_')
            if j[0].isdigit():
                player['on' + j] = k
            else:
                player[j] = k
        del player['pos']
        del player['age']
        del player['born']
        del player['nation']

        for human in all_players:
            if human['name'] == name:
                human.update(player)

def edit_player(player):
    del player['born']
    player['age'] = player.pop('age')[:2]

    if len(player['pos']) == 2:
        player['pos'] = player.pop('pos')[:2]
    else:
        if 'FW' in player['pos']:
            player['pos'] = 'FW'
        else:
            player['pos'] = player.pop('pos')[:2]


save_data()

schedule.every().minute.do(update_players_data)


while True:
    schedule.run_pending()
    time.sleep(1)
