#First time testing out Riots API
#Following guide by iTero Gaming on Youtube
#This is just meant to be a testing file and for reference
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()
api_key = os.getenv("API_KEY")
puuid = os.getenv("MY_PUUID")

#part 1------------------------------------------------------------------------
"""
api_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
api_url = api_url + puuid + '?api_key=' + api_key

resp_player_info = requests.get(api_url)
# Player info including different id's and other info
player_info = resp_player_info.json()
# Player level
player_account_level = player_info['summonerLevel']
"""


#Part 2------------------------------------------------------------------------
# Get past 20 played games by puuid
url_matches = (f"https://europe.api.riotgames.com/lol/match/v5/matches/"
               f"by-puuid/{puuid}/ids?start=0&count=20")
#Get the data
api_matches = url_matches + "&api_key=" + api_key
resp_matches = requests.get(api_matches)

#Id's of last 20 games here
match_ids = resp_matches.json()
"""
# Get data from last game played
game_api_url = (f"https://europe.api.riotgames.com/lol/match/v5/matches/"
                 f"{match_ids[0]}?api_key={api_key}")

game_resp = requests.get(game_api_url)
game_data = game_resp.json()

print(game_data['info']['participants'][0]['championName'])
"""


#Part 3------------------------------------------------------------------------
# Get MY player info with indexing from my latest game.
"""
my_index = game_data['metadata']['participants'].index(puuid)

kills = game_data['info']['participants'][my_index]['kills']
deaths = game_data['info']['participants'][my_index]['deaths']
assists = game_data['info']['participants'][my_index]['assists']

kda = (kills + assists)/deaths
print(kda)
"""


#Part 4 creating a loop--------------------------------------------------------
def did_win(puuid, match_data):
    """
    Check if player won, by puuid
    :param puuid:string,  wanted players id
    :param match_data: json
    :return: Bool
    """
    #same as in part 3
    part_index = match_data['metadata']['participants'].index(puuid)
    return match_data['info']['participants'][part_index]['win']


def get_match_data(region, match_id):
    api_url = (
        "https://" +
        region +
        ".api.riotgames.com/lol/match/v5/matches/" +
        match_id +
        "?api_key=" +
        api_key
    )
    while True:
        resp = requests.get(api_url)

        if resp.status_code == 429:
            print("Too mane requests, 429")
            time.sleep(10)
            continue

        data = resp.json()
        return data

# Lets say I want to know if I won the latest game I played
region = "europe"

#loop through last 20 games and print wins and losses
"""for match in match_ids:
    data = get_match_data(region, match)
    print(did_win(puuid, data))"""


#Part 5------------------------------------------------------------------------

def get_matches(region, id, count, api_key):
    api_url = (
        "https://" +
        region +
        ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        id +
        "/ids" +
        "?type=ranked&" +
        "start=0&" +
        "count=" +
        str(count) +
        "&api_key=" +
        api_key
    )

    resp = requests.get(api_url)
    return resp.json()

matches = get_matches(region, puuid, 100, api_key)




















