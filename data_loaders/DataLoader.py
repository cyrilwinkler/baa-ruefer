# data_loaders/data_loader.py
import json
from abc import ABC, abstractmethod

class DataLoader(ABC):
    """
    Abstract class to load data from api or json files
    
    :param team_ids: list of team ids
    :param api: api object to get data from api
    """
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

            self.home_team_id = 489

            self.todays_fixture_id =  731608
            
        else:
            self.team_information = api.get_team_information()
            with open('../data/api/test/team_information.json', 'w', encoding='UTF-8') as f:
                json.dump(self.team_information, f, ensure_ascii=False, indent=4)
            print('team_information saved')
            
            self.team_stats = api.get_team_statistics()
            with open('../data/api/test/team_stats.json', 'w', encoding='UTF-8') as f:
                json.dump(self.team_stats, f, ensure_ascii=False, indent=4)
            print('team_stats saved')

            self.team_fixtures = api.get_fixtures()
            with open('../data/api/test/team_fixtures.json', 'w', encoding='UTF-8') as f:
                json.dump(self.team_fixtures, f, ensure_ascii=False, indent=4)
            print('team_fixtures saved')

            self.fixture_lineups = api.get_fixture_lineup()
            with open('../data/api/test/fixture_lineups.json', 'w', encoding='UTF-8') as f:
                json.dump(self.fixture_lineups, f, ensure_ascii=False, indent=4)
            print('fixture_lineups saved')

            self.players = api.get_players()
            with open('../data/api/test/players.json', 'w', encoding='UTF-8') as f:
                json.dump(self.players, f, ensure_ascii=False, indent=4)
            print('players saved')

            self.players_ids = api.get_player_ids()
            with open('../data/api/test/players_ids.json', 'w', encoding='UTF-8') as f:
                json.dump(self.players_ids, f, ensure_ascii=False, indent=4)
            print('players_ids saved')

            self.player_injuries = api.get_injuries()
            with open('../data/api/test/player_injuries.json', 'w', encoding='UTF-8') as f:
                json.dump(self.player_injuries, f, ensure_ascii=False, indent=4)
            print('player_injuries saved')

            self.transfers = api.get_transfers()
            with open('../data/api/test/transfers.json', 'w', encoding='UTF-8') as f:
                json.dump(self.transfers, f, ensure_ascii=False, indent=4)
            print('transfers saved')

            self.coaches = api.get_coaches()
            with open('../data/api/test/coaches.json', 'w', encoding='UTF-8') as f:
                json.dump(self.coaches, f, ensure_ascii=False, indent=4)
            print('coaches saved')

            self.team_mapping = api.get_team_mapping()
            with open('../data/api/test/team_mapping.json', 'w', encoding='UTF-8') as f:
                json.dump(self.team_mapping, f, ensure_ascii=False, indent=4)
            print('team_mapping saved')

            self.transfer_rumours = api.get_transfer_rumours()
            with open('../data/api/test/transfer_rumours.json', 'w', encoding='UTF-8') as f:
                json.dump(self.transfer_rumours, f, ensure_ascii=False, indent=4)
            print('transfer_rumours saved')

            self.team_news = api.get_team_news()
            with open('../data/api/test/team_news.json', 'w', encoding='UTF-8') as f:
                json.dump(self.team_news, f, ensure_ascii=False, indent=4)
            print('team_news saved')

            self.player_news = api.get_player_news()
            with open('../data/api/test/player_news.json', 'w', encoding='UTF-8') as f:
                json.dump(self.player_news, f, ensure_ascii=False, indent=4)
            print('player_news saved')

            self.news_ids = api.get_news_ids()
            with open('../data/api/test/news_ids.json', 'w', encoding='UTF-8') as f:
                json.dump(self.news_ids, f, ensure_ascii=False, indent=4)
            print('news_ids saved')

            self.player_mapping = api.get_player_mapping()
            with open('../data/api/test/player_mapping.json', 'w', encoding='UTF-8') as f:
                json.dump(self.player_mapping, f, ensure_ascii=False, indent=4)
            print('player_mapping saved')

            self.todays_fixture_id = api.get_todays_fixture_id()
            with open('../data/api/test/todays_fixture_id.json', 'w', encoding='UTF-8') as f:
                json.dump(self.todays_fixture_id, f, ensure_ascii=False, indent=4)
            print('todays_fixture_id saved')

            self.home_team_id = api.get_home_team_id()
            with open('../data/api/test/home_team_id.json', 'w', encoding='UTF-8') as f:
                json.dump(self.home_team_id, f, ensure_ascii=False, indent=4)
            print('home_team_id saved')

            self.fixture_stats = api.get_fixture_statistics() #60 Requests (only Serie A)
            self.news_details = api.get_news_details() #310 Requests
        
    
    @abstractmethod
    def get_player_names(self):
        pass

    @abstractmethod
    def get_player_information(self):
        pass

    @abstractmethod
    def get_player_statistics(self):
        pass

    @abstractmethod
    def get_player_injuries(self):
        pass

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
    def get_player_transfers(self):
        pass

    @abstractmethod
    def get_player_news(self):
        pass

    @abstractmethod
    def get_news_details(self):
        pass

    @abstractmethod
    def get_team_news(self):
        pass

    @abstractmethod
    def get_head_to_head(self):
        pass

    @abstractmethod
    def get_home_team_id(self):
        pass

    @abstractmethod
    def get_players_ids(self):
        pass

    @abstractmethod
    def get_team_fixtures(self):
        pass

    @abstractmethod
    def get_todays_fixture_id(self):
        pass

    @abstractmethod
    def get_fixture_lineup(self):
        pass

    @abstractmethod
    def get_fixture_stats(self):
        pass

    @abstractmethod
    def get_coaches(self):
        pass

