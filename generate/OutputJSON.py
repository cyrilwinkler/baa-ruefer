import sys
sys.path.append('/Users/tschip/workspace/baa/baa-ruefer/')
#sys.path.append('/home/jovyan/baa-ruefer/')
from openai import OpenAI
import json
import time

from GPTGenerate import GPTGenerate


class OutputJSON():
    def __init__(self, team_ids: list, gpt_api_key=None, requests_api=None):
        self.team_ids = team_ids
        self.gpt_api_key = gpt_api_key
        self.requests_api = requests_api
        self.input_json = GPTGenerate(self.team_ids, self.gpt_api_key, self.requests_api).main()

    def create_output_json(self, commentary_flavor: str):
        output_json = {}
        for team_id in list(self.input_json.keys())[:2]:
            output_json[team_id] = {}
            output_json[team_id]['team_name'] = self.input_json[team_id]['name']

            team_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['information']}"
            output_json[team_id]['information'] = self.generate_gpt_flavor(team_information_input)

            output_json[team_id]['statistics'] = {}
            for statistic in self.input_json[team_id]['statistics']:
                team_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['statistics'][statistic]}"
                output_json[team_id]['statistics'][statistic] = self.generate_gpt_flavor(team_statistics_input)

            if self.input_json[team_id]['news'] != None:
                output_json[team_id]['news'] = {}
                for news in self.input_json[team_id]['news']:
                    team_news_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['news'][news]}"
                    output_json[team_id]['news'][news] = self.generate_gpt_flavor(team_news_input)

            if self.input_json[team_id]['injuries'] != {}:
                output_json[team_id]['injuries'] = {}
                for player_id in self.input_json[team_id]['injuries']:
                    team_injuries_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['injuries'][player_id]}"
                    output_json[team_id]['injuries'][player_id] = self.generate_gpt_flavor(team_injuries_input)

            output_json[team_id]['players'] = {}
            for player_id in self.input_json[team_id]['players']:
                output_json[team_id]['players'][player_id] = {}

                player_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['information']}"
                output_json[team_id]['players'][player_id]['information'] = self.generate_gpt_flavor(player_information_input)

                output_json[team_id]['players'][player_id]['statistics'] = {}
                for statistic in self.input_json[team_id]['players'][player_id]['statistics']:
                    player_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['statistics'][statistic]}"
                    output_json[team_id]['players'][player_id]['statistics'][statistic] = self.generate_gpt_flavor(player_statistics_input)
                
                time.sleep(1)

                output_json[team_id]['players'][player_id]['transfers'] = {}
                for transfer in self.input_json[team_id]['players'][player_id]['transfers']:
                    player_transfers_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['transfers'][transfer]}"
                    output_json[team_id]['players'][player_id]['transfers'][transfer] = self.generate_gpt_flavor(player_transfers_input)

                time.sleep(1)

                if self.input_json[team_id]['players'][player_id]['news'] != None:
                    output_json[team_id]['players'][player_id]['news'] = {}
                    for news in self.input_json[team_id]['players'][player_id]['news']:
                        player_news_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['players'][player_id]['news'][news]}"
                        output_json[team_id]['players'][player_id]['news'][news] = self.generate_gpt_flavor(player_news_input)
                
                time.sleep(1)

                output_json[team_id]['coach'] = {}
                for coach_information in self.input_json[team_id]['coach']:
                    player_coaches_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json[team_id]['coach'][coach_information]}"
                    output_json[team_id]['coach'][coach_information] = self.generate_gpt_flavor(player_coaches_input)
        
        output_json['fixture'] = {}
        for id in self.input_json['fixture']:
            if id == 'information':
                fixture_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key. {self.input_json['fixture']['information']}"
                output_json['fixture']['information'] = self.generate_gpt_flavor(fixture_information_input)

            output_json['fixture'][id]['statistics'] = {}
            for statistic in self.input_json['fixture'][id]['statistics']:
                fixture_statistics_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key.{self.input_json['fixture'][id]['statistics'][statistic]}"
                output_json['fixture'][id]['statistics'][statistic] = self.generate_gpt_flavor(fixture_statistics_input)

        venue_information_input = f"Create three outputs in different length, with the flavor {commentary_flavor}. Provide the output as a json. The length title is the key.{self.input_json['venue']}"
        output_json['venue'] = self.generate_gpt_flavor(venue_information_input)

        return output_json

    def generate_gpt_flavor(self, input):
        client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=self.gpt_api_key,
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You get a text from a sports journalist for live commentary. Take the text and create three outputs with different length. A short in one sentence. A middle one with 2 to 3 sentences. And a long one. Write the text with the provided flavor."},
                {"role": "user", "content": f"{input}"},
            ],
            model="gpt-4",
            temperature=0.9,
        )
        return response.choices[0].message.content
    

if __name__ == "__main__":
    team_ids = [487, 489]
    output_json = OutputJSON(team_ids, "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")
    output_file = output_json.create_output_json('humorous')

    with open('final_output.json', 'w') as fp:
        json.dump(output_file, fp, indent=4)

            