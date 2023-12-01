# data_loaders/data_loader.py
import json
from abc import ABC, abstractmethod

class DataLoader(ABC):
    def __init__(self, team_ids: list, api=None):
        self.team_ids = team_ids
        
        if api is None:
            with open('../data/api/team_information.json') as f:
                self.team_information = json.load(f)

            with open('../data/api/team_stats.json') as f:
                self.team_stats = json.load(f)

            with open('../data/api/team_fixtures.json') as f:
                self.team_fixtures = json.load(f)

            with open('../data/api/fixture_lineups.json') as f:
                self.fixture_lineups = json.load(f)

            with open('../data/api/fixture_stats.json') as f:
                self.fixture_stats = json.load(f)

            with open('../data/api/players.json') as f:
                self.players = json.load(f)

            with open('../data/api/players_ids.json') as f:
                self.players_ids = json.load(f)

            with open('../data/api/player_injuries.json') as f:
                self.player_injuries = json.load(f)

            with open('../data/api/transfers.json') as f:
                self.transfers = json.load(f)

            with open('../data/api/coaches.json') as f:
                self.coaches = json.load(f)

            with open('../data/api/team_mapping.json') as f:
                self.team_mapping = json.load(f)

            with open('../data/api/transfer_rumours.json') as f:
                self.transfer_rumours = json.load(f)

            with open('../data/api/team_news.json') as f:
                self.team_news = json.load(f)

            with open('../data/api/player_news.json') as f:
                self.player_news = json.load(f)

            with open('../data/api/news_ids.json') as f:
                self.news_ids = json.load(f)

            with open('../data/api/player_mapping.json') as f:
                self.player_mapping = json.load(f)

            with open('../data/api/news_details.json') as f:
                self.news_details = json.load(f)

            self.home_team_id = 487

            self.todays_fixture_id = 731586
            
        else:
            self.team_information = api.get_team_information()
            self.teams_stats = api.get_team_statistics()
            self.team_fixtures = api.get_fixtures()
            self.fixture_lineups = api.get_fixture_lineup()
            self.players = api.get_players()
            self.players_ids = api.get_player_ids()
            self.player_injuries = api.get_injuries()
            self.transfers = api.get_transfers()
            self.coaches = api.get_coaches()
            self.team_mapping = api.get_team_mapping()
            self.transfer_rumours = api.get_transfer_rumours()
            self.team_news = api.get_team_news()
            self.player_news = api.get_player_news()
            self.news_ids = api.get_news_ids()
            self.player_mapping = api.get_player_mapping()
            self.todays_fixture_id = api.get_todays_fixture_id()
            #self.home_team_id = api.get_home_team_id()
            #self.fixture_stats = api.get_fixture_statistics() 60 Requests (only Serie A)
            #self.news_details = api.get_news_details() 310 Requests
        
    @abstractmethod
    def get_team_information(self):
        pass

    @abstractmethod
    def get_venue_information(self):
        pass

    @abstractmethod
    def get_team_statistics(self):
        pass

    @abstractmethod
    def get_team_players(self):
        pass

    @abstractmethod
    def get_player_injuries(self):
        pass

    @abstractmethod
    def get_team_fixtures(self):
        pass

    @abstractmethod
    def get_head_to_head(self):
        pass

    @abstractmethod
    def get_fixture_stats(self):
        pass

    @abstractmethod
    def get_player_news(self):
        pass
