from rouge import Rouge
from nltk import ngrams
from difflib import SequenceMatcher
import numpy as np
import json

class Metrics():
    """
    Class for calculating the ROUGE and PARENT-T metrics.
    """
    def __init__(self):
        self.rouge = Rouge()
        self.team_information_parentT = []
        self.team_statistics_parentT = []
        self.team_injuries_parentT = []
        self.venue_information_parentT = []
        self.player_information_parentT = []
        self.player_statistics_parentT = []
        self.player_transfers_parentT = []
        self.fixture_information_parentT = []
        self.fixture_statistics_parentT = []
        self.coach_parentT = []
        self.rouge_scores_1 = []
        self.rouge_scores_2 = []
        self.rouge_scores_l = []

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
        precision_scores = [self.entailed_precision(ngrams(generated_text.split(), n), set(table_records)) for n in range(1, 6)]
        entailed_precision_score = self.geometric_average(precision_scores)
        recall_score = self.entailment_recall(table_records, generated_text)
        parent_t = (2 * entailed_precision_score * recall_score) / (entailed_precision_score + recall_score) if (entailed_precision_score + recall_score) > 0 else 0
        return parent_t
    
    def system_level_parent_t_score(self, model_outputs, table_records_list):
        total_parent_t_score = sum(self.parent_t_score(generated_text, table_records) for generated_text, table_records in zip(model_outputs, table_records_list))
        return total_parent_t_score / len(model_outputs) if len(model_outputs) > 0 else 0

    def calculate_rouge_scores(self, hypothesis, reference):
        if hypothesis != None:
            scores = self.rouge.get_scores(hypothesis, reference)
            self.rouge_scores_1.append(scores[0]['rouge-1']['f'])
            self.rouge_scores_2.append(scores[0]['rouge-2']['f'])
            self.rouge_scores_l.append(scores[0]['rouge-l']['f'])
        else:  
            self.rouge_scores_1.append(0)
            self.rouge_scores_2.append(0)
            self.rouge_scores_l.append(0)

    def create_list_of_table_records(self, table_records):
        li = []
        for item in table_records.items():
            for i in str(item[1]).split(' '):
                li.append(i)
        return li
    
    def create_list_of_generated_text(self, generated_text):
        output_strings = []
        for item in generated_text:
            output_strings.append(generated_text[item])
    
    def set_parentT_score(self, score_type, generated_text, table_record):
        if score_type == "team_information":
            self.team_information_parentT.append(self.parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
        
        elif score_type == "team_statistics":
            if type(generated_text) == json:
                generated_text = self.create_list_of_generated_text(generated_text)
                self.team_statistics_parentT.append(self.system_level_parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
            else:
                self.team_statistics_parentT.append(0)
        
        elif score_type == "team_injuries":
            self.team_injuries_parentT.append(self.parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
        
        elif score_type == "player_information":
            if type(generated_text) == json:
                generated_text = self.create_list_of_generated_text(generated_text)
                self.player_information_parentT.append(self.system_level_parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
            else:
                self.player_information_parentT.append(0)
        
        elif score_type == "player_statistics":
            if type(generated_text) == json:
                generated_text = self.create_list_of_generated_text(generated_text)
                self.player_statistics_parentT.append(self.system_level_parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
            else:
                self.player_statistics_parentT.append(0)
        
        elif score_type == "player_transfers":
            if type(generated_text) == json:
                generated_text = self.create_list_of_generated_text(generated_text)
                self.player_transfers_parentT.append(self.system_level_parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
            else:
                self.player_transfers_parentT.append(0)
        
        elif score_type == "fixture_information":
            self.fixture_information_parentT.append(self.parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
        
        elif score_type == "fixture_statistics":
            if type(generated_text) == json:
                generated_text = self.create_list_of_generated_text(generated_text)
                self.fixture_statistics_parentT.append(self.system_level_parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
        
        elif score_type == "coach":
            if type(generated_text) == json:
                generated_text = self.create_list_of_generated_text(generated_text)
                self.coach_parentT.append(self.system_level_parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
            else:
                self.coach_parentT.append(0)
        
        elif score_type == "venue_information":
            self.venue_information_parentT.append(self.parent_t_score(generated_text, self.create_list_of_table_records(table_record)))
    
    def get_overall_parentT(self, score_type):
        if score_type == "team_information":
            return sum(self.team_information_parentT) / len(self.team_information_parentT) if len(self.team_information_parentT) > 0 else None
        elif score_type == "team_statistics":
            return sum(self.team_statistics_parentT) / len(self.team_statistics_parentT) if len(self.team_statistics_parentT) > 0 else None        
        elif score_type == "team_injuries":
            return sum(self.team_injuries_parentT) / len(self.team_injuries_parentT) if len(self.team_injuries_parentT) > 0 else None        
        elif score_type == "player_information":
            return sum(self.player_information_parentT) / len(self.player_information_parentT) if len(self.player_information_parentT) > 0 else None        
        elif score_type == "player_statistics":
            return sum(self.player_statistics_parentT) / len(self.player_statistics_parentT) if len(self.player_statistics_parentT) > 0 else None        
        elif score_type == "player_transfers":
            return sum(self.player_transfers_parentT) / len(self.player_transfers_parentT) if len(self.player_transfers_parentT) > 0 else None        
        elif score_type == "fixture_information":
            return sum(self.fixture_information_parentT) / len(self.fixture_information_parentT) if len(self.fixture_information_parentT) > 0 else None        
        elif score_type == "fixture_statistics":
            return sum(self.fixture_statistics_parentT) / len(self.fixture_statistics_parentT) if len(self.fixture_statistics_parentT) > 0 else None        
        elif score_type == "coach":
            return sum(self.coach_parentT) / len(self.coach_parentT) if len(self.coach_parentT) > 0 else None        
        elif score_type == "venue_information":
            return sum(self.venue_information_parentT) / len(self.venue_information_parentT) if len(self.venue_information_parentT) > 0 else None
     
    def get_overall_rouge_scores(self):
        return (sum(self.rouge_scores_1) / len(self.rouge_scores_1)) if len(self.rouge_scores_1) > 0 else None, (sum(self.rouge_scores_2) / len(self.rouge_scores_2)) if len(self.rouge_scores_2) > 0 else None, (sum(self.rouge_scores_l) / len(self.rouge_scores_l)) if len(self.rouge_scores_l) > 0 else None

    def save_scores_to_json(self, path, filename):
        with open(f'{path}{filename}', 'w') as score_file:
            json.dump({
                'team_information': self.get_overall_parentT('team_information'),
                'team_statistics': self.get_overall_parentT('team_statistics'),
                'team_injuries': self.get_overall_parentT('team_injuries'),
                'player_information': self.get_overall_parentT('player_information'),
                'player_statistics': self.get_overall_parentT('player_statistics'),
                'player_transfers': self.get_overall_parentT('player_transfers'),
                'coach': self.get_overall_parentT('coach'),
                'fixture_information': self.get_overall_parentT('fixture_information'),
                'fixture_statistics': self.get_overall_parentT('fixture_statistics'),
                'venue_information': self.get_overall_parentT('venue_information'),
                'news_rouge_1': self.get_overall_rouge_scores()[0],
                'news_rouge_2': self.get_overall_rouge_scores()[1],
                'news_rouge_l': self.get_overall_rouge_scores()[2]
            }, score_file, indent=4)