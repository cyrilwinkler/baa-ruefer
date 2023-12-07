import sys
sys.path.append('/Users/tschip/workspace/baa/baa-ruefer/')
#sys.path.append('/home/jovyan/baa-ruefer/')
#from openai import OpenAI
import json
import time
import openai

#from GPTGenerate import GPTGenerate


class OutputJSON():
    def __init__(self, team_ids: list, gpt_api_key=None, requests_api=None):
        self.team_ids = team_ids
        self.gpt_api_key = gpt_api_key
        self.requests_api = requests_api
        with open('output_2.json', 'r') as fp:
            self.input_json = json.load(fp)

    def create_output_json(self, commentary_flavor: str):
        output_json = {}
        for team_id in list(self.input_json.keys())[:2]:
            print(f'Generating output for team {team_id}')

            output_json[team_id] = {}
            output_json[team_id]['team_name'] = self.input_json[team_id]['name']
            
            print(f'Generating output for team {team_id} information')
            team_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['information']}"
            team_information_output = self.generate_gpt_flavor(team_information_input)
            try:
                output_json[team_id]['information'] = json.loads(team_information_output)
            except:
                print(team_information_output)
                output_json[team_id]['information'] = self.format_to_json(team_information_output)
            print(f'Generated output for team {output_json[team_id]["information"]}')
            
            print(f'Generating output for team {team_id} statistics')
            output_json[team_id]['statistics'] = {}
            for statistic in self.input_json[team_id]['statistics']:
                print(f'Generating output for team {team_id} statistics {statistic}')
                team_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['statistics'][statistic]}"
                team_statistics_output = self.generate_gpt_flavor(team_statistics_input)
                try:
                    output_json[team_id]['statistics'][statistic] = json.loads(team_statistics_output)
                except:
                    output_json[team_id]['statistics'][statistic] = self.format_to_json(team_statistics_output)

            if self.input_json[team_id]['news'] != None:
                print(f'Generating output for team {team_id} news')
                output_json[team_id]['news'] = {}
                for news in self.input_json[team_id]['news']:
                    team_news_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['news'][news]}"
                    team_news_output = self.generate_gpt_flavor(team_news_input)
                    try:
                        output_json[team_id]['news'][news] = json.loads(team_news_output)
                    except:
                        output_json[team_id]['news'][news] = self.format_to_json(team_news_output)

            if self.input_json[team_id]['injuries'] != {}:
                output_json[team_id]['injuries'] = {}
                print(f'Generating output for team {team_id} injuries')
                for player_id in self.input_json[team_id]['injuries']:
                    print(f'Generating output for player {player_id}')
                    team_injuries_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['injuries'][player_id]}"
                    team_injuries_output = self.generate_gpt_flavor(team_injuries_input)
                    try:
                        output_json[team_id]['injuries'][player_id] = json.loads(team_injuries_output)
                    except:
                        output_json[team_id]['injuries'][player_id] = self.format_to_json(team_injuries_output)

            print(f'Generating output for team {team_id} players')
            output_json[team_id]['players'] = {}
            counter = 1
            n_players = len(self.input_json[team_id]['players'])
            for player_id in self.input_json[team_id]['players']:
                print(f'Generating output for player {player_id}')
                print(f'Player {counter} of {n_players}')
                output_json[team_id]['players'][player_id] = {}
                
                print(f'Generating output for player {player_id} information')
                player_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['information']}"
                player_information_output = self.generate_gpt_flavor(player_information_input)
                try:
                    output_json[team_id]['players'][player_id]['information'] = json.loads(player_information_output)
                except:
                    output_json[team_id]['players'][player_id]['information'] = self.format_to_json(player_information_output)

                print(f'Generating output for player {player_id} statistics')
                output_json[team_id]['players'][player_id]['statistics'] = {}
                if type(self.input_json[team_id]['players'][player_id]['statistics']) != str:
                    for statistic in self.input_json[team_id]['players'][player_id]['statistics']:
                        print(f'Generating output for player {player_id} statistics {statistic}')
                        player_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['statistics'][statistic]}"
                        player_statistics_output = self.generate_gpt_flavor(player_statistics_input)
                        try:
                            output_json[team_id]['players'][player_id]['statistics'][statistic] = json.loads(player_statistics_output)
                        except:
                            output_json[team_id]['players'][player_id]['statistics'][statistic] = self.format_to_json(player_statistics_output)
                else:
                    player_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['statistics']}"
                    output_json[team_id]['players'][player_id]['statistics'] = self.generate_gpt_flavor(player_statistics_input)

                print(f'Generating output for player {player_id} transfers')
                output_json[team_id]['players'][player_id]['transfers'] = {}
                if type(self.input_json[team_id]['players'][player_id]['transfers']) != str:
                    for transfer in self.input_json[team_id]['players'][player_id]['transfers']:
                        print(f'Generating output for player {player_id} transfers {transfer}')
                        player_transfers_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['transfers'][transfer]}"
                        player_transfers_output = self.generate_gpt_flavor(player_transfers_input)
                        try:
                            output_json[team_id]['players'][player_id]['transfers'][transfer] = json.loads(player_transfers_output)
                        except:
                            output_json[team_id]['players'][player_id]['transfers'][transfer] = self.format_to_json(player_transfers_output)
                else:
                    player_transfers_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['transfers']}"
                    output_json[team_id]['players'][player_id]['transfers'] = self.generate_gpt_flavor(player_transfers_input)

                if self.input_json[team_id]['players'][player_id]['news'] != None:
                    print(f'Generating output for player {player_id} news')
                    output_json[team_id]['players'][player_id]['news'] = {}
                    if type(self.input_json[team_id]['players'][player_id]['news']) != str:
                        for news in self.input_json[team_id]['players'][player_id]['news']:
                            print(f'Generating output for player {player_id} news {news}')
                            player_news_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['news'][news]}"
                            output_json[team_id]['players'][player_id]['news'][news] = self.generate_gpt_flavor(player_news_input)
                    else:
                        player_news_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key.{self.input_json[team_id]['players'][player_id]['news']}"
                        player_news_output = self.generate_gpt_flavor(player_news_input)
                        try:
                            output_json[team_id]['players'][player_id]['news'] = json.loads(player_news_output)
                        except:
                            output_json[team_id]['players'][player_id]['news'] = self.format_to_json(player_news_output)
            
                counter += 1
                with open('json_output_dump.json', 'w', encoding='UTF-8') as fp:
                    json.dump(output_json, fp, indent=4, ensure_ascii=False)

            print(f'Generating output for team {team_id} coach')
            output_json[team_id]['coach'] = {}
            if type(self.input_json[team_id]['coach']) != str:
                for coach_information in self.input_json[team_id]['coach']:
                    print(f'Generating output for team {team_id} coach {coach_information}')
                    player_coaches_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['coach'][coach_information]}"
                    player_coaches_output = self.generate_gpt_flavor(player_coaches_input)
                    try:
                        output_json[team_id]['coach'][coach_information] = json.loads(player_coaches_output)
                    except:
                        output_json[team_id]['coach'][coach_information] = self.format_to_json(player_coaches_output)
            else:
                player_coaches_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key.{self.input_json[team_id]['coach']}"
                output_json[team_id]['coach'] = self.generate_gpt_flavor(player_coaches_input)        
        
        print(f'Generating output for fixture')
        output_json['fixture'] = {}
        for id in self.input_json['fixture']:
            output_json['fixture'][id] = {}
            print(f'Generating output for {id}')
            if id == 'information':
                fixture_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json['fixture']['information']}"
                fixture_information_output = self.generate_gpt_flavor(fixture_information_input)
                try:
                    output_json['fixture'][id] = json.loads(fixture_information_output)
                except:
                    output_json['fixture'][id] = self.format_to_json(fixture_information_output)
            else:
                output_json['fixture'][id]['statistics'] = {}
                if type(self.input_json['fixture'][id]['statistics']) != str:
                    for statistic in self.input_json['fixture'][id]['statistics']:
                        print(f'Generating output for {id} {statistic}')
                        fixture_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key.{self.input_json['fixture'][id]['statistics'][statistic]}"
                        fixture_statistics_output = self.generate_gpt_flavor(fixture_statistics_input)
                        try:
                            output_json['fixture'][id]['statistics'][statistic] = json.loads(fixture_statistics_output)
                        except:
                            output_json['fixture'][id]['statistics'][statistic] = self.format_to_json(fixture_statistics_output)
                else:
                    fixture_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key.{self.input_json['fixture'][id]['statistics']}"
                    output_json['fixture'][id]['statistics'] = self.generate_gpt_flavor(fixture_statistics_input)

        print(f'Generating output for venue')
        venue_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key.{self.input_json['venue']}"
        output_json['venue'] = self.generate_gpt_flavor(venue_information_input)

        return output_json

    def generate_gpt_flavor(self, input):
        ## point openai library to internal endpoint
        openai.api_key = "1234"
        openai.api_base = "http://10.180.132.23:8180/v1"

        ## specify the used model
        messages = [
            {   
                "role": "system", 
                "content": "You get a text from a sports journalist for live commentary. Take the text and create three outputs with different length. A short in one sentence. A middle one with 2 to 3 sentences. And a long one. Write the text with the provided flavor. And provide it as a json. No other text is allowed."
            },
            {
                "role": "user",
                "content": "Create three outputs in different length, with the flavor humorous. Provide the output as a json. The length title is the key. Do not any other text than the json. 'Ladies and gentlemen, turning our focus to team Lazio, hailing all the way from the beautiful country of Italy. With a rich history traced back to their founding in 1900, they\'ve been synonymous with Italy\'s football prowess, and they\'re here today, displaying their prowess on the pitch, sporting the proud team code \'LAZ\'.'}"
            },
            {
                "role": "assistant",
                "content": "{\"short\": \"Lazio, the Italian team with a code as lazy as LAZ, has been kicking the football around since 1900!\", \"middle\": \"Nope, it's not a lazy Sunday, we're talking about Lazio, also known as LAZ, a football team all the way from Italy. These guys have been showing off their footwork on the field for well over a century now since 1900.\", \"long\": \"Put your espresso aside and let's have a chat about team Lazio. No, they're not a bunch of lazy guys despite their code name LAZ. They are, in fact, one of Italy's most historical football teams. Born in 1900, they've been around longer than the pizza slice you're considering right now. You could say they’ve been twirling the football around their feet just about as long as Italians have been twirling spaghetti on their forks. More than a century of legacy, and they're still going strong, much like that extra shot of espresso in your coffee!\"}"
            },
            {
                "role": "user",
                "content": f"{input}"
            },
        ]

        model_name = "TheBloke/Llama-2-13B-chat-AWQ"
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=0,
        )

        print(f'Response: {response["choices"][0]["message"]["content"]}')
        return response["choices"][0]["message"]["content"]
    
    def format_to_json(self, input):
        ## point openai library to internal endpoint
        openai.api_key = "1234"
        openai.api_base = "http://10.180.132.23:8180/v1"

        ## specify the used model
        messages = [
            {   
                "role": "system", 
                "content": "You string with an JSON and a sentence before the actual JSON. Remove the sentence and provide the formatted JSON as a string."
            },
            {
                "role": "user",
                "content": f"Format string to JSON string: {input}"
            },
        ]

        model_name = "TheBloke/Llama-2-13B-chat-AWQ"
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=0,
        )

        print(f'Response: {response["choices"][0]["message"]["content"]}')
        return response["choices"][0]["message"]["content"]
    

if __name__ == "__main__":
    team_ids = [487, 489]
    output_json = OutputJSON(team_ids)#, "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")
    
    for flavor in ['sarcastic', 'serious', 'neutral', 'for the team and player', 'against the team and player', 'analytical', 'emotional', 'educational', 'upbeat and energetic']:
        output_file = output_json.create_output_json(flavor)

        with open('final_output_{flavor}.json', 'w') as fp:
            json.dump(output_file, fp, indent=4)

            