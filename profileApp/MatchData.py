
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
    
    @property
    def get_game_mode(self):
        return self.info['gameMode']
    
    @property
    def get_game_duration(self):
        return self.info['gameDuration']
    

    @property
    def get_team_summary(self):
        summary = []

        for team in self.info['teams']:
            #Get game result for game
            team_win = 'Victory' if team['win'] else 'Defeat'

            # Either 100 or 200, 100 = blue side and 200 = red side
            team_id = team['teamId']

            # 5 champion id's for a team
            bans = [ban['championId'] for ban in team['bans']]

            summary.append(
                {
                    'team': team_id,
                    'bans': bans,
                    'win': team_win
                }
            )
        return summary
    

    @property
    def get_match_overview(self):
        overview = []
        
        for participant in self.info['participants']:
            profile_icon_png = f"{participant['profileIcon']}.png"
            overview.append(
                {'name': participant['riotIdGameName'],
                 'tag': participant['riotIdTagline'],
                 'champion': participant['championName'],
                 'position': participant['teamPosition'],
                 'cs': participant['totalMinionsKilled'],
                 'kills': participant['kills'],
                 'deaths': participant['deaths'],
                 'assists': participant['assists'],
                 'profileIcon': profile_icon_png
                 }
            )
        
        return overview
