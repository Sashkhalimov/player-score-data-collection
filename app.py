import soccerdata as sd
from yarl import URL
import requests

import settings
from utils import format_stat_name, format_stat_value, get_playing_time, edit_position, update_result

fbref = sd.FBref(leagues=['ENG-Premier League'], seasons='22-23')

url = URL(settings.BASE_API_URL) / 'api' / 'player'

STAT_TYPES = {
    'all':[
    'standard', 
    'passing', 
    'passing_types', 
    'playing_time',
    'possession',
    ],
    'GK':[
    'keeper', 
    'keeper_adv',
    ],
    'DF':[
    'misc',
    'defense',
    ],
    'MF':[
    'misc',
    'defense',
    'shooting',
    'goal_shot_creation',
    ],
    'FW':[
    'goal_shot_creation', 
    'shooting', 
    ]
}

def get_players():
    result = {}

    for stat_type in STAT_TYPES['all']:
        stat_types_by_poisition(stat_type, result)

    for position in STAT_TYPES:
        for stat_type in STAT_TYPES[position]:
            stat_types_by_poisition(stat_type, result, position)

    return result


def stat_types_by_poisition(stat_type, result, position=None):
    stats = (fbref.read_player_season_stats(stat_type=stat_type)).to_dict(orient='index')
    for key, value in stats.items():
        if position is not None:
            if edit_position(value[('Pos', '')]) == position:
                update_result(key, value, result)
        else:
            update_result(key, value, result)


def format_players_data(players):
    result = []

    for player, player_stats in players.items():
        player = {'name':player[3], 'team':player[2]}

        playing_time = get_playing_time(player_stats)

        if playing_time <= 0.5:
            continue

        for stat_name, stat_value in player_stats.items():
            stat_name = format_stat_name(stat_name)
            stat_value = format_stat_value(stat_value)
            player[stat_name] = stat_value
        
        try:
            player['age'] = player['age'][:2]
        except Exception as e:
            print('Can be')

        player['pos'] = edit_position(player['pos'])
        if 'int' in player.keys():
            player['_int'] = player.pop('int')
        del player['born']

        result.append(player)

    return result
    

if __name__ == '__main__':
    players = get_players()
    players = format_players_data(players)
    for player in players:
        requests.post(str(url / player['pos']), json=player)


