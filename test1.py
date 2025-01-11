#First time testing out Riots API

from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("API_KEY")
puuid = os.getenv("MY_PUUID")
api_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
api_url = api_url + puuid + '?api_key=' + api_key

resp = requests.get(api_url)
player_info = resp.json()

player_account_level = player_info['summonerLevel']
print(player_account_level)