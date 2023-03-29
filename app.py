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
 

schedule.every().minute.do(update_players_data)


while True:
    schedule.run_pending()
    time.sleep(1)
