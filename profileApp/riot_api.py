from dotenv import load_dotenv
from MatchData import MatchData
from flask_caching import Cache
import os
import requests
import time
import json

load_dotenv()
API_KEY = os.getenv("API_KEY")

#Remove this later
PUUID = os.getenv("MY_PUUID")


def get_puuid(region, gameName, tagLine):
    """
    Return the puuid of player. Puuid is used to get
    the stats of the player.
    ACCOUNT-V1
    :param region: str, EUROPE, AMERICAS, ASIA, ESPORTS
    :param gameName:str, ingame name of player
    :param tagLine:str, 3-5 letters
    :return: dict
    """
    api_url = (f"https://{region}.api.riotgames.com/riot/"
               f"account/v1/accounts/by-riot-id/{gameName}/{tagLine}")
    api_url = api_url + '?api_key=' + API_KEY

    response = requests.get(api_url)
    print(response.status_code)
    if response.status_code == 200:
        info = response.json()
        puuid = info['puuid']
        return puuid
    else:
        print("get_puuid")
        raise Exception(f"Error: {response.status_code}, {response.json()}")


def get_summoner_info(server, puuid):
    """
    This functions purpose is to fetch, summoner level and icon
    SUMMONER-V4
    :return: dict
    """

    api_url = (f"https://{server}.api.riotgames.com/lol/summoner/v4/"
               f"summoners/by-puuid/{puuid}?api_key={API_KEY}")

    response = requests.get(api_url)
    print(response.status_code)

    if response.status_code == 200:
        info = response.json()
        profile_icon = info['profileIconId']
        summoner_level = info['summonerLevel']
        profile_icon_png = f"{profile_icon}.png"

        return {
            "profileIcon": profile_icon_png,
            "summonerLevel": summoner_level,
        }
    else:
        print("get_summoner_info")
        raise Exception(f"Error: {response.status_code}, {response.json()}")


def init_matchs_history(region, puuid):
    """
    Gets user's 20 most recent game IDs and turns them into MatchData objects.
    MATCH-V5
    :param region: str, region of the user
    :param puuid: str, players ID
    :return: list of MatchData objects for user match history.
    """
    #Get match ids
    api_url = (f"https://{region}.api.riotgames.com/lol/match/v5/matches/"
               f"by-puuid/{puuid}/ids?start=0&count=20&api_key={API_KEY}")

    response = requests.get(api_url)
    #Get list of game ids
    ids = response.json()

    match_history = []

    for match in ids:

        #Get match data
        api_url = (f"https://{region}.api.riotgames.com/lol/match/v5/matches/"
                   f"{match}?api_key={API_KEY}")

        response_data = requests.get(api_url)
        #If api request rate limit exceeds wait
        if response_data.status_code == 200:
            data = response_data.json()
            match_obj = MatchData(data['metadata'], data['info'], puuid)
            match_history.append(match_obj)

        elif response_data.status_code == 429:
            print("sleeping")
            time.sleep(10)

        else:
            print("init_match_history FAIL")
            raise Exception(
                f"Error: {response_data.status_code}, {response.json()}")
    
    
    return match_history


def get_match_preview(match_history):
    """
    Turns match data from MatchData objects to small dict for
    match history preview.
    :return: list
    """
    #Turn the matches into dict for html

    matches_frontend = []
    id = 0
    for match in match_history:
        champion = match.get_champion
        matches_frontend.append({
            "win": match.did_i_win,
            "champion": champion,
            "icon": f"{champion}.png",
            "id": id
        })
        id += 1

    return matches_frontend


def get_champion_mastery(puuid, server):
    """
    This function fetches mastery of players top 3 played champions
    CHAMPION-MASTERY-V4
    :param puuid: str, players ID
    :param server: str, server of the user
    :return: dict, containing top played champs, their levels and points
    """
    api_url = (f"https://{server}.api.riotgames.com/lol/champion-mastery/v4/"
               f"champion-masteries/by-puuid/{puuid}/top?count=3&api_key={API_KEY}")

    response = requests.get(api_url)
    top_list = []
    if response.status_code == 200:
        top_champs = response.json()
        for champion in top_champs:
            championName = champion_id_to_name(int(champion['championId']))
            top_list.append(
                {'id': championName,
                 'level': champion['championLevel'],
                 'points': champion['championPoints']}
            )
        return top_list
    else:
        print("get_champion_mastery")
        raise Exception(f"Error: {response.status_code}, {response.text}")


def is_in_game_currently():
    """
    Get CurrentGameInfo
    SPECTATOR-V5
    :return:
    """
    return


def get_region(server):
    if server == 'EUW1' or 'EUN1':
        return 'EUROPE'
    else:
        return 'AMERICAS'

#print(get_champion_mastery(PUUID, 'euw1'))


def champion_id_to_name(id):
    """
    Turns champion id to champion json.
    In future this can be used to access more champion information
    :param id: int, champion id
    :return:str, champion name
    """

    json_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'championData', 'champion.json')
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for champ_name, champ_data in data["data"].items():
        if champ_data["key"] == str(id):  
            return champ_name

    return "Unknown Champion"


def handle_match_data(match_data):
    return match_data.get_match_overview



#Testing
#--------------------------------------------------------------


    