import soccerdata as sd
import requests
import settings
from yarl import URL

import schedule
import time

fbref = sd.FBref(leagues=['ENG-Premier League'], seasons='22-23')

stats = fbref.read_player_season_stats(stat_type='standard')
url = URL(settings.BASE_API_URL)

def request_post():
    r = requests.post(str(url), json=stats.to_json())

schedule.every().hour.do(request_post())