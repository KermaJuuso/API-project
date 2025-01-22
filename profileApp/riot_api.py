from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")

#Remove this later
PUUID = os.getenv("MY_PUUID")


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
    if response.status_code == 200:
        info = response.json()
        puuid = info['puuid']
        name = info['gameName']
        tag_line = info['tagLine']
        return puuid
    else:
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
    info = response.json()
    profile_icon = info['profileIconId']
    summoner_level = info['summonerLevel']

    return {
        "profileIconId": profile_icon,
        "summonerLevel": summoner_level,
    }


def get_matches(region, puuid):
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

    match_obj_list = []
    for match in ids:
        #Get match data
        api_url = (f"https://{region}.api.riotgames.com/lol/match/v5/matches/"
                   f"{match}?api_key={API_KEY}")

        response = requests.get(api_url)
        data = response.json()
        match_obj = MatchData(data['metadata'], data['info'], puuid)
        match_obj_list.append(match_obj)

    return match_obj_list


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


def get_match_history(region, puuid):
    match_obj_list = get_matches(region, puuid)

    #Turn the matches into dict for html
    matches_frontend = [
        {"win": match.did_i_win, "champion": match.get_champion}
        for match in match_obj_list
    ]

    return matches_frontend


