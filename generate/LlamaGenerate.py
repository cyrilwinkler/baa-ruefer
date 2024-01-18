import sys
sys.path.append('/Users/tschip/workspace/baa/baa-ruefer/')
import openai
import json
import time
import re
import tqdm

from data_loaders.JSONDataLoader import JSONDataLoader
from generate.Metrics import Metrics

class LlamaGenerate():
    """
    A class for generating Llama-2 output using the JSONDataLoader and Metrics classes.

    Args:
    team_ids (list): A list of team IDs for which data will be generated.
    requests_api (object, optional): An object providing API request capabilities. Default is None.

    Attributes:
    metrics (Metrics): An instance of the Metrics class for calculating ROUGE and PARENT-T metrics.
    team_ids (list): A list of team IDs for which data will be generated.
    player_names (dict): Player names information obtained from JSONDataLoader.
    player_information (dict): Player general information obtained from JSONDataLoader.
    player_statistics (dict): Player statistics obtained from JSONDataLoader.
    player_injuries (dict): Player injuries information obtained from JSONDataLoader.
    team_information (dict): Team information obtained from JSONDataLoader.
    venue_information (dict): Venue information obtained from JSONDataLoader.
    team_statistics (dict): Team statistics obtained from JSONDataLoader.
    player_transfers (dict): Player transfers information obtained from JSONDataLoader.
    player_news (dict): Player-related news obtained from JSONDataLoader.
    news_details (dict): News details obtained from JSONDataLoader.
    team_news (dict): Team-related news obtained from JSONDataLoader.
    head_to_head (dict): Head-to-head statistics obtained from JSONDataLoader.
    home_team (int): The ID of the home team for today's fixture obtained from JSONDataLoader.
    players_ids (dict): Player IDs information obtained from JSONDataLoader.
    team_fixtures (dict): Team fixtures obtained from JSONDataLoader.
    todays_fixture_id (int): The ID of today's fixture obtained from JSONDataLoader.
    fixture_lineup (dict): Fixture lineup information obtained from JSONDataLoader.
    fixture_statistics (dict): Fixture statistics obtained from JSONDataLoader.
    coaches (dict): Coaches information obtained from JSONDataLoader.
    """
    def __init__(self, team_ids: list, requests_api=None):
        dataloader = JSONDataLoader(team_ids, requests_api)
        self.metrics = Metrics()
        self.team_ids = team_ids
        self.player_names = dataloader.get_player_names()
        self.player_information = dataloader.get_player_information()
        self.player_statistics = dataloader.get_player_statistics()
        self.player_injuries = dataloader.get_player_injuries()
        self.team_information = dataloader.get_team_information()
        self.venue_information = dataloader.get_venue_information()
        self.team_statistics = dataloader.get_team_statistics()
        self.player_transfers = dataloader.get_player_transfers()
        self.player_news = dataloader.get_player_news()
        self.news_details = dataloader.get_news_details()
        self.team_news = dataloader.get_team_news()
        self.head_to_head = dataloader.get_head_to_head()
        self.home_team = dataloader.get_home_team_id()
        self.players_ids = dataloader.get_players_ids()
        self.team_fixtures = dataloader.get_team_fixtures()
        self.todays_fixture_id = dataloader.get_todays_fixture_id()
        self.fixture_lineup = dataloader.get_fixture_lineup()
        self.fixture_statistics = dataloader.get_fixture_stats()
        self.coaches = dataloader.get_coaches()
    
    def get_team_ids(self):
        """Returns list of team IDs."""
        return self.team_ids
    
    def get_team_name(self, team_id):
        """Returns team name for given team ID."""
        for fixture_key in dict(sorted(self.head_to_head.items())):
            if self.head_to_head[fixture_key]['home_id'] == team_id:
                return self.head_to_head[fixture_key]['home_name']
            else:
                return self.head_to_head[fixture_key]['away_name']
            
    def get_team_information(self):
        """Returns the team information."""
        return self.team_information
            
    def get_team_statistics(self, team_id):
        """Returns dictionary of team statistics for given team ID."""
        return self.team_statistics[team_id]
    
    def get_team_news(self):
        """Returns the team news."""
        team_news_detail = {}
        for team_id in self.team_news:
            team_news_detail[team_id] = {}
            for news in self.team_news[team_id]:
                if news['id'] in self.news_details:
                    team_news_detail[team_id][news['newsHeadline']] = ''.join(value for key, value in sorted(self.news_details[news['id']]['text'].items()))
        team_news_detail = {key: value for key, value in team_news_detail.items() if value}
        return team_news_detail
    
    def get_players_ids(self):
        """Returns list of player IDs."""
        return self.players_ids
    
    def get_player_names(self):
        """Returns list of player names."""
        return self.player_names

    def get_player_information(self):
        """Returns the player information."""
        return self.player_information
    
    def get_player_statistics(self):
        """Returns the player statistics."""
        return self.player_statistics
    
    def get_player_transfers(self):
        """Returns the player transfers."""
        return self.player_transfers
    
    def get_player_injuires(self):
        """Returns the player injuries."""
        return self.player_injuries
    
    def get_player_news(self):
        """Returns the player news."""
        player_news_detail = {}
        for player_id in self.player_news:
            player_news_detail[player_id] = {}
            for news in self.player_news[player_id]:
                if news['id'] in self.news_details:
                    player_news_detail[player_id][news['newsHeadline']] = ''.join(value for key, value in sorted(self.news_details[news['id']]['text'].items()))
        player_news_detail = {key: value for key, value in player_news_detail.items() if value}
        return player_news_detail
    
    def get_team_coach(self):
        """Returns the team coach."""
        for team_id in self.coaches:
            try:
                del self.coaches[team_id]['id']
                del self.coaches[team_id]['name']
                if self.coaches[team_id]['height'] == None:
                    del self.coaches[team_id]['height']
                if self.coaches[team_id]['weight'] == None:
                    del self.coaches[team_id]['weight']
            except:
                pass
        return self.coaches
    
    def get_today_fixture_id(self):
        """Returns the fixture ID for today's match."""
        return self.todays_fixture_id
    
    def get_fixture_information(self):
        """Returns the fixture information."""
        fixtures = self.team_fixtures[list(self.team_fixtures.keys())[0]]
        for fixture in fixtures:
            if fixture == self.todays_fixture_id:
                fixture =  self.team_fixtures[str(self.home_team)][fixture]
                try:
                    del fixture['fixture_id']
                    del fixture['league_id']
                    del fixture['league_logo']
                    del fixture['league_name']
                    del fixture['league_country']
                    del fixture['league_flag']
                    del fixture['league_season']
                    del fixture['teams_home_id']
                    del fixture['teams_away_id']
                except:
                    pass

                return fixture
            
    def get_fixture_lineup(self):
        """Returns the fixture lineup."""
        return self.fixture_lineup
    
    def get_player_ids_from_fixture(self, team_id):
        """Returns the player IDs from the fixture lineup."""
        all_ids = set()
        # Extract player IDs from 'startXI'
        for player_info in self.get_fixture_lineup()[str(team_id)].get('startXI', []):
            player_id = player_info.get('player', {}).get('id')
            if player_id is not None:
                all_ids.add(player_id)

        # Extract player IDs from 'substitutes'
        for substitute_info in self.get_fixture_lineup()[str(team_id)].get('substitutes', []):
            player_id = substitute_info.get('player', {}).get('id')
            if player_id is not None:
                all_ids.add(player_id)

        return list(all_ids)
    
    def get_fixture_statistics(self):
        """Returns the fixture statistics."""
        return self.fixture_statistics

    def get_venue_information(self):
        """Returns the venue information."""
        for venue_id in self.venue_information:
            if self.venue_information[venue_id]['name'] == self.get_fixture_information()['fixture_venue']:
                try:
                    del self.venue_information[venue_id]['team_id']
                except:
                    pass
                return self.venue_information[venue_id]
    
    def generate_team_information(self, team_id):
        """Generates Llama-2 output for team information for the given team ID."""
        messages = [
            {   
                "role": "system", 
                "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentence. Without introduction what you did."
            },
            {
                "role": "user",
                "content": "Generate a sentence about the team information. The informations are provided in the JSON. {'name': 'Lazio', 'code': 'LAZ', 'country': 'Italy', 'founded': 1900}"
            },
            {
                "role": "assistant",
                "content": "Lazio, proudly bearing the code LAZ, hails from the heart of Italy. With roots tracing back to 1900, they have a rich history in the panorama of world football, steadily leaving their mark through every passing decade."
            },
            {
                "role": "user",
                "content": f"Generate a sentence about the team information. The informations are provided in the JSON. {self.get_team_information()[team_id]}"
            },
        ]
        model_outputs = self._generate_llama_output(messages)

        self.metrics.set_parentT_score('team_information', model_outputs, self.get_team_information()[team_id])

        return model_outputs
    
    def generate_team_statistics(self, team_id):
        """Generates Llama-2 output for team statistics for the given team ID."""
        messages = [
            {   
                "role": "system", 
                "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentences about statistical facts in JSON format. Without introduction what you did."
            },
            {
                "role": "user",
                "content": """Give me multiple different sentences about the team statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {'team_name': 'Lazio', 'fixtures_played_home': 19, 'fixtures_played_away': 19, 'fixtures_wins_home': 10, 'fixtures_wins_away': 8, 'fixtures_draws_home': 6, 'fixtures_draws_away': 4, 'fixtures_loses_home': 3, 'fixtures_loses_away': 7, 'fixtures_loses_total': 10, 'goals_for_total_home': 42, 'goals_for_total_away': 35, 'goals_for_average_home': '2.2', 'goals_for_average_away': '1.8', 'goals_for_average_total': '2.0', 'goals_for_minute_0-15_total': 12, 'goals_for_minute_0-15_percentage': '16.00%', 'goals_for_minute_16-30_total': 7, 'goals_for_minute_16-30_percentage': '9.33%', 'goals_for_minute_31-45_total': 14, 'goals_for_minute_31-45_percentage': '18.67%', 'goals_for_minute_46-60_total': 13, 'goals_for_minute_46-60_percentage': '17.33%', 'goals_for_minute_61-75_total': 15, 'goals_for_minute_61-75_percentage': '20.00%', 'goals_for_minute_76-90_total': 8, 'goals_for_minute_76-90_percentage': '10.67%', 'goals_for_minute_91-105_total': 6,
                 'goals_for_minute_91-105_percentage': '8.00%', 'goals_for_minute_106-120_total': None, 'goals_for_minute_106-120_percentage': None, 'goals_against_total_home': 25, 'goals_against_total_away': 33, 'goals_against_total_total': 58, 'goals_against_average_home': '1.3', 'goals_against_average_away': '1.7', 'goals_against_average_total': '1.5', 'goals_against_minute_0-15_total': 14, 'goals_against_minute_0-15_percentage': '23.33%', 'goals_against_minute_16-30_total': 8, 'goals_against_minute_16-30_percentage': '13.33%', 'goals_against_minute_31-45_total': 8,
                 'goals_against_minute_31-45_percentage': '13.33%', 'goals_against_minute_46-60_total': 7, 'goals_against_minute_46-60_percentage': '11.67%', 'goals_against_minute_61-75_total': 10, 'goals_against_minute_61-75_percentage': '16.67%', 'goals_against_minute_76-90_total': 7, 'goals_against_minute_76-90_percentage': '11.67%', 'goals_against_minute_91-105_total': 6, 'goals_against_minute_91-105_percentage': '10.00%'}
                        """
            },
            {
                "role": "assistant",
                "content": """{
                \"fixtures_played\": \"Lazio has played an equal amount of games at home and away this season, with a total of 19 each, summing up to a total of 38 fixtures overall.\",
                \"fixtures_wins\": \"In terms of victories, Lazio has a slight home advantage, with 10 wins at home and 8 on the road, bringing their total fixtures wins to 18.\",
                \"fixtures_draws_loses\": \"Lazio has had 10 draws and 10 losses in total this season, with a marginally higher draws and losses count at home.\",
                \"goal_statistics\": \"The team scored a total of 77 goals, with 42 at home and 35 away, which gives them an average of 2.0 goals per game. Regarding conceded goals, they let in 58 goals in total, slightly more away (33) than at home (25).\",
                \"goal_timing\": \"Lazio tends to score most of their goals between the 61st and 75th minute, while they are most vulnerable to conceding in the opening 15 minutes of the game.\",
                
                }"""
            },
            {
                "role": "user",
                "content": f"Give me multiple different sentences about the team statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {self.team_statistics[team_id]}"
            },
        ]
        team_statistics_output = self._generate_llama_output(messages)
        try:
            model_outputs = json.loads(self.correct_json(self.extract_first_match(team_statistics_output)))                
            self.metrics.set_parentT_score('team_statistics', model_outputs, self.get_team_statistics(team_id))
            return model_outputs        
        except:
            self.metrics.set_parentT_score('team_statistics', None, None)
            return None
            
    def generate_team_news(self, team_id):
        """Generates Llama-2 output for team news for the given team ID."""
        teams = {}
        news = self.get_team_news()
        teams[team_id] = {}

        if str(team_id) in news:        
            teams[team_id]['news'] = {}
            for n in news[str(team_id)].items():
                pattern = re.compile('<.*?>')
                result = re.sub(pattern, '', n[1])
                teams[team_id]['news'][n[0]] = self._generate_llama_output(f"Summarize the news article with focus on the team {self.get_team_name(team_id)}. The article is provided in the JSON. Format it as a normal text. summarize it with at most 3 sentences. {result}")
                self.metrics.calculate_rouge_scores(teams[team_id]['news'][n[0]], result)
                break
        else:
            teams[team_id]['news'] = None

        return teams

    def generate_team_injuries(self, team_id):
        """Generates Llama-2 output for team injuries for the given team ID."""
        fixture_id = self.todays_fixture_id
        injuries = self.player_injuries[str(team_id)]
        injuries_dict = {}
        outputs = {}
        print(f"Generate players injuries for team {team_id}")
        for player_id in tqdm.tqdm(injuries):
            if injuries[player_id]['fixture_id'] == fixture_id:
                injuries_dict[player_id] = injuries[player_id]
                injuries_dict[player_id]['player_name'] = self.get_player_names()[team_id][player_id]
                del injuries_dict[player_id]['fixture_id']
                messages = [
                    {
                        "role": "system",
                        "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentence. Without introduction what you did."
                    },
                    {
                        "role": "user",
                        "content": f"Generate a sentence about the player and the injury for the fixture. The information are provided in the JSON. {injuries_dict[player_id]}"
                    },
                ]
                outputs[player_id] = self._generate_llama_output(messages)

                self.metrics.set_parentT_score.append('team_injuries', outputs[player_id], injuries_dict[player_id])

        return outputs

    def generate_team_players(self, team_id):
        """Generates Llama-2 output for each team player in the given team."""
        players = {}
        information = self.get_player_information()[str(team_id)]
        statistics = self.get_player_statistics()[str(team_id)]
        transfers = self.get_player_transfers()
        transfer_dict = {}
        news = self.get_player_news()
        counter = 1
        print(f"Generating player information and statistics for team team_id")
        for player_id in tqdm.tqdm(self.get_player_ids_from_fixture(team_id)):
            players[player_id] = {}
            try:
                del information[player_id]['injured']
                del information[player_id]['name']
            except:
                pass
            player_information_message = [
                {   
                    "role": "system", 
                    "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentence. Without introduction what you did."
                },
                {
                    "role": "user",
                    "content": "Generate a sentence about the team information. The informations are provided in the JSON. {'name': 'Lazio', 'code': 'LAZ', 'country': 'Italy', 'founded': 1900}"
                },
                {
                    "role": "assistant",
                    "content": "Lazio, proudly bearing the code LAZ, hails from the heart of Italy. With roots tracing back to 1900, they have a rich history in the panorama of world football, steadily leaving their mark through every passing decade."
                },
                {
                    "role": "user",
                    "content": f"Generate a sentence about the player information. The informations are provided in the JSON. {information[player_id]}"
                },
            ]
            player_information_output = self._generate_llama_output(player_information_message)
            try:
                model_outputs = json.loads(self.correct_json(self.extract_first_match(player_information_output)))
                self.metrics.set_parentT_score('player_information', model_outputs, information[player_id])
                players[player_id]['information'] = model_outputs
            except:
                self.metrics.set_parentT_score('player_information', None, None)
                players[player_id]['information'] = None

            statistics[player_id]['player_name'] = self.get_player_names()[team_id][player_id]
            player_statistics_messages = [
                {   
                    "role": "system", 
                    "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentences about statistical facts in JSON format. Without introduction what you did."
                },
                {
                    "role": "user",
                    "content": """Give me multiple different sentences about the team statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {'team_name': 'Lazio', 'fixtures_played_home': 19, 'fixtures_played_away': 19, 'fixtures_wins_home': 10, 'fixtures_wins_away': 8, 'fixtures_draws_home': 6, 'fixtures_draws_away': 4, 'fixtures_loses_home': 3, 'fixtures_loses_away': 7, 'fixtures_loses_total': 10, 'goals_for_total_home': 42, 'goals_for_total_away': 35, 'goals_for_average_home': '2.2', 'goals_for_average_away': '1.8', 'goals_for_average_total': '2.0', 'goals_for_minute_0-15_total': 12, 'goals_for_minute_0-15_percentage': '16.00%', 'goals_for_minute_16-30_total': 7, 'goals_for_minute_16-30_percentage': '9.33%', 'goals_for_minute_31-45_total': 14, 'goals_for_minute_31-45_percentage': '18.67%', 'goals_for_minute_46-60_total': 13, 'goals_for_minute_46-60_percentage': '17.33%', 'goals_for_minute_61-75_total': 15, 'goals_for_minute_61-75_percentage': '20.00%', 'goals_for_minute_76-90_total': 8, 'goals_for_minute_76-90_percentage': '10.67%', 'goals_for_minute_91-105_total': 6,
                    'goals_for_minute_91-105_percentage': '8.00%', 'goals_for_minute_106-120_total': None, 'goals_for_minute_106-120_percentage': None, 'goals_against_total_home': 25, 'goals_against_total_away': 33, 'goals_against_total_total': 58, 'goals_against_average_home': '1.3', 'goals_against_average_away': '1.7', 'goals_against_average_total': '1.5', 'goals_against_minute_0-15_total': 14, 'goals_against_minute_0-15_percentage': '23.33%', 'goals_against_minute_16-30_total': 8, 'goals_against_minute_16-30_percentage': '13.33%', 'goals_against_minute_31-45_total': 8,
                    'goals_against_minute_31-45_percentage': '13.33%', 'goals_against_minute_46-60_total': 7, 'goals_against_minute_46-60_percentage': '11.67%', 'goals_against_minute_61-75_total': 10, 'goals_against_minute_61-75_percentage': '16.67%', 'goals_against_minute_76-90_total': 7, 'goals_against_minute_76-90_percentage': '11.67%', 'goals_against_minute_91-105_total': 6, 'goals_against_minute_91-105_percentage': '10.00%'}
                            """
                },
                {
                    "role": "assistant",
                    "content": """{
                    \"fixtures_played\": \"Lazio has played an equal amount of games at home and away this season, with a total of 19 each, summing up to a total of 38 fixtures overall.\",
                    \"fixtures_wins\": \"In terms of victories, Lazio has a slight home advantage, with 10 wins at home and 8 on the road, bringing their total fixtures wins to 18.\",
                    \"fixtures_draws_loses\": \"Lazio has had 10 draws and 10 losses in total this season, with a marginally higher draws and losses count at home.\",
                    \"goal_statistics\": \"The team scored a total of 77 goals, with 42 at home and 35 away, which gives them an average of 2.0 goals per game. Regarding conceded goals, they let in 58 goals in total, slightly more away (33) than at home (25).\",
                    \"goal_timing\": \"Lazio tends to score most of their goals between the 61st and 75th minute, while they are most vulnerable to conceding in the opening 15 minutes of the game.\",
                    
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Give me multiple different sentences about the player statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {statistics[player_id]}"
                },
            ]

            player_statistics_output = self._generate_llama_output(player_statistics_messages)
            try:
                model_outputs = json.loads(self.correct_json(self.extract_first_match(player_statistics_output)))
                self.metrics.set_parentT_score('player_statistics', model_outputs, statistics[player_id])
                players[player_id]['statistics'] = model_outputs

            except:
                self.metrics.set_parentT_score('player_statistics', None, None)
                players[player_id]['statistics'] =  None

            try:
                transfer_dict[player_id] = {}
                transfer_dict[player_id]['player_name'] = self.get_player_names()[team_id][player_id]
                transfer_dict[player_id]['transfers'] = transfers[str(player_id)]
                player_transfers_message = [
                    {   
                        "role": "system", 
                        "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentences about statistical facts in JSON format. Without introduction what you did."
                    },
                    {
                        "role": "user",
                        "content": """Give me multiple different sentences about the team statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {'team_name': 'Lazio', 'fixtures_played_home': 19, 'fixtures_played_away': 19, 'fixtures_wins_home': 10, 'fixtures_wins_away': 8, 'fixtures_draws_home': 6, 'fixtures_draws_away': 4, 'fixtures_loses_home': 3, 'fixtures_loses_away': 7, 'fixtures_loses_total': 10, 'goals_for_total_home': 42, 'goals_for_total_away': 35, 'goals_for_average_home': '2.2', 'goals_for_average_away': '1.8', 'goals_for_average_total': '2.0', 'goals_for_minute_0-15_total': 12, 'goals_for_minute_0-15_percentage': '16.00%', 'goals_for_minute_16-30_total': 7, 'goals_for_minute_16-30_percentage': '9.33%', 'goals_for_minute_31-45_total': 14, 'goals_for_minute_31-45_percentage': '18.67%', 'goals_for_minute_46-60_total': 13, 'goals_for_minute_46-60_percentage': '17.33%', 'goals_for_minute_61-75_total': 15, 'goals_for_minute_61-75_percentage': '20.00%', 'goals_for_minute_76-90_total': 8, 'goals_for_minute_76-90_percentage': '10.67%', 'goals_for_minute_91-105_total': 6,
                        'goals_for_minute_91-105_percentage': '8.00%', 'goals_for_minute_106-120_total': None, 'goals_for_minute_106-120_percentage': None, 'goals_against_total_home': 25, 'goals_against_total_away': 33, 'goals_against_total_total': 58, 'goals_against_average_home': '1.3', 'goals_against_average_away': '1.7', 'goals_against_average_total': '1.5', 'goals_against_minute_0-15_total': 14, 'goals_against_minute_0-15_percentage': '23.33%', 'goals_against_minute_16-30_total': 8, 'goals_against_minute_16-30_percentage': '13.33%', 'goals_against_minute_31-45_total': 8,
                        'goals_against_minute_31-45_percentage': '13.33%', 'goals_against_minute_46-60_total': 7, 'goals_against_minute_46-60_percentage': '11.67%', 'goals_against_minute_61-75_total': 10, 'goals_against_minute_61-75_percentage': '16.67%', 'goals_against_minute_76-90_total': 7, 'goals_against_minute_76-90_percentage': '11.67%', 'goals_against_minute_91-105_total': 6, 'goals_against_minute_91-105_percentage': '10.00%'}
                                """
                    },
                    {
                        "role": "assistant",
                        "content": """{
                        \"fixtures_played\": \"Lazio has played an equal amount of games at home and away this season, with a total of 19 each, summing up to a total of 38 fixtures overall.\",
                        \"fixtures_wins\": \"In terms of victories, Lazio has a slight home advantage, with 10 wins at home and 8 on the road, bringing their total fixtures wins to 18.\",
                        \"fixtures_draws_loses\": \"Lazio has had 10 draws and 10 losses in total this season, with a marginally higher draws and losses count at home.\",
                        \"goal_statistics\": \"The team scored a total of 77 goals, with 42 at home and 35 away, which gives them an average of 2.0 goals per game. Regarding conceded goals, they let in 58 goals in total, slightly more away (33) than at home (25).\",
                        \"goal_timing\": \"Lazio tends to score most of their goals between the 61st and 75th minute, while they are most vulnerable to conceding in the opening 15 minutes of the game.\",
                        
                        }"""
                    },
                    {
                        "role": "user",
                        "content": f"Give me multiple different sentences about the player transfers. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {transfer_dict[player_id]}"
                    },
                ]

                player_transfers = self._generate_llama_output(player_transfers_message)
                try:
                    model_outputs = json.loads(self.correct_json(self.extract_first_match(player_transfers)))
                    
                    self.metrics.set_parentT_score('player_transfers', model_outputs, transfer_dict[player_id])
                    players[player_id]['transfers'] = json.loads(self.correct_json(self.extract_first_match(player_transfers)))
                except:
                    self.metrics.set_parentT_score('player_transfers', None, None)
                    players[player_id]['transfers'] = None
            except:
                players[player_id]['transfers'] = 'No transfers for this player'

            if str(player_id) in news:
                players[player_id]['news'] = {}
                for n in news[str(player_id)].items():
                    pattern = re.compile('<.*?>')
                    result = re.sub(pattern, '', n[1])
                    players[player_id]['news'][n[0]] = self._generate_llama_output(f"""Summarize the news article with focus on the player {self.get_player_names()[team_id][player_id]}. 
                                                                                   Summarize it with at most 3 sentences. {result}""")
                    self.metrics.calculate_rouge_scores(players[player_id]['news'][n[0]], result)
                    break
            else:
                players[player_id]['news'] = None
            counter += 1
            if counter % 10 == 0:
                time.sleep(3)
        return players

    def generate_team_coach(self, team_id):
        """Generates Llama-2 output for team coach for the given team ID."""
        team_coach_messages = [
                {   
                    "role": "system", 
                    "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentences about statistical facts in JSON format. Without introduction what you did."
                },
                {
                    "role": "user",
                    "content": """Give me multiple different sentences about the team statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {'team_name': 'Lazio', 'fixtures_played_home': 19, 'fixtures_played_away': 19, 'fixtures_wins_home': 10, 'fixtures_wins_away': 8, 'fixtures_draws_home': 6, 'fixtures_draws_away': 4, 'fixtures_loses_home': 3, 'fixtures_loses_away': 7, 'fixtures_loses_total': 10, 'goals_for_total_home': 42, 'goals_for_total_away': 35, 'goals_for_average_home': '2.2', 'goals_for_average_away': '1.8', 'goals_for_average_total': '2.0', 'goals_for_minute_0-15_total': 12, 'goals_for_minute_0-15_percentage': '16.00%', 'goals_for_minute_16-30_total': 7, 'goals_for_minute_16-30_percentage': '9.33%', 'goals_for_minute_31-45_total': 14, 'goals_for_minute_31-45_percentage': '18.67%', 'goals_for_minute_46-60_total': 13, 'goals_for_minute_46-60_percentage': '17.33%', 'goals_for_minute_61-75_total': 15, 'goals_for_minute_61-75_percentage': '20.00%', 'goals_for_minute_76-90_total': 8, 'goals_for_minute_76-90_percentage': '10.67%', 'goals_for_minute_91-105_total': 6,
                    'goals_for_minute_91-105_percentage': '8.00%', 'goals_for_minute_106-120_total': None, 'goals_for_minute_106-120_percentage': None, 'goals_against_total_home': 25, 'goals_against_total_away': 33, 'goals_against_total_total': 58, 'goals_against_average_home': '1.3', 'goals_against_average_away': '1.7', 'goals_against_average_total': '1.5', 'goals_against_minute_0-15_total': 14, 'goals_against_minute_0-15_percentage': '23.33%', 'goals_against_minute_16-30_total': 8, 'goals_against_minute_16-30_percentage': '13.33%', 'goals_against_minute_31-45_total': 8,
                    'goals_against_minute_31-45_percentage': '13.33%', 'goals_against_minute_46-60_total': 7, 'goals_against_minute_46-60_percentage': '11.67%', 'goals_against_minute_61-75_total': 10, 'goals_against_minute_61-75_percentage': '16.67%', 'goals_against_minute_76-90_total': 7, 'goals_against_minute_76-90_percentage': '11.67%', 'goals_against_minute_91-105_total': 6, 'goals_against_minute_91-105_percentage': '10.00%'}
                            """
                },
                {
                    "role": "assistant",
                    "content": """{
                    \"fixtures_played\": \"Lazio has played an equal amount of games at home and away this season, with a total of 19 each, summing up to a total of 38 fixtures overall.\",
                    \"fixtures_wins\": \"In terms of victories, Lazio has a slight home advantage, with 10 wins at home and 8 on the road, bringing their total fixtures wins to 18.\",
                    \"fixtures_draws_loses\": \"Lazio has had 10 draws and 10 losses in total this season, with a marginally higher draws and losses count at home.\",
                    \"goal_statistics\": \"The team scored a total of 77 goals, with 42 at home and 35 away, which gives them an average of 2.0 goals per game. Regarding conceded goals, they let in 58 goals in total, slightly more away (33) than at home (25).\",
                    \"goal_timing\": \"Lazio tends to score most of their goals between the 61st and 75th minute, while they are most vulnerable to conceding in the opening 15 minutes of the game.\",
                    
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Give me multiple different sentences about the coach. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {self.coaches[str(team_id)]}"
                },
            ]
        team_coach_output = self._generate_llama_output(team_coach_messages)
        try:
            model_outputs = json.loads(self.correct_json(self.extract_first_match(team_coach_output)))

            self.metrics.set_parentT_score('coach', model_outputs, self.coaches[str(team_id)])

            return model_outputs
        except:
            self.metrics.set_parentT_score('coach', None, None)
            return None

    def generate_fixture(self):
        """Generates Llama-2 output for fixture."""
        fixture = {}
        information = self.get_fixture_information()
        statistics = self.get_fixture_statistics()

        fixture_information_message = [
                {   
                    "role": "system", 
                    "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentence. Without introduction what you did."
                },
                {
                    "role": "user",
                    "content": "Generate a sentence about the team information. The informations are provided in the JSON. {'name': 'Lazio', 'code': 'LAZ', 'country': 'Italy', 'founded': 1900}"
                },
                {
                    "role": "assistant",
                    "content": "Lazio, proudly bearing the code LAZ, hails from the heart of Italy. With roots tracing back to 1900, they have a rich history in the panorama of world football, steadily leaving their mark through every passing decade."
                },
                {
                    "role": "user",
                    "content": f"Generate a sentence about the fixture information. The informations are provided in the JSON. {information}"
                },
            ]

        fixture['information'] = self._generate_llama_output(fixture_information_message)

        self.metrics.set_parentT_score('fixture_information', fixture['information'], information)

        for team_id in statistics:
            fixture[team_id] = {}
            fixture_statistics_messages = [
                {   
                    "role": "system", 
                    "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentences about statistical facts in JSON format. Without introduction what you did."
                },
                {
                    "role": "user",
                    "content": """Give me multiple different sentences about the team statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {'team_name': 'Lazio', 'fixtures_played_home': 19, 'fixtures_played_away': 19, 'fixtures_wins_home': 10, 'fixtures_wins_away': 8, 'fixtures_draws_home': 6, 'fixtures_draws_away': 4, 'fixtures_loses_home': 3, 'fixtures_loses_away': 7, 'fixtures_loses_total': 10, 'goals_for_total_home': 42, 'goals_for_total_away': 35, 'goals_for_average_home': '2.2', 'goals_for_average_away': '1.8', 'goals_for_average_total': '2.0', 'goals_for_minute_0-15_total': 12, 'goals_for_minute_0-15_percentage': '16.00%', 'goals_for_minute_16-30_total': 7, 'goals_for_minute_16-30_percentage': '9.33%', 'goals_for_minute_31-45_total': 14, 'goals_for_minute_31-45_percentage': '18.67%', 'goals_for_minute_46-60_total': 13, 'goals_for_minute_46-60_percentage': '17.33%', 'goals_for_minute_61-75_total': 15, 'goals_for_minute_61-75_percentage': '20.00%', 'goals_for_minute_76-90_total': 8, 'goals_for_minute_76-90_percentage': '10.67%', 'goals_for_minute_91-105_total': 6,
                    'goals_for_minute_91-105_percentage': '8.00%', 'goals_for_minute_106-120_total': None, 'goals_for_minute_106-120_percentage': None, 'goals_against_total_home': 25, 'goals_against_total_away': 33, 'goals_against_total_total': 58, 'goals_against_average_home': '1.3', 'goals_against_average_away': '1.7', 'goals_against_average_total': '1.5', 'goals_against_minute_0-15_total': 14, 'goals_against_minute_0-15_percentage': '23.33%', 'goals_against_minute_16-30_total': 8, 'goals_against_minute_16-30_percentage': '13.33%', 'goals_against_minute_31-45_total': 8,
                    'goals_against_minute_31-45_percentage': '13.33%', 'goals_against_minute_46-60_total': 7, 'goals_against_minute_46-60_percentage': '11.67%', 'goals_against_minute_61-75_total': 10, 'goals_against_minute_61-75_percentage': '16.67%', 'goals_against_minute_76-90_total': 7, 'goals_against_minute_76-90_percentage': '11.67%', 'goals_against_minute_91-105_total': 6, 'goals_against_minute_91-105_percentage': '10.00%'}
                            """
                },
                {
                    "role": "assistant",
                    "content": """{
                    \"fixtures_played\": \"Lazio has played an equal amount of games at home and away this season, with a total of 19 each, summing up to a total of 38 fixtures overall.\",
                    \"fixtures_wins\": \"In terms of victories, Lazio has a slight home advantage, with 10 wins at home and 8 on the road, bringing their total fixtures wins to 18.\",
                    \"fixtures_draws_loses\": \"Lazio has had 10 draws and 10 losses in total this season, with a marginally higher draws and losses count at home.\",
                    \"goal_statistics\": \"The team scored a total of 77 goals, with 42 at home and 35 away, which gives them an average of 2.0 goals per game. Regarding conceded goals, they let in 58 goals in total, slightly more away (33) than at home (25).\",
                    \"goal_timing\": \"Lazio tends to score most of their goals between the 61st and 75th minute, while they are most vulnerable to conceding in the opening 15 minutes of the game.\",
                    
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Give me multiple different sentences about the fixture statistics. The informations are provided in the JSON. Return the sentences as a python dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'. {statistics[str(team_id)]}"
                },
            ]
            fixture_statistics_output = self._generate_llama_output(fixture_statistics_messages)
            try:
                model_outputs = json.loads(self.correct_json(self.extract_first_match(fixture_statistics_output)))
                
                self.metrics.set_parentT_score('fixture_statistics', model_outputs, statistics[str(team_id)])

                fixture[team_id]['statistics'] = model_outputs
            except:
                self.metrics.set_parentT_score('fixture_statistics', None, None)
                fixture[team_id]['statistics'] = None

        return fixture

    def generate_venue(self):
        """Generates Llama-2 output for venue."""
        venue_messages = [{   
                    "role": "system", 
                    "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary. Just return the sentence. Without introduction what you did."
                },
                {
                    "role": "user",
                    "content": "Generate a sentence about the team information. The informations are provided in the JSON. {'name': 'Lazio', 'code': 'LAZ', 'country': 'Italy', 'founded': 1900}"
                },
                {
                    "role": "assistant",
                    "content": "Lazio, proudly bearing the code LAZ, hails from the heart of Italy. With roots tracing back to 1900, they have a rich history in the panorama of world football, steadily leaving their mark through every passing decade."
                },
                {
                    "role": "user",
                    "content": f"Generate a sentence about the venue information. The informations are provided in the JSON. {self.get_venue_information()}"
                },
            ]
        model_outputs = self._generate_llama_output(venue_messages)
        self.metrics.set_parentT_score('venue_information', model_outputs, self.get_venue_information())   
        return model_outputs
    
    def _generate_llama_output(self, messages):
        """Generates Llama-2 output with the given messages."""
        openai.api_key = "1234"
        openai.api_base = "http://10.180.132.23:8182/v1"

        model_name = "TheBloke/Llama-2-70B-chat-AWQ"
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]
    
    def extract_first_match(self, input_string):
        """Extracts the first dictionary match ('{...}') from the given input string."""
        pattern = r'\{[^}]*\}'
        matches = re.findall(pattern, input_string)
        
        if matches:
            return matches[0]
        else:
            return input_string

    def correct_json(self, json_string):
        """Corrects the given JSON string to be valid."""
        # Remove extra spaces and newlines
        cleaned_json = json_string.replace("\n", "").replace("  ", "")
        
        # Remove double quotes around property names
        cleaned_json = cleaned_json.replace('"{', '{').replace('}"', '}')
        cleaned_json = cleaned_json.replace(',}', '}')
        
        return cleaned_json
    
    def main(self):
        """Main function to create the output json file."""
        output_json = {}
        for team_id in self.team_ids:
            output_json[team_id] = {}
            output_json[team_id]['name'] = self.get_team_name(team_id)
            print(f'Generating information for {self.get_team_name(team_id)}')
            output_json[team_id]['information'] = self.generate_team_information(team_id)

            print(f'Generating statistics for {self.get_team_name(team_id)}')
            output_json[team_id]['statistics'] = self.generate_team_statistics(team_id)

            print(f'Generating news for {self.get_team_name(team_id)}')
            output_json[team_id]['news'] = self.generate_team_news(team_id)

            print(f'Generating injuries information for {self.get_team_name(team_id)}')
            output_json[team_id]['injuries'] = self.generate_team_injuries(team_id)

            print(f'Generating players for {self.get_team_name(team_id)}')
            output_json[team_id]['players'] = self.generate_team_players(team_id)

            print(f'Generating coach for {self.get_team_name(team_id)}')
            output_json[team_id]['coach'] = self.generate_team_coach(team_id)

        # fixture 
        print(f'Generating fixture for {self.get_team_name(self.team_ids[0])} vs {self.get_team_name(self.team_ids[1])}')
        output_json['fixture'] = self.generate_fixture()

        print(f'Generating venue for {self.get_team_name(self.team_ids[0])} vs {self.get_team_name(self.team_ids[1])}')
        output_json['venue'] = self.generate_venue()

        print(f'save output to llama_output.json')
        with open('llama_output.json', 'w', encoding='utf-8') as outfile:
            json.dump(output_json, outfile, indent=4)

        print(f'save parentT and rouge scores')
        self.metrics.save_scores_to_json(path='', filename='scores.json')        

        return output_json
    
if __name__ == "__main__":
    generated_output = LlamaGenerate(team_ids=[487, 489]).main()