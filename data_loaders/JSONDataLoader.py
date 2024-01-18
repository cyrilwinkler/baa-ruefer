# data_loaders/JSONDataLoader.py
import sys
sys.path.append('/Users/tschip/workspace/baa/baa-ruefer/')
from data_loaders.DataLoader import DataLoader

class JSONDataLoader(DataLoader):
    """
    JSONDataLoader class for loading data from APIs or JSON files.

    This class extends the base DataLoader class and is specifically designed to load data and return it as a dictionary.

    Parameters:
    - team_ids (list): A list of the two team IDs for which data should be loaded.
    - api (optional): An optional parameter representing the API connection.
                     If provided, the loader will use this API for data retrieval.
                     If not provided, the loader will load the data from locally stored JSON files.
    """

    def __init__(self, team_ids: list, api=None):
        super().__init__(team_ids, api)
    
    def get_todays_fixture_id(self):
        """
        Returns the ID of today's fixture.
        """
        return self.todays_fixture_id
    
    def get_home_team_id(self):
        """
        Returns the ID of the home team.
        """
        return self.home_team_id
    
    def get_news_ids(self):
        """
        Returns a list containing the IDs of all news articles.
        """
        return self.news_ids
    
    def get_news_details(self):
        """
        Returns a dictionary containing the details of all news articles.
        """
        return self.news_details
    
    def get_team_information(self):
        """
        Returns a dictionary containing information about all teams.
        The dictionary is organized by team ID and returns a flatten dictionary for each team.
        """
        team_information = self.team_information.copy()
        team_dict = {}
        for i in team_information.items():
            i = i[1]#[0]
            team_dict[i['team']['id']] = self.flatten_dict(i['team'])
            del team_dict[i['team']['id']]['id']
            del team_dict[i['team']['id']]['logo']
            del team_dict[i['team']['id']]['national']

        return team_dict
    
    def get_team_statistics(self):
        """
        Returns a dictionary containing statistics for both teams.
        The dictionary is organized by team ID and returns a flatten dictionary for each team.
        """
        teams = {}
        for team_id in self.team_ids:            
            for i in self.team_stats.items():
                id = i[0]
                i = i[1]
                if id == str(team_id):
                    del i['team']['logo']
                    del i['league']
                    teams[team_id] = self.flatten_dict(i)
                    del teams[team_id]['team_id']
        return teams
    
    def get_team_news(self):
        """
        Returns a dictionary containing news articles for each team.
        """
        return self.team_news

    def get_team_fixtures(self):
        """
        Returns a dictionary containing fixtures for each team, where each fixture is represented by its unique ID.
        First the dictionary is flattened, such that each fixture is represented by a single dictionary. 
        Then, unnecessary information is removed from the dictionary.
        
        Returns:
        - fixture_dict (dict): A dictionary containing fixtures for each team, where each fixture is represented by its unique ID.

        Example:
        {
            "team_id_1": {
                "111111": {
                    "information_1": "value_1",
                    "information_2": "value_2",
                    ...
                },
                "222222": {
                    "information_1": "value_1",
                    "information_2": "value_2",
                    ...
                }
            },
            "team_id_1": {
            ...
            }
        }
        """
        fixture_dict = {}
        for id in self.team_fixtures:
            fixture_dict[id] = {}
            for fixture in self.team_fixtures[id]:
                fixture_dict[id][fixture['fixture']['id']] = self.flatten_dict(fixture)
                try:
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_timezone']
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_timestamp']
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_periods_first']
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_periods_second']
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_venue_id']
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_status_long']
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_status_short']
                    del fixture_dict[id][fixture['fixture']['id']]['fixture_status_elapsed']
                    del fixture_dict[id][fixture['fixture']['id']]['league_id']
                    del fixture_dict[id][fixture['fixture']['id']]['league_name']
                    del fixture_dict[id][fixture['fixture']['id']]['league_country']
                    del fixture_dict[id][fixture['fixture']['id']]['league_logo']
                    del fixture_dict[id][fixture['fixture']['id']]['league_flag']
                    del fixture_dict[id][fixture['fixture']['id']]['league_season']
                    del fixture_dict[id][fixture['fixture']['id']]['teams_home_id']
                    del fixture_dict[id][fixture['fixture']['id']]['teams_home_logo']
                    del fixture_dict[id][fixture['fixture']['id']]['teams_away_id']
                    del fixture_dict[id][fixture['fixture']['id']]['teams_away_logo']
                except:
                    pass
                
        return fixture_dict

    def get_fixture_lineup(self):
        """
        Returns a dictionary containing the lineup for each team, where each lineup is represented by its unique ID.
        """
        return self.fixture_lineups
    
    def get_fixture_stats(self):
        """
        Retrieves statistics for today's fixture.
        A dictionary containing fixture statistics for each team participating in today's fixture.
        The statistics are organized by team ID and include team statistics. 
        The statistics are flattened, such that each team is represented by a single dictionary.
        Unnecessary details like team logo and team ID are excluded.

        Returns:
        - fixture_stat (dict): A dictionary containing fixture statistics for each team participating in today's fixture.
        """
        fixture_id = self.get_todays_fixture_id()
        q = self.fixture_stats[str(fixture_id)]
        fixture_stat = {}
        for team_id in q:
            fixture_stat[team_id] = {}
            for i in q[team_id]:
                i = self.flatten_dict(i)
                del i['team_logo']
                del i['team_id']
                for j in i:
                    if j == 'statistics':
                        for k in  i[j]:
                            fixture_stat[team_id][k['type']] = k['value']
                    else:
                        fixture_stat[team_id][j] = i[j]
        return fixture_stat
    
    def get_players_ids(self):
        """
        Returns a list containing the IDs of all players in the lineup.
        """
        return self.players_ids
            
    def get_players(self):
        """
        Returns a dictionary containing information about all players in the lineup.
        The dictionary is organized by team ID and has a list with dictionaries for each player.
        """
        return self.players
    
    def get_player_names(self):
        """
        Returns a dictionary containing the names of all players in the lineup.
        The dictionary is organized by team ID. Each team has a dictionary with player IDs as key and the name as value.
        """
        players_names = {}
        for team_id in self.team_ids:
            players_names[team_id] = {}
            for player in self.players[str(team_id)]:
                    players_names[team_id][player['player']['id']] = player['player']['lastname'] if player['player']['lastname'] != None else player['player']['name']
        return players_names
    
    def get_player_information(self):
        """
        Returns a dictionary containing information about all players in the lineup.
        """
        player_dict = {}
        for id in self.players:
            player_dict[id] = {}
            for player in self.players[id]:
                player_dict[id][player['player']['id']] = self.flatten_dict(player['player'])
                del player_dict[id][player['player']['id']]['id']
                del player_dict[id][player['player']['id']]['photo']
        return player_dict
    
    def get_player_statistics(self):
        """
        Returns a dictionary containing statistics for all players in the lineup.
        """
        player_dict = {}
        for id in self.players:
            player_dict[id] = {}
            for player in self.players[id]:
                player_dict[id][player['player']['id']] = self.flatten_dict(player['statistics'][0])
                del player_dict[id][player['player']['id']]['team_id']
                del player_dict[id][player['player']['id']]['team_name']
                del player_dict[id][player['player']['id']]['team_logo']
                del player_dict[id][player['player']['id']]['league_id']
                del player_dict[id][player['player']['id']]['league_name']
                del player_dict[id][player['player']['id']]['league_country']
                del player_dict[id][player['player']['id']]['league_logo']
                del player_dict[id][player['player']['id']]['league_flag']
                del player_dict[id][player['player']['id']]['league_season']

        return player_dict
    
    def get_player_injuries(self):
        """
        Returns a dictionary containing injuries for all players in the lineup.
        """
        injuries_dict = {}
        for team_id in self.player_injuries:
            injuries_dict[team_id] = {}
            for injuries in self.player_injuries[team_id]:
                injuries_dict[team_id][injuries['player']['id']] = injuries['player']
                injuries_dict[team_id][injuries['player']['id']]['injury_type'] = injuries_dict[team_id][injuries['player']['id']]['type']
                injuries_dict[team_id][injuries['player']['id']]['injury_reason'] = injuries_dict[team_id][injuries['player']['id']]['reason']
                injuries_dict[team_id][injuries['player']['id']]['fixture_id'] = injuries['fixture']['id']
                del injuries_dict[team_id][injuries['player']['id']]['name']
                del injuries_dict[team_id][injuries['player']['id']]['type']
                del injuries_dict[team_id][injuries['player']['id']]['reason']
                del injuries_dict[team_id][injuries['player']['id']]['photo']
                del injuries_dict[team_id][injuries['player']['id']]['id']
        return injuries_dict
    
    def get_player_news(self):
        """
        Returns a dictionary containing news articles for all players in the lineup.
        """
        return self.player_news
    
    def get_player_transfers(self):
        """
        Returns a dictionary containing transfers for all players in the lineup.
        """
        transfer_dict = {}
        for player_id in self.transfers:
            transfer_dict[player_id] = []
            if self.transfers[player_id] != []:
                for transfer in self.transfers[player_id][0]['transfers']:
                    transfer = self.flatten_dict(transfer)
                    transfer['transfer_type'] = transfer['type']
                    del transfer['type']
                    del transfer['teams_in_logo']
                    del transfer['teams_out_id']
                    del transfer['teams_in_id']
                    del transfer['teams_out_logo']
                    transfer_dict[player_id].append(transfer)
            else:
                transfer_dict[player_id] = 'No transfers'
        return transfer_dict
    
    def get_transfer_rumours(self):
        """
        Returns a dictionary containing transfer rumours for all players in the lineup.
        """
        return self.transfer_rumours
    
    def get_coaches(self):
        """
        Returns a dictionary containing information about both coaches.
        """
        for i in self.coaches:
            self.coaches[i] = self.flatten_dict(self.coaches[i][0])
            try:
                del self.coaches[i]['team_logo']
                del self.coaches[i]['team_id']
                del self.coaches[i]['team_name']
                del self.coaches[i]['photo']
            except:
                pass
            for j in self.coaches[i]:
                if j == 'career':
                    for id in range(len(self.coaches[i][j])):
                        self.coaches[i][j][id] = self.flatten_dict(self.coaches[i][j][id])
                        try:
                            del self.coaches[i][j][id]['team_logo']
                            del self.coaches[i][j][id]['team_id']
                        except:
                            pass
        return self.coaches
    
    def get_head_to_head(self):
        """
        Returns a dictionary containing the head-to-head data of the teams.
        """
        head_to_head_dict = {}
        for id in self.team_fixtures:
            for fixture in self.team_fixtures[id]:
                if ((fixture['teams']['home']['id'] == self.team_ids[0]) and (fixture['teams']['away']['id'] == self.team_ids[1])) or ((fixture['teams']['home']['id'] == self.team_ids[1]) and (fixture['teams']['away']['id'] == self.team_ids[0])):
                    fixture_dict = {}
                    try:
                        del fixture['teams']['home']['logo']
                        del fixture['teams']['away']['logo']
                        del fixture['fixture']['timezone']
                        del fixture['fixture']['timestamp']
                        del fixture['fixture']['periods']
                    except:
                        pass
                    fixture['fixture']['date'] = fixture['fixture']['date'].split('T')[0]
                    fixture['fixture']['game_duration'] = fixture['fixture']['status']['elapsed']
                    fixture['fixture']['status'] = fixture['fixture']['status']['long']
                    fixture['fixture']['venue'] = fixture['fixture']['venue']['name']
                    fixture_dict[fixture['fixture']['id']] = {**fixture['teams'], **fixture['fixture']}
                    head_to_head_dict.update(fixture_dict)

        head_to_head = {}
        for i in head_to_head_dict:
            head_to_head[i] = self.flatten_dict(head_to_head_dict[i])
            del head_to_head[i]['id']

        return head_to_head
    
    def get_venue_information(self):
        """
        Returns a dictionary containing information about the venue of the fixture.
        """
        venue_information = self.team_information
        venue_dict = {}
        for i in venue_information.items():
            i = i[1]#[0]
            venue_dict[i['venue']['id']] = self.flatten_dict(i['venue'])
            venue_dict[i['venue']['id']]['team_id'] = i['team']['id']
            del venue_dict[i['venue']['id']]['id']
            del venue_dict[i['venue']['id']]['image']

        return venue_dict

    def flatten_dict(self, d, parent_key='', sep='_'):
        """
        Recursively flattens a nested dictionary.

        Args:
        d (dict): The dictionary to be flattened.
        parent_key (str, optional): The prefix to be added to each key. Default is an empty string.
        sep (str, optional): The separator used between parent and child keys. Default is underscore '_'.

        Returns:
        dict: A flattened dictionary where keys are composed of parent and child keys separated by the specified separator.

        Example:
        For the input dictionary {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}, calling flatten_dict would return:
        {'a': 1, 'b_c': 2, 'b_d_e': 3}
        """
        flattened = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                flattened.update(self.flatten_dict(v, new_key, sep=sep))
            else:
                flattened[new_key] = v
        return flattened