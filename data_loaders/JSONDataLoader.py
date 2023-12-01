# data_loaders/JSONDataLoader.py
from DataLoader import DataLoader

class JSONDataLoader(DataLoader):
    def __init__(self, team_ids: list, api=None):
        super().__init__(team_ids, api)

    def get_team_stats(self):
        return self.team_stats
    
    def get_team_fixtures(self):
        return self.team_fixtures
    
    def get_fixture_lineups(self):
        return self.fixture_lineups
    
    def get_fixture_stats(self):
        return self.fixture_stats
    
    def get_players(self):
        return self.players
    
    def get_players_ids(self):
        return self.players_ids
    
    def get_injuries(self):
        return self.player_injuries
    
    def get_transfers(self):
        return self.transfers
    
    def get_coaches(self):
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
        teams = []
        for team_id in self.team_ids:
            for i in self.teams_stats.items():
                id = i[0]
                i = i[1]
                if id == str(team_id):
                    del i['team']['logo']
                    del i['league']
                    teams.append(i)
        return teams
    
    def get_team_players(self):
        teams = []
        for team_id in self.team_ids:
            team_player = {}
            for i in self.players:
                if len(i['statistics']) == 1:
                    if i['statistics'][0]['team']['id'] == team_id:
                        try:
                            del i['player']['photo']
                            del i['player']['name']
                            del i['statistics'][0]['team']['logo']
                            del i['statistics'][0]['league']['logo']
                            del i['statistics'][0]['league']['flag']
                            del i['statistics'][0]['league']['id']
                            del i['statistics'][0]['league']['name']
                        except:
                            pass
                        flat_data = {}
                        for key, value in i["statistics"][0].items():
                            if isinstance(value, dict):
                                for subkey, subvalue in value.items():
                                    flat_data[subkey] = subvalue
                            else:
                                flat_data[key] = value
                        #flat_data = {k: v for k, v in flat_data.items() if v is not None}
                        i['player']['statistics'] = flat_data
                        team_player[i['player']['id']] = i['player']
                        del team_player[i['player']['id']]['id']
                else:
                    for n in range(len(i['statistics'])):
                        if i['statistics'][n]['team']['id'] == team_id:
                            try:
                                del i['player']['photo']
                                del i['player']['name']
                                del i['statistics'][n]['team']['logo']
                                del i['statistics'][n]['league']['logo']
                                del i['statistics'][n]['league']['flag']
                                del i['statistics'][n]['league']['id']                                
                                del i['statistics'][0]['league']['name']
                            except:
                                pass
                            team_player[i['player']['id']] = i['player']
                            #team_player[i['player']['id']] = {k: v for k, v in team_player[i['player']['id']].items() if v is not None}
            teams.append(team_player)
        return teams
    
   #def get_player_injuries(self):
        teams = []
        for team_id in self.team_ids:
            injured_player = {}
            for i in self.injuries:    
                if i['team']['id'] == team_id:
                    if injured_player.get(i['player']['id']) is not None:
                        if injured_player[i['player']['id']]['injured_since'] > i['fixture']['date']:
                            injured_player[i['player']['id']]['injured_since'] = i['fixture']['date'].split('T')[0]
                        elif (injured_player[i['player']['id']]['injured_until'] < i['fixture']['date']) and (injured_player[i['player']['id']]['injured_until'] != ''):
                            injured_player[i['player']['id']]['injured_until'] = i['fixture']['date'].split('T')[0]
                    else: 
                        player_dict = {}
                        player_dict['injury_type'] = i['player']['type']
                        player_dict['injury_reason'] = i['player']['reason']
                        player_dict['injured_since'] = i['fixture']['date'].split('T')[0]
                        player_dict['injured_until'] = i['fixture']['date'].split('T')[0]
                        injured_player[i['player']['id']] = player_dict
            teams.append(injured_player)
        return teams
    
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
        head_to_head = {}
        for i in self.fixtures:
            if ((i['teams']['home']['id'] == self.team_ids[0]) and (i['teams']['away']['id'] == self.team_ids[1])) or ((i['teams']['home']['id'] == self.team_ids[1]) and (i['teams']['away']['id'] == self.team_ids[0])):
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
                i['fixture']['status'] = i['fixture']['status']['long']
                i['fixture']['venue'] = i['fixture']['venue']['name']
                fixture_dict[i['fixture']['id']] = {**i['teams'], **i['fixture']}
                head_to_head.update(fixture_dict)
        return head_to_head
    
    def get_fixture_stats(self):
        fixture_stats = {}
        for i in self.fixture_stats.items():
            fixture_id = i[0]
            i = i[1]            
        return i
    
    def get_player_news(self):
        return self.player_news
    
    def get_team_information(self):
        pass

    def get_venue_information(self):
        pass