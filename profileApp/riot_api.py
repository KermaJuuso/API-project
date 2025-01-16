from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_puuid(region, gameName, tagLine):
    """
    Return the puuid of player. Puuid is used to get
    the stats of the player.
    :param region: str, EUROPE, AMERICAS, ASIA, ESPORTS
    :param gameName:str, ingame name of player
    :param tagLine:str, 3-5 letters
    :return: str, puuid
    """
    api_url = (f"https://{region}.api.riotgames.com/riot/"
               f"account/v1/accounts/by-riot-id/{gameName}/{tagLine}")
    api_url = api_url + '?api_key=' + API_KEY

    response = requests.get(api_url)
    if response.status_code == 200:
        info = response.json()
        return info['puuid']
    else:
        raise Exception(f"Error: {response.status_code}, {response.json()}")


def get_summoner_info():
    """
    This functions purpose is to fetch, summoner level and icon
    SUMMONER-V4
    :return:
    """
    return


def get_match_history():
    """
    This function fetches match information
    MATCH-V5
    :return:
    """
    return


def get_champion_mastery():
    """
    This function fetches mastery of players top played champions-
    CHAMPION-MASTERY-V4
    :return:
    """
    return


def is_in_game_currently():
    """
    Get CurrentGameInfo
    SPECTATOR-V5
    :return:
    """
    return

def get_player_stats(region, gameName, tagLine):
    return
