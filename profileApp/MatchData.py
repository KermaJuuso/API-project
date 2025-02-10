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