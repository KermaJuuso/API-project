#First time testing out Riots API

from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("API_KEY")
puuid = os.getenv("MY_PUUID")
api_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
api_url = api_url + puuid + '?api_key=' + api_key

resp_player_info = requests.get(api_url)
# Player info including different id's and other info
player_info = resp_player_info.json()
# Player level
player_account_level = player_info['summonerLevel']

#------------------------------------------------------------------------------

# Get past 20 played games by puuid
url_matches = (f"https://europe.api.riotgames.com/lol/match/v5/matches/"
               f"by-puuid/{puuid}/ids?start=0&count=20")
#Get the data
api_matches = url_matches + "&api_key=" + api_key
resp_matches = requests.get(api_matches)
match_ids = resp_matches.json()

game_api_url = (f"https://europe.api.riotgames.com/lol/match/v5/matches/"
                 f"{match_ids[0]}?api_key={api_key}")

game_resp = requests.get(game_api_url)
game_data = game_resp.json()

print(game_data['info']['participants'][5]['championName'])