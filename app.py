import time
import requests
import schedule
import soccerdata as sd
from yarl import URL
from pprint import pprint
import math

from loguru import logger

import settings

fbref = sd.FBref(leagues=['ENG-Premier League'], seasons='22-23')

url = URL(settings.BASE_API_URL) / 'api' / 'player'

def save_data():
    all_players = {}

    first_save(all_players)

    for player in all_players:



        save_stat_type('possession', all_players)
        save_stat_type('playing_time', all_players)
        save_stat_type('passing', all_players)
        save_stat_type('passing_types', all_players)
        
        if all_players[player]['pos'] == 'GK':
            save_stat_type('keeper', all_players)
            save_stat_type('keeper_adv', all_players)

        elif all_players[player]['pos'] == 'DF':
            save_stat_type('misc', all_players)
            save_stat_type('defense', all_players)

        elif all_players[player]['pos'] == 'MF':
            save_stat_type('misc', all_players)
            save_stat_type('shooting', all_players)
            save_stat_type('defense', all_players)
            save_stat_type('goal_shot_creation', all_players)

        elif all_players[player]['pos'] == 'FW':
            save_stat_type('shooting', all_players)
            save_stat_type('goal_shot_creation', all_players)

        
        # if player['pos'] == 'GK':
        #     requests.post(str(url / 'GK'), json=player)

    pprint(all_players)
    # for player in all_players:
    #     requests.post(str(url / player['pos']), json=player)
        

def first_save(all_players):
    stats = fbref.read_player_season_stats(stat_type='standard')
    players = stats.to_dict(orient='index')

    for key, value in players.items():
        player = {}

        player['name'] = key[3]
        player['team'] = key[2]
        if float(value[('Playing Time', '90s')]) > 0.5:
            for j, k in value.items():
                player[('_'.join(' '.join(j).split()).lower().replace('%', '_percent').replace('+/-', '_plus_minus_').replace('/', '_in_').replace('+', '_plus_').replace('-', '_minus_'). replace('(', '').replace(')', '').replace(':', '_').replace('#', '_'))] = k
            edit_player(player)
            all_players[player['name']] = player


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
            if isinstance(k, float) and math.isnan(k):
                player[j] = 0.0 
            
        del player['pos']
        del player['age']
        del player['born']
        del player['nation']

        criterion = 'on90s'
        if stat_type == 'playing_time' or stat_type == 'keeper':
            criterion = 'playing_time_90s'

        if float(player[criterion]) > 0.5:
            all_players[name].update(player)
        


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
'''
schedule.every().minute.do(save_data)


while True:
    schedule.run_pending()
    time.sleep(1)
'''