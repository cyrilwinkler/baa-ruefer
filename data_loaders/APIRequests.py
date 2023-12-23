import json
import requests
import time
from datetime import datetime

class APIRequests:
    def __init__(self, api_key, team_ids: list, season: int, league_id: int, fixture_date:str, max_requests=99):
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
        }
        self.headers_TM = {
            'x-rapidapi-key': api_key,
            "X-RapidAPI-Host": "transfermarket.p.rapidapi.com"
        }
        self.team_ids = team_ids
        self.season = str(season)
        self.league_id = str(league_id)
        self.fixture_date = datetime.strptime(fixture_date, '%d-%m-%Y').strftime('%d-%m-%Y')
        self.base_url_F = 'https://api-football-v1.p.rapidapi.com/v3/'
        self.base_url_TM = 'https://transfermarket.p.rapidapi.com/'
        self.league_id_TM = 'IT1'
        self.domain_TM = 'com'
        self.requests_limit = max_requests
        self.requests = 0

    def set_team_information(self):
        """Set team information for both teams in the league for the given season."""
        print('Request team information...')
        endpoint = 'teams'
        teams = {}
        
        for team_id in self.team_ids:
            params = {'id': str(team_id)}
            if self.requests <= self.requests_limit:
                teams[team_id] = self._fetch_data_F(endpoint=endpoint, params=params)
            else:
                print('Reached requests limit.')
        
        self.teams = teams

    def get_team_information(self):
        """Returns a dictionary with team_id as key and team information as value."""
        try:
            return self.teams
        except:
            self.set_team_information()
            return self.teams

    def set_team_statistics(self):
        """Set team statistics for both team in the league for the given season."""
        print('Request team statistics...')
        endpoint = 'teams/statistics'
        teams_stats = {}
        
        for team_id in self.team_ids:
            params = {'league': self.league_id, 'season': self.season, 'team': str(team_id)}
            if self.requests <= self.requests_limit:
                resp = self._fetch_data_F(endpoint=endpoint, params=params, optional=True)
                teams_stats[team_id] = resp
            else:
                print('Reached requests limit.')
        
        self.teams_stats = teams_stats

    def get_team_statistics(self):
        """Returns a dictionary with team_id as key and team statistics as value."""
        try:
            return self.teams_stats
        except:
            self.set_team_statistics()
            return self.teams_stats
    
    def set_fixtures(self):
        """Set fixtures for both teams in the league for the given season."""
        print('Request team fixtures...')
        endpoint = 'fixtures'
        fixtures = {}
        
        for team_id in self.team_ids:
            params = {'season': self.season, 'team': str(team_id), 'league': str(self.league_id)}
            if self.requests <= self.requests_limit:
                fixtures[team_id] = self._fetch_data_F(endpoint=endpoint, params=params)
            else:
                print('Reached requests limit.')
        
        self.fixtures = fixtures

    def get_fixtures(self):
        """Returns a dictionary with team_id as key and a list of fixtures as value."""
        try:
            return self.fixtures
        except:
            self.set_fixtures()
            return self.fixtures
        
    def get_home_team_id(self):
        team_id = list(self.get_fixtures().keys())[0]
        for i in self.get_fixtures()[team_id]: #[1:]
            fixture_lineup_date = datetime.utcfromtimestamp(int(i['fixture']['timestamp'])).strftime('%d-%m-%Y')
            if fixture_lineup_date == self.fixture_date:
                return i['teams']['home']['id']
        
    def set_fixture_lineup(self):
        """Set fixture lineup for both teams in the league for the given season."""
        endpoint = 'fixtures/lineups'
        fixture_lineup = {}
        
        team_id = list(self.get_fixtures().keys())[0]
        for i in self.get_fixtures()[team_id]: #[1:]
            fixture_lineup_date = datetime.utcfromtimestamp(int(i['fixture']['timestamp'])).strftime('%d-%m-%Y')
            if fixture_lineup_date == self.fixture_date:
                self.fixture_id = i['fixture']['id']
                params = {'fixture': str(self.fixture_id)}
                if self.requests <= self.requests_limit:
                    print('Request team fixture lineup...')
                    resp = self._fetch_data_F(endpoint=endpoint, params=params)
                    print(f'fixture_lineup: {resp}')
                    for idx in range(len(resp)):
                        if resp[idx]['team']['id'] == self.team_ids[0]:
                            fixture_lineup[self.team_ids[0]] = resp[idx]
                        elif resp[idx]['team']['id'] == self.team_ids[1]:
                            fixture_lineup[self.team_ids[1]] = resp[idx]
                else:
                    print('Reached requests limit.')

        self.fixture_lineup = fixture_lineup

    def get_fixture_lineup(self):
        """Returns a dictionary with team_id as key and fixture lineup as value."""
        try:
            return self.fixture_lineup
        except:
            self.set_fixture_lineup()
            return self.fixture_lineup
        
    def get_todays_fixture_id(self):
        try:
            return self.fixture_id
        except:
            self.get_fixture_lineup()
            return self.fixture_id
    
    def set_players(self):
        """Set all players for both teams in the league for the given season."""
        print('Request players...')
        players = {}
        endpoint = 'players'
        
        for team_id in self.team_ids:
            params = {'season': self.season, 'team': str(team_id)}
            if self.requests <= self.requests_limit:
                players[team_id] = self._fetch_data_F(endpoint=endpoint, params=params)
            else:
                print('Reached requests limit.')
        
        self.players = players

    def get_players(self):
        """Returns a dictionary with team_id as key and a list of all players that are signed in this team as value."""
        try:
            return self.players
        except:
            self.set_players()
            return self.players

    def get_player_ids(self):
        """Returns a list of player ids. Playing in the fixture."""
        player_ids = []
        keys = ['startXI', 'substitutes']
        for team_id in self.team_ids:
            for key in keys:
                for i in self.get_fixture_lineup()[team_id][key]:
                    player_ids.append(i['player']['id'])
        return player_ids
    
    def set_injuries(self):
        """Get injuries for both teams in the league for the given season.
        Returns a dictionary with team_id as key and a list of injuries as value."""
        print('Request injuries...')
        endpoint = 'injuries'
        injuries = {}
        
        for team_id in self.team_ids:
            params = {'season': self.season, 'team': str(team_id)}
            if self.requests <= self.requests_limit:
                injuries[team_id] = self._fetch_data_F(endpoint=endpoint, params=params)
            else:
                print('Reached requests limit.')
        
        self.injuries = injuries
    
    def get_injuries(self):
        """Returns a dictionary with team_id as key and a list of injuries as value."""
        try:
            return self.injuries
        except:
            self.set_injuries()
            return self.injuries
    
    def set_transfers(self):
        """Get transfers for both teams in the league for the given season."""
        print('Request transfers...')
        endpoint = 'transfers'
        transfers = {}
        
        for player in self.get_player_ids():
            params = {'player': str(player)}
            if self.requests <= self.requests_limit:
                transfers[player] = self._fetch_data_F(endpoint=endpoint, params=params)
            else:
                print('Reached requests limit.')
        
        self.transfers = transfers

    def get_transfers(self):
        """Returns a dictionary with player_id as key and a list of transfers as value."""
        try:
            return self.transfers
        except:
            self.set_transfers()
            return self.transfers
    
    def set_fixture_statistics(self):
        """Set fixture statistics for both teams in the league for the given season."""
        print('Request fixture statistics...')
        endpoint = 'fixtures/statistics'
        fixture_statistics = {}
        
        for team_id in self.team_ids:
            for i in self.get_fixtures()[team_id]:
                formatted_fixture_date = datetime.utcfromtimestamp(int(i['fixture']['timestamp'])).strftime('%d-%m-%Y')                
                if formatted_fixture_date < self.fixture_date:
                    params = {'fixture': str(i['fixture']['id']), 'team': str(team_id)}
                    if self.requests <= self.requests_limit:
                        if i['fixture']['id'] not in fixture_statistics.keys():
                            fixture_statistics[i['fixture']['id']] = {}
                        fixture_statistics[i['fixture']['id']][team_id] = self._fetch_data_F(endpoint=endpoint, params=params)
                    else:
                        print('Reached requests limit.')
        
        self.fixture_statistics = fixture_statistics

    def get_fixture_statistics(self):
        """Returns a dictionary with team_id as key and fixture statistics as value."""
        try:
            return self.fixture_statistics
        except:
            self.set_fixture_statistics()
            return self.fixture_statistics
    
    def set_coaches(self):
        """Set coaches for both teams in the league for the given season."""
        print('Request coaches...')
        endpoint = 'coachs'
        coaches = {}
        
        for team_id in self.team_ids:
            params = {'team': str(team_id)}
            if self.requests <= self.requests_limit:
                coaches[team_id] = self._fetch_data_F(endpoint=endpoint, params=params)
            else:
                print('Reached requests limit.')
        
        self.coaches = coaches

    def get_coaches(self):
        """Returns a dictionary with team_id as key and coaches as value."""
        try:
            return self.coaches
        except:
            self.set_coaches()
            return self.coaches
        
    def set_standings_footballAPI(self):
        """Set standings for both teams in the league for the given season."""
        print('Request standings...')
        endpoint = 'standings'
        standings = {}
        
        params = {'league': self.league_id, 'season': self.season}
        if self.requests <= self.requests_limit:
            standings = self._fetch_data_F(endpoint=endpoint, params=params)
        else:
            print('Reached requests limit.')
        
        self.standings_F = standings[0]['league']['standings'][0]

    def get_standings_footballAPI(self):
        """Returns a dictionary with team_id as key and standings as value."""
        try:
            return self.standings_F
        except:
            self.set_standings_footballAPI()
            return self.standings_F

    def set_standings_TransferMarket(self):
        """Set standings for both teams in the league for the given season."""
        print('Request standings TM...')
        endpoint = 'competitions/get-table'
        standings = {}
        
        params = {'id': self.league_id_TM, 'seasonID': self.season}
        if self.requests <= self.requests_limit:
            standings = self._fetch_data_TM(endpoint=endpoint, params=params)
        else:
            print('Reached requests limit.')
        
        self.standings_TM = standings['table']

    def get_standings_TransferMarket(self):
        """Returns a dictionary with team_id as key and standings as value."""
        try:
            return self.standings_TM
        except:
            self.set_standings_TransferMarket()
            return self.standings_TM

    def get_team_mapping(self):
        """Returns a dictionary with team_key from one API key and team_key from the other as value."""
        team_mapping = {}
        for team_id in self.team_ids:
            for i in self.get_standings_footballAPI():
                if i['team']['id'] == team_id:
                    ranking = i['rank']
            for t in self.get_standings_TransferMarket():
                if t['rank'] == ranking:
                    team_mapping[team_id] = t['id']
                    team_mapping[t['id']] = team_id
        return team_mapping
    
    def set_transfer_rumours(self):
        """Set transfer rumours for both teams in the league for the given season."""
        print('Request transfer rumours TM...')
        endpoint = 'transfers/list-rumors'
        transfer_rumours = {}
        
        for team_id in self.team_ids:
            team_id_TM = self.get_team_mapping()[team_id]
            params = {'team': str(team_id_TM)}
            params = {"competitionIds":self.league_id_TM, "clubIds":str(team_id), "sort":"date_desc","domain":self.domain_TM}
            transfer_rumours[team_id] = self._fetch_data_TM(endpoint=endpoint, params=params)['rumors']
        
        self.transfer_rumours = transfer_rumours

    def get_transfer_rumours(self):
        """Returns a dictionary with team_id as key and transfer rumours as value."""
        try:
            return self.transfer_rumours
        except:
            self.set_transfer_rumours()
            return self.transfer_rumours
        
    def set_team_news(self):
        """Set player news for both teams in the league for the given season."""
        print('Request team news TM...')
        endpoint = 'news/list-by-club'
        team_news = {}
        
        for team_id in self.team_ids:
            id = self.get_team_mapping()[team_id]
            params = {"id":id,"domain":self.domain_TM}
            team_news[team_id] = self._fetch_data_TM(endpoint=endpoint, params=params)['news']
        
        self.team_news = team_news

    def get_team_news(self):
        """Returns a dictionary with team_id as key and player news as value."""
        try:
            return self.team_news
        except:
            self.set_team_news()
            return self.team_news
        
    def set_team_fixtures_TM(self):
        """Set player news for both teams in the league for the given season."""
        print('Request team fixtures TM...')
        endpoint = 'matches/list-by-date'
        team_fixtures_TM = {}
        params = {"date":datetime.strptime(self.fixture_date, '%d-%m-%Y').strftime('%Y-%m-%d'),"domain":self.domain_TM}
        team_fixtures_TM = self._fetch_data_TM(endpoint=endpoint, params=params)['liveMatches']['IT1']
        
        self.team_fixtures_TM = team_fixtures_TM

    def get_team_fixtures_TM(self):
        """Returns a dictionary with team_id as key and player news as value."""
        try:
            return self.team_fixtures_TM
        except:
            self.set_team_fixtures_TM()
            return self.team_fixtures_TM
        
    def set_fixture_lineup_TM(self):
        """Set player news for both teams in the league for the given season."""
        print('Request fixture lineup TM...')
        endpoint = 'matches/get-line-ups'
        fixture_lineup_TM = {}
        for i in self.get_team_fixtures_TM():
            if i['homeClubID'] == self.get_team_mapping()[self.team_ids[0]] or i['homeClubID'] == self.get_team_mapping()[self.team_ids[1]]:
                params = {"id":i['id'],"domain":self.domain_TM}
                response = self._fetch_data_TM(endpoint=endpoint, params=params)['formations']
                fixture_lineup_TM[self.get_team_mapping()[i['homeClubID']]] = response['home']
                fixture_lineup_TM[self.get_team_mapping()[i['awayClubID']]] = response['away']
            time.sleep(1)

        self.fixture_lineup_TM = fixture_lineup_TM

    def get_fixture_lineup_TM(self):
        """Returns a dictionary with team_id as key and player news as value."""
        try:
            return self.fixture_lineup_TM
        except:
            self.set_fixture_lineup_TM()
            return self.fixture_lineup_TM
    
    def get_player_mapping(self):
        """Returns a dictionary with player_key from one API key and player_key from the other as value."""
        player_mapping = {}
        for team_id in self.team_ids:
            for player in self.get_fixture_lineup()[team_id]['startXI']:
                for i in self.get_fixture_lineup_TM()[team_id]['start'].values():
                    if int(i['number']) == player['player']['number']:
                        player_mapping[player['player']['id']] = i['id']
                        player_mapping[i['id']] = player['player']['id']
            for player in self.get_fixture_lineup()[team_id]['substitutes']:
                for i in self.get_fixture_lineup_TM()[team_id]['bank']:
                    if int(i['number']) == player['player']['number']:
                        player_mapping[player['player']['id']] = i['id']
                        player_mapping[i['id']] = player['player']['id']
        return player_mapping        

    def set_player_news(self):
        """Set player news for both teams in the league for the given season."""
        print('Request player news TM...')
        player_news = {}
        endpoint = 'news/list-by-player'
        for player_id in self.get_player_ids():
            player_id_TM = self.get_player_mapping()[player_id]
            params = {"id":player_id_TM,"domain":self.domain_TM}
            player_news[player_id] = self._fetch_data_TM(endpoint=endpoint, params=params)['news'][0]
            time.sleep(1)
        
        self.player_news = player_news

    def get_player_news(self):
        """Returns a dictionary with player_id as key and player news as value."""
        try:
            return self.player_news
        except:
            self.set_player_news()
            return self.player_news
        
    def get_news_ids(self):
        news_ids = set()
        for team_id in self.team_ids:
            for i in self.get_team_news()[team_id]:
                news_ids.add(i['id'])
            for i in self.get_player_news():
                for j in self.get_player_news()[i]:
                    news_ids.add(j['id'])
        return news_ids

    def set_news_details(self):
        """Set player news for both teams in the league for the given season."""
        print('Request news details TM...')
        news_detail = {}
        endpoint = 'news/detail'
        for news_id in self.get_news_ids():
            params = {"id":news_id}
            news_detail[news_id] = self._fetch_data_TM(endpoint=endpoint, params=params)['news']
            time.sleep(1)
        
        self.player_news = news_detail

    def get_news_details(self):
        """Returns a dictionary with player_id as key and player news as value."""
        try:
            return self.player_news
        except:
            self.set_news_details()
            return self.player_news

    def _fetch_data_F(self, endpoint, params, page=1, players_data=None, optional=None):
        """Fetches data recursivlely from API and returns a list of players."""
        if players_data is None:
            players_data = []

        if page > 1:
            params['page'] = page
        response = requests.get(f'{self.base_url_F}{endpoint}', params=params, headers=self.headers)
        self.requests += 1
        print(f"Requests: {response.status_code}")
        time.sleep(2)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            players = response.json()
            print(f"response: {response.json()['results']}")
            players_data += players['response']

            if optional is not None:
                print(f"response: {players['response']}")
                return players['response']

            if players['paging']['current'] < players['paging']['total']:
                next_page = players['paging']['current'] + 1

                # Add a sleep delay if needed
                if next_page % 2 == 1:
                    time.sleep(3)

                players_data = self._fetch_data_F(endpoint, params, next_page, players_data)

        else:
            print(f"Request failed with status code: {response.status_code}")

        print(f"Players_data: {players_data}")
        return players_data

    def _fetch_data_TM(self, endpoint, params):
        """Fetches data from TransferMarket API"""
        print(params)
        response = requests.get(f'{self.base_url_TM}{endpoint}', params=params, headers=self.headers_TM)
        print(f"Response: {response}")
        return response.json()