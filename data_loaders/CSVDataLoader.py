# data_loaders/json_loader.py
import sys
#sys.path.append('/Users/tschip/workspace/baa/baa-ruefer/')
sys.path.append('/home/jovyan/baa-ruefer/')

from data_loaders.DataLoader import DataLoader
import pandas as pd

class CSVDataLoader(DataLoader):
    def __init__(self, team_ids: list, api=None):
        super().__init__(team_ids, api)


    def get_team_information(self):
        teams = []
        for team in self.team_information:
            teams.append(pd.DataFrame.from_dict(self.team_information[team]['team'], orient='index').T)

        return pd.concat(teams).drop(columns=['logo', 'national']).reset_index(drop=True)
    
    def get_venue_information(self):
        venues = []
        for team in self.team_information:
            venue = pd.DataFrame.from_dict(self.team_information[team]['venue'], orient='index').T
            venue['team_id'] = self.team_information[team]['team']['id']
            venues.append(venue)
        df = pd.concat(venues).drop(columns=['image']).reset_index(drop=True)
        
        return df[df.team_id == self.get_home_team_id()].drop(columns=['team_id']).reset_index(drop=True)
    
    def get_todays_fixture_id(self):
        return self.todays_fixture_id
    
    def get_fixture_lineup(self):
        return self.fixture_lineups

    def get_home_team_id(self):
        return self.home_team_id
    
    def get_players_ids(self):
        return self.players_ids
    
    def get_player_names(self):
        players_names = {}
        for team_id in self.team_ids:
            for player in self.players[str(team_id)]:
                    players_names[player['player']['id']] = player['player']['lastname'] if player['player']['lastname'] != None else player['player']['name']
            return pd.DataFrame.from_dict(players_names, orient='index').reset_index().rename(columns={'index': 'player_id', 0: 'player_name'})
    
    def get_player_information(self):
        players_information = []
        for id in self.players:
            for player in self.players[id]:
                flattened_data = self.flatten_dict(player['player'])
                flattened_data['team_id'] = id
                players_information.append(pd.DataFrame.from_dict(flattened_data, orient='index').T.drop(columns=['photo', 'name']))

        df = pd.concat(players_information).reset_index(drop=True)
        #df.rename(columns={'id': 'player_id'}, inplace=True)
        #transfers = self.get_player_transfers().sort_values(by=['date'], ascending=False).drop_duplicates(subset=['player_id'], keep='first')
        #df = df.merge(transfers, on='player_id', how='left')
        #df = df.merge(self.get_player_statistics(), on='player_id', how='left')
        return df
    
    def get_player_statistics(self):
        players_statistics = []
        for id in self.players:
            for player in self.players[id]:
                flattened_data = self.flatten_dict(player['statistics'][-1])
                flattened_data['player_id'] = player['player']['id']
                players_statistics.append(pd.DataFrame.from_dict(flattened_data, orient='index').T.drop(columns=['team_logo', 'league_logo', 'league_flag', 'league_id', 'league_name', 'league_country', 'team_name', 'games_number']))

        return pd.concat(players_statistics).reset_index(drop=True)
    
    def get_player_transfers(self):
        transfers_list = []
        for id in self.transfers:
            for transfer in self.transfers[id]:
                flatten_data = self.flatten_dict(transfer['transfers'][0])
                flatten_data['player_id'] = transfer['player']['id']
            transfers_list.append(pd.DataFrame.from_dict(flatten_data, orient='index').T.drop(columns=['teams_in_logo', 'teams_out_logo', 'teams_in_id', 'teams_out_id', 'teams_in_name']))

        return pd.concat(transfers_list).reset_index(drop=True)

    def get_team_statistics(self):
        return self.team_stats

    def get_team_players(self):
        # Implementation for getting team players from JSON data
        pass

    def get_player_injuries(self):########################################################################### 
        # Implementation for getting player injuries from JSON data
        injuries_list = []
        for id in self.player_injuries:
            for injury in self.player_injuries[id]:
                try:
                    del injury['league']
                    del injury['team']
                    del injury['player']['photo']
                    del injury['player']['name']
                    del injury['fixture']['timezone']
                    del injury['fixture']['timestamp']
                except:
                    pass
                injuries_list.append(pd.DataFrame.from_dict(self.flatten_dict(injury), orient='index').T)
        return pd.concat(injuries_list).reset_index(drop=True)

    def get_team_fixtures(self):
        return self.team_fixtures

    def get_head_to_head(self):
        # Implementation for getting head-to-head data from JSON data
        head_to_head = {}
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
                    head_to_head.update(fixture_dict)

        head_to_head_list = []
        for i in head_to_head:
            head_to_head_list.append(self.flatten_dict(head_to_head[i]))

        return pd.DataFrame(head_to_head_list).drop(columns=['venue', 'game_duration', 'status']).reset_index(drop=True)

    def get_fixture_stats(self):
        # Implementation for getting fixture stats from JSON data
        fixture_statistics = []

        for i in self.fixture_stats:
            # Flatten the JSON data
            flattened_data = self.flatten_dict(self.fixture_stats[i]['team'], 'team')
            print(self.fixture_stats[i])
            for x in self.fixture_stats[i]['statistics']:
                print(x)
                flattened_data.update({x['type']: x['value']})

            # Create a DataFrame
            fixture_statistics.append(pd.DataFrame.from_dict(flattened_data, orient='index').T.drop(columns=['team_logo']))

        return pd.concat(fixture_statistics).reset_index(drop=True)

    def get_player_news(self):
        # Implementation for getting player news from JSON data
        pass

    def get_team_news(self):
        # Implementation for getting player news from JSON data
        pass

    def flatten_dict(self, d, parent_key='', sep='_'):
        flattened = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                flattened.update(self.flatten_dict(v, new_key, sep=sep))
            else:
                flattened[new_key] = v
        return flattened