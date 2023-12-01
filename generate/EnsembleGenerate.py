import sys
sys.path.append('/Users/tschip/workspace/baa/ruefer/')
import subprocess
import numpy as np
from nltk import ngrams
import pandas as pd
from datetime import datetime
from difflib import SequenceMatcher

from models.logic2text.GPT import GPT
from data_loaders.CSVDataLoader import CSVDataLoader


class EnsembleGenerate():
    def __init__(self, team_ids: list):
        dataloader = CSVDataLoader(team_ids)
        self.player_names = dataloader.get_player_names()
        self.player_information = dataloader.get_player_information()
        self.player_statistics = dataloader.get_player_statistics()
        self.player_injuries = dataloader.get_player_injuries()
        self.team_information = dataloader.get_team_information()
        self.venue_information = dataloader.get_venue_information()
        self.team_statistics = dataloader.get_team_statistics()
        self.player_transfers = dataloader.get_player_transfers()
        self.player_news = dataloader.get_player_news()
        self.team_news = dataloader.get_team_news()
        self.head_to_head = dataloader.get_head_to_head()
        self.home_team = dataloader.get_home_team_id()
        self.players_ids = dataloader.get_players_ids()
        self.team_fixtures = dataloader.get_team_fixtures()
        self.todays_fixture_id = dataloader.get_todays_fixture_id()
        self.fixture_lineup = dataloader.get_fixture_lineup()

        self.vtm = None
        self.gpt = GPT()
        self.team_information_parentT = []
        self.venue_information_parentT = []
        self.player_information_parentT = []
        self.fixture_information_parentT = []

        self.palyer_stats_templates = {
            'the games the player palyed and how he was substituted': [0, 1, 6, 7, 37]
        }
    
    def get_players_ids(self):
        return self.players_ids
    
    def get_player_names(self):
        return self.player_names
    
    def get_team_name(self, team_id):
        if self.head_to_head[self.head_to_head['home_id'] == team_id].shape[0] > 0:
            return self.head_to_head[self.head_to_head['home_id'] == team_id]['home_name'].iloc[0]
        else:
            return self.head_to_head[self.head_to_head['away_id'] == team_id]['away_name'].iloc[0]
    
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
        team_information = self.get_team_information()
        team_information['name_1'] = team_information['name'].apply(lambda x: x.split(' ')[0])
        team_information['name_2'] = team_information['name'].apply(lambda x: x.split(' ')[1] if len(x.split(' ')) > 1 else '<none>')
        team_information.rename(columns={'code': 'code_1', 'country': 'country_1', 'founded': 'founded_1'}, inplace=True)
        input = self._create_VTM_input(team_information[team_information['id'] == team_id].drop(columns=['id']), 'club')
        output = self._generate_VTM(input)
        
        best_result = self.get_best_VTM_output(team_information[team_information['id'] == team_id].drop(columns=['id']), output, 'team_information')

        return best_result
    
    def generate_team_statistics(self, team_id):
        pass

    def generate_team_news(self, team_id):
        pass

    def generate_team_injuries(self, team_id):
        pass

    def generate_team_players(self, team_id):
        team_player = {}
        information = self.get_player_information()[self.get_player_information()['team_id'] == str(team_id)].copy()
        information.drop(columns=['team_id', 'age'], axis=1, inplace=True)
        information.rename(columns={'firstname': 'name_1', 'lastname': 'name_2', 'birthdate': 'birth_date', 'birth_place': 'birth_place_1', 'birth_country': 'birth_place_2', 'games_position': 'position_1', 'name_y': 'current_club'}, inplace=True)
        information['birth_date'] = pd.to_datetime(information['birth_date'], format='%Y-%m-%d')
        information['birth_date'] = information['birth_date'].dt.strftime('%d-%B-%Y')
        players = information[information.id.isin(self.get_players_ids())].dropna(subset=['name_1'], axis=0).id.values.tolist()
        input_string = self._create_VTM_input(information[information.id.isin(self.get_players_ids())].drop(columns=['id']).dropna(subset=['name_1'], axis=0), 'footballer')
        output = self._generate_VTM(input_string)

        while output:
            popped_element = output[:5]
            output = output[6:]
            team_player[players[0]] = {}
            team_player[players[0]]['information'] = self.get_best_VTM_output(information[information['id'] == players[0]].drop(columns=['id']), popped_element, 'player_information')
            team_player[players[0]]['information_metric'] = self.get_player_information_parentT()
            team_player[players[0]]['statistics'] = self.generate_player_statistics(players[0])
            players = players[1:]

        transfers = self.get_player_transfers()
        news = self.get_player_news()

        return team_player
    
    def generate_player_statistics(self, team_id):
        player_stats = {}
        player = self.get_player_statistics()[self.get_player_statistics()['team_id'] == team_id]#.drop(columns=['team_id', 'league_season'])
        player = player.merge(self.get_player_names(), on='player_id', how='right')
        print(player)
        for i in self.palyer_stats_templates:
            player_stats[i] = self.gpt.generate(player, self.palyer_stats_templates[i], i)

        return player_stats

    def generate_team_coach(self, team_id):
        pass

    def generate_fixture(self):
        fixture = {}
        information = self.get_fixture_information()
        information.rename(columns={'time': 'time_1'}, inplace=True)
        input_string = self._create_VTM_input(information, 'game')
        #output = self._generate_VTM(input_string)
        best_result = self.get_best_VTM_output(information, output, 'fixture_information')

        fixture['information'] = best_result
        fixture['information_metric'] = self.get_fixture_information_parentT()

        statistics = self.get_fixture_statistics()
        return fixture

    def generate_venue(self):
        venue = self.get_venue_information()
        venue['name_1'] = venue['name'].apply(lambda x: x.split(' ')[0])
        venue['name_2'] = venue['name'].apply(lambda x: x.split(' ')[1] if len(x.split(' ')) > 1 else '<none>')
        venue.rename(columns={'country': 'country_1', 'city': 'city_1', 'capacity': 'capacity_1'}, inplace=True)
        input_string = self._create_VTM_input(venue.drop(columns=['id']), 'venue')
        output = self._generate_VTM(input_string)

        return self.get_best_VTM_output(venue.drop(columns=['id']), output, 'venue_information')

    def get_team_information(self):
        return self.team_information

    def get_player_information(self):
        return self.player_information
    
    def get_player_statistics(self):
        return self.player_statistics
    
    def get_player_transfers(self):
        return self.player_transfers
    
    def get_player_news(self):
        return self.player_news
    
    def get_fixture_information(self):
        fixtures = self.team_fixtures[list(self.team_fixtures.keys())[0]]
        for fixture in fixtures:
            if fixture['fixture']['id'] == self.todays_fixture_id:
                fixture_split = fixture['fixture']['date'].split('T')
                fixture['fixture']['date'] = datetime.strptime(fixture_split[0], '%Y-%m-%d').strftime('%d-%B-%Y')
                fixture['fixture']['time'] = fixture_split[1].split(':')[0] + ':' + fixture_split[1].split(':')[1]
                fixture['fixture']['name_1'] = fixture['fixture']['referee'].split('. ')[1]
                return pd.DataFrame.from_dict(fixture['fixture'], orient='index').T.drop(columns=['timezone', 'timestamp', 'periods', 'venue', 'id', 'status', 'referee'])

    def get_fixture_lineup(self):
        return self.fixture_lineup
    
    def get_fixture_statistics(self):
        pass

    def get_venue_information(self):
        return self.venue_information
    
    def _create_VTM_input(self, df, table_type):
        cols = df.columns
        f = open('vtm_input.txt', 'w')
        for k in range(len(df)):
            tmp = ''
            artc_title = ''
            for c, i in zip(cols, df.iloc[k]):
                i = str(i).lower()
                i = i.split(' ')
                for id, n in enumerate(i):
                    if c == 'birth_date' or c == 'date':
                        n = n.split('-')
                        for id, x in enumerate(n):
                            tmp += f'{c}_{id + 1}:{x}{"." if id==0 else ""}\t'
                    else:
                        if not '_' in c[-2:]:
                            tmp += f'{c}_{id + 1}:{n}\t'
                        else:
                            tmp += f'{c}:{n}\t'
                    if (c == 'name_1') | (c == 'name_2'):
                        artc_title += f'article_title_{c[-1]}:{n}\t'
            input = tmp + artc_title + f'article_title_3:{table_type}\n'
            f.write(input.replace("nan", "<none>").replace("none", "<none>").replace("n/a", "<none>"))
        f.close()
        return 'vtm_input.txt'
    
    def _generate_VTM(self, input):
        command = [
            'python', '../../VariationalTemplateMachine/generate.py',
            '-data', '../../VariationalTemplateMachine/data/Wiki',
            '-max_vocab_cnt', '50000',
            '-load', '../../VariationalTemplateMachine/models/model.pth',
            '-various_gen', '5',
            '-mask_prob', '0.0',
            '-cuda',
            '-decode_method', 'temp_sample',
            '-sample_temperature', '0.2',
            '-gen_to_fi', f'{input.split(".")[0]}_generated.txt'
        ]

        # Execute the command
        #process = subprocess.run(command, capture_output=True, text=True)
        
        # Check for errors
        #if process.returncode != 0:
            #print(f"Error: {process.stderr}")
            #return None
        
        # Parse the output from the subprocess
        a = open(f'{input.split(".")[0]}_generated.txt', 'r+')
        return a.readlines()
    
    def get_best_VTM_output(self, input, output, source):
        input_list = input.values.tolist()[0]
        high_score = 0
        best_result = ''
        if source == 'team_information':
            for i in output:
                i = i.replace('\n', '').replace('-lrb-', '').replace('-rrb-', '').replace('``', '').replace("''", '')
                score = self.parent_t_score(i, input_list)
                self.team_information_parentT.append(score)
                if score >= high_score:
                    high_score = score
                    best_result = i
        elif source == 'venue_information':
            for i in output:
                i = i.replace('\n', '').replace('-lrb-', '').replace('-rrb-', '').replace('``', '').replace("''", '')
                score = self.parent_t_score(i, input_list)
                self.venue_information_parentT.append(score)
                if score >= high_score:
                    high_score = score
                    best_result = i
        elif source == 'player_information':
            for i in output:
                i = i.replace('\n', '').replace('-lrb-', '').replace('-rrb-', '').replace('``', '').replace("''", '')
                score = self.parent_t_score(i, input_list)
                self.player_information_parentT.append(score)
                if score >= high_score:
                    high_score = score
                    best_result = i

        elif source == 'fixture_information':
            for i in output:
                i = i.replace('\n', '').replace('-lrb-', '').replace('-rrb-', '').replace('``', '').replace("''", '')
                score = self.parent_t_score(i, input_list)
                self.fixture_information_parentT.append(score)
                if score >= high_score:
                    high_score = score
                    best_result = i

        return best_result

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
