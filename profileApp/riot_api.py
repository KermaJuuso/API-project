from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_puuid(region, gameName, tagLine):
    api_url = (f"https://{region}.api.riotgames.com/riot/"
               f"account/v1/accounts/by-riot-id/{gameName}/{tagLine}")
    api_url = api_url + '?api_key=' + API_KEY

    info = requests.get(api_url)
    info = info.json()
    print(info)

get_puuid("europe", "ukko2000", "EUW")