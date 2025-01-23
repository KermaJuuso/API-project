from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()
API_KEY = os.getenv("API_KEY")

#Remove this later
PUUID = os.getenv("MY_PUUID")

USER_MATCH_DATA = []

class MatchData:
    def __init__(self, metadata, info, puuid):
        self.metadata = metadata
        self.info = info

        # Find all the user-specific data
        self.my_id = puuid
        self.my_index = self.metadata['participants'].index(self.my_id)
        self.my_data = info['participants'][self.my_index]

    @property
    def did_i_win(self):
        return self.my_data['win']

    @property
    def get_champion(self):
        return self.my_data['championName']



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


    USER_MATCH_DATA.clear()
    for match in ids:

        #Get match data
        api_url = (f"https://{region}.api.riotgames.com/lol/match/v5/matches/"
                   f"{match}?api_key={API_KEY}")

        response_data = requests.get(api_url)
        #If api request rate limit exceeds wait
        if response_data.status_code == 200:
            data = response_data.json()
            match_obj = MatchData(data['metadata'], data['info'], puuid)
            USER_MATCH_DATA.append(match_obj)

        elif response_data.status_code == 429:
            print("sleeping")
            time.sleep(10)

        else:
            print("init_match_history")
            raise Exception(
                f"Error: {response_data.status_code}, {response.json()}")


def get_match_data():

    #Turn the matches into dict for html
    matches_frontend = [
        {"win": match.did_i_win, "champion": match.get_champion}
        for match in USER_MATCH_DATA
    ]

    return matches_frontend


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


def get_region(server):
    if server == 'EUW1' or 'EUN1':
        return 'EUROPE'
    else:
        return 'AMERICAS'
