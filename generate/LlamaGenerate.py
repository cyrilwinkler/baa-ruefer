import sys
sys.path.append('/Users/tschip/workspace/baa/baa-ruefer/')
#sys.path.append('/home/jovyan/baa-ruefer/')
import subprocess
import numpy as np
from nltk import ngrams
import pandas as pd
from datetime import datetime
from difflib import SequenceMatcher
import openai
import json
import time

from data_loaders.JSONDataLoader import JSONDataLoader


class LlamaGenerate():
    def __init__(self, team_ids: list, gpt_api_key=None, requests_api=None):
        dataloader = JSONDataLoader(team_ids)
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

        self.team_information_parentT = []
        self.venue_information_parentT = []
        self.player_information_parentT = []
        self.fixture_information_parentT = []

        self.gpt_api_key = gpt_api_key
    
    def get_players_ids(self):
        return self.players_ids
    
    def get_player_names(self):
        return self.player_names
    
    def get_team_name(self, team_id):
        for fixture_key in dict(sorted(self.head_to_head.items())):
            if self.head_to_head[fixture_key]['home_id'] == team_id:
                return self.head_to_head[fixture_key]['home_name']
            else:
                return self.head_to_head[fixture_key]['away_name']
    
    def get_team_information_parentT(self):
        return self.team_information_parentT[-1]
    
    def get_player_information_parentT(self):
        return self.player_information_parentT[-1]
    
    def get_venue_information_parentT(self):
        return self.venue_information_parentT[-1]
    
    def get_fixture_information_parentT(self):
        return self.fixture_information_parentT[-1]
    
    def get_overall_team_information_parentT(self):
        return sum(self.team_information_parentT) / len(self.team_information_parentT)

    def get_overall_player_information_parentT(self):
        return sum(self.player_information_parentT) / len(self.player_information_parentT)
    
    def get_overall_venue_information_parentT(self):
        return sum(self.venue_information_parentT) / len(self.venue_information_parentT)
    
    def get_overall_fixture_information_parentT(self):
        return sum(self.fixture_information_parentT) / len(self.fixture_information_parentT)
    
    def generate_team_information(self, team_id):
        return self._generate_GPT_output(f"Generate a sentence about the team information. The informations are provided in the JSON. {self.get_team_information()[team_id]}")
    
    def generate_team_statistics(self, team_id):
        team_statistics_output = self._generate_GPT_output(f"Give me multiple different sentences about the team statistics. The informations are provided in the JSON.  For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'{self.team_statistics[team_id]}")
        try:
            return json.loads(team_statistics_output)
        except:
            return team_statistics_output

    def generate_team_news(self, team_id):
        pass

    def generate_team_injuries(self, team_id):
        fixture_id = self.todays_fixture_id
        injuries = self.player_injuries[str(team_id)]
        injuries_dict = {}
        outputs = {}
        for player_id in injuries:
            if injuries[player_id]['fixture_id'] == fixture_id:
                injuries_dict[player_id] = injuries[player_id]
                injuries_dict[player_id]['player_name'] = self.get_player_names()[team_id][player_id]
                del injuries_dict[player_id]['fixture_id']
                outputs[player_id] = self._generate_GPT_output(f"Generate a sentence about the player and the injury for the fixture. The information are provided in the JSON. {injuries_dict[player_id]['player_name']}")

        return outputs

    def generate_team_players(self, team_id):
        players = {}
        information = self.get_player_information()[str(team_id)]
        statistics = self.get_player_statistics()[str(team_id)]
        transfers = self.get_player_transfers()
        transfer_dict = {}
        news = self.get_player_news()
        counter = 1
        for player_id in self.get_player_ids_from_fixture(team_id):
            players[player_id] = {}
            try:
                del information[player_id]['injured']
                del information[player_id]['name']
            except:
                pass
            player_information_output = self._generate_GPT_output(f"Give me sentences about the player information. The information are provided in the JSON. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'{information[player_id]}")
            try:
                players[player_id]['information'] = json.loads(player_information_output)
            except:
                players[player_id]['information'] = player_information_output

            statistics[player_id]['player_name'] = self.get_player_names()[team_id][player_id]
            player_statistics_output = self._generate_GPT_output(f"Give me multiple different sentences about the player statistics. The informations are provided in the JSON. Return the sentences as a dictionary. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'{statistics[player_id]}")
            try:
                players[player_id]['statistics'] = json.loads(player_statistics_output)
            except:
                players[player_id]['statistics'] = player_statistics_output

            try:
                transfer_dict[player_id] = {}
                transfer_dict[player_id]['player_name'] = self.get_player_names()[team_id][player_id]
                transfer_dict[player_id]['transfers'] = transfers[str(player_id)]
                player_transfers = self._generate_GPT_output(f"Give me multiple different sentences about the player transfer history. The informations are provided in the JSON. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'{transfer_dict[player_id]}")
                try:
                    players[player_id]['transfers'] = json.loads(player_transfers)
                except:
                    players[player_id]['transfers'] = player_transfers
            except:
                players[player_id]['transfers'] = 'No transfers for this player'

            if str(player_id) in news:
                players[player_id]['news'] = {}
                for n in news[str(player_id)].items():
                    players[player_id]['news'][n[0]] = self._generate_GPT_output(f"Summarize the news article. The article are provided in the JSON. Format it as a normal text. The text must be in english. {n[1]}")
            else:
                players[player_id]['news'] = None
            print(f'Player {counter} of {len(self.get_player_ids_from_fixture(team_id))}')
            counter += 1
            if counter % 10 == 0:
                time.sleep(3)
        return players

    def generate_team_coach(self, team_id):
        team_coach_output = self._generate_GPT_output(f"Give me sentences about the coach. The information are provided in the JSON. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'{self.coaches[str(team_id)]}")
        try:
            return json.loads(team_coach_output)
        except:
            return team_coach_output

    def generate_fixture(self):
        fixture = {}
        information = self.get_fixture_information()
        statistics = self.get_fixture_statistics()

        fixture['information'] = self._generate_GPT_output(f"Give me sentences about the fixture information. The information are provided in the JSON. {information}")

        for team_id in statistics:
            fixture[team_id] = {}
            fixture_statistics_output = self._generate_GPT_output(f"Give me multiple different sentences about the fixture statistics. The informations are provided in the JSON. For each fact create a key with the topic and the sentecnes as value. Generate text without \ and '\n'{statistics[str(team_id)]}")
            try:
                fixture[team_id]['statistics'] = json.loads(fixture_statistics_output)
            except:
                fixture[team_id]['statistics'] = fixture_statistics_output

        return fixture

    def generate_venue(self):
        return self._generate_GPT_output(f"Give me sentences about the venue information. The information are provided in the JSON. {self.get_venue_information()}")

    def get_team_information(self):
        return self.team_information

    def get_player_information(self):
        return self.player_information
    
    def get_player_statistics(self):
        return self.player_statistics
    
    def get_player_transfers(self):
        return self.player_transfers
    
    def get_player_injuires(self):
        return self.player_injuries
    
    def get_player_news(self):
        player_news_detail = {}
        for player_id in self.player_news:
            player_news_detail[player_id] = {}
            for news in self.player_news[player_id]:
                if news['id'] in self.news_details:
                    player_news_detail[player_id][news['newsHeadline']] = result_string = ''.join(value for key, value in sorted(self.news_details[news['id']]['text'].items()))
        player_news_detail = {key: value for key, value in player_news_detail.items() if value}
        return player_news_detail
    
    def get_team_coach(self):
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
        return self.todays_fixture_id
    
    def get_fixture_information(self):
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
        return self.fixture_lineup
    
    def get_player_ids_from_fixture(self, team_id):
        all_ids = set()
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
        return self.fixture_statistics

    def get_venue_information(self):
        for venue_id in self.venue_information:
            if self.venue_information[venue_id]['name'] == self.get_fixture_information()['fixture_venue']:
                try:
                    del self.venue_information[venue_id]['team_id']
                except:
                    pass
                return self.venue_information[venue_id]
    
    def _generate_GPT_output(self, input):
        client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=self.gpt_api_key,
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a sports journalist for football (soccer) respond in sentences that can be used in live commentary"},
                {"role": "user", "content": f"{input}"},
            ],
            model="gpt-4",
            temperature=0.9,
        )
        print(response)
        return response.choices[0].message.content

    def word_overlap_model(self, g, table_lexical_items):
        return sum(1 for token in g if token in table_lexical_items) / len(g)

    def entailed_precision(self, generated_ngrams, table_lexical_items):
        total_entailment_prob = 0
        total_generated_ngrams = 0
        for g in generated_ngrams:
            total_entailment_prob += self.word_overlap_model(g, table_lexical_items)
            total_generated_ngrams += len(g)
        return total_entailment_prob / total_generated_ngrams if total_generated_ngrams > 0 else 0

    def geometric_average(self, scores):
        return np.exp(np.mean(np.log([score + 1e-10 for score in scores]))) if len(scores) > 0 else 0

    def longest_common_subsequence(self, x, y):
        x = str(x)
        y = str(y)
        seq_matcher = SequenceMatcher(None, x, y)
        match = seq_matcher.find_longest_match(0, len(x), 0, len(y))
        return match.size

    def entailment_recall(self, table_records, generated_text):
        total_recall = sum(self.longest_common_subsequence(record, generated_text) for record in table_records)
        return total_recall / len(table_records) if len(table_records) > 0 else 0

    def parent_t_score(self, generated_text, table_records):
        precision_scores = [self.entailed_precision(ngrams(generated_text.split(), n), set(table_records)) for n in range(1)]
        entailed_precision_score = self.geometric_average(precision_scores)
        recall_score = self.entailment_recall(table_records, generated_text)
        parent_t = (2 * entailed_precision_score * recall_score) / (entailed_precision_score + recall_score) if (entailed_precision_score + recall_score) > 0 else 0
        return parent_t
    
    def main(self):
        output_json = {}

        output_json[self.team_ids[0]] = {}
        output_json[self.team_ids[0]]['name'] = self.get_team_name(self.team_ids[0])
        output_json[self.team_ids[0]]['information'] = self.generate_team_information(self.team_ids[0])
        output_json[self.team_ids[0]]['statistics'] = self.generate_team_statistics(self.team_ids[0])
        output_json[self.team_ids[0]]['news'] = self.generate_team_news(self.team_ids[0])
        output_json[self.team_ids[0]]['injuries'] = self.generate_team_injuries(self.team_ids[0])
        output_json[self.team_ids[0]]['players'] = self.generate_team_players(self.team_ids[0])
        output_json[self.team_ids[0]]['coach'] = self.generate_team_coach(self.team_ids[0])

        # team 489
        output_json[self.team_ids[1]] = {}
        output_json[self.team_ids[1]]['name'] = self.get_team_name(self.team_ids[1])
        output_json[self.team_ids[1]]['information'] = self.generate_team_information(self.team_ids[1])
        output_json[self.team_ids[1]]['statistics'] = self.generate_team_statistics(self.team_ids[1])
        output_json[self.team_ids[1]]['news'] = self.generate_team_news(self.team_ids[1])
        output_json[self.team_ids[1]]['injuries'] = self.generate_team_injuries(self.team_ids[1])
        output_json[self.team_ids[1]]['players'] = self.generate_team_players(self.team_ids[1])
        output_json[self.team_ids[1]]['coach'] = self.generate_team_coach(self.team_ids[1])

        # fixture 
        output_json['fixture'] = self.generate_fixture()
        output_json['venue'] = self.generate_venue()

        with open('output.json', 'w') as outfile:
            json.dump(output_json, outfile, indent=4)

        return output_json

