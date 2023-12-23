# data_loaders/JSONDataLoader.py
import sys
sys.path.append('/Users/tschip/workspace/baa/baa-ruefer/')
#sys.path.append('/home/jovyan/baa-ruefer/')

from data_loaders.DataLoader import DataLoader

class JSONDataLoader(DataLoader):
    def __init__(self, team_ids: list, api=None):

        super().__init__(team_ids, api)
    
    def get_team_fixtures(self):
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

    def get_todays_fixture_id(self):
        return self.todays_fixture_id
    
    def get_fixture_lineup(self):
        return self.fixture_lineups
    
    def get_home_team_id(self):
        return self.home_team_id
    
    def get_fixture_stats(self):
        #return None
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
            
    
    def get_players(self):
        return self.players
    
    def get_players_ids(self):
        return self.players_ids
    
    def get_player_names(self):
        players_names = {}
        for team_id in self.team_ids:
            players_names[team_id] = {}
            for player in self.players[str(team_id)]:
                    players_names[team_id][player['player']['id']] = player['player']['lastname'] if player['player']['lastname'] != None else player['player']['name']
        return players_names
    
    def get_transfers(self):
        return self.transfers
    
    def get_coaches(self):
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
    
    def get_team_mapping(self):
        return self.team_mapping
    
    def get_transfer_rumours(self):
        return self.transfer_rumours
    
    def get_team_news(self):
        return self.team_news
    
    def get_player_news(self):
        return self.player_news
    
    def get_news_ids(self):
        return self.news_ids 
    
    def get_player_mapping(self):
        return self.player_mapping
    
    def get_news_details(self):
        return self.news_details

    def get_team_statistics(self):
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
    
    def get_player_information(self):
        player_dict = {}
        for id in self.players:
            player_dict[id] = {}
            for player in self.players[id]:
                player_dict[id][player['player']['id']] = self.flatten_dict(player['player'])
                del player_dict[id][player['player']['id']]['id']
                del player_dict[id][player['player']['id']]['photo']
        return player_dict

    def get_player_statistics(self):
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
    
    def get_player_transfers(self):
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
    
    def get_player_injuries(self):
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
    
    def get_all_team_fixtures(self):
        teams = []
        for team_id in self.team_ids:
            team_fixtures = {}
            for i in self.fixtures:
                if (i['teams']['home']['id'] == team_id) or (i['teams']['away']['id'] == team_id):
                    fixture_dict = {}
                    try:
                        del i['teams']['home']['logo']
                        del i['teams']['away']['logo']
                        del i['fixture']['timezone']
                        del i['fixture']['timestamp']
                        del i['fixture']['periods']
                    except:
                        pass                
                    i['fixture']['date'] = i['fixture']['date'].split('T')[0]
                    i['fixture']['game_duration'] = i['fixture']['status']['elapsed']
                    i['fixture']['game_status'] = i['fixture']['status']['long']
                    i['fixture']['venue_name'] = i['fixture']['venue']['name']
                    fixture_dict[i['fixture']['id']] = {**i['teams'], **i['fixture']}
                    
                    team_fixtures.update(fixture_dict)
            teams.append(team_fixtures)
        return teams
    
    def get_head_to_head(self):
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
    
    def get_team_information(self):
        team_information = self.team_information.copy()
        team_dict = {}
        for i in team_information.items():
            i = i[1]#[0]
            team_dict[i['team']['id']] = self.flatten_dict(i['team'])
            del team_dict[i['team']['id']]['id']
            del team_dict[i['team']['id']]['logo']
            del team_dict[i['team']['id']]['national']

        return team_dict

    def get_venue_information(self):
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
        flattened = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                flattened.update(self.flatten_dict(v, new_key, sep=sep))
            else:
                flattened[new_key] = v
        return flattened