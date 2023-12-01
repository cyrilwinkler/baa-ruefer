import sys
sys.path.append('/Users/tschip/workspace/baa/ruefer/')

import pandas as pd
import torch
import torch.nn as nn
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from models.logic2text.utils import sample_sequence
from torch.autograd import Variable
from models.logic2text.DataLoader import *
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class GPT():
    def __init__(self) -> None:
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.model = nn.DataParallel(self.model)
        self.model.load_state_dict(torch.load('../models/logic2text/models/GPT_ep19.pt', map_location=device))
        self.model.to(device)
        self.model.eval()

        self.dataset = GPTTableDatabase(None, None, None, self.tokenizer, 5, 800)

    def generate(self, data, cols, table_description):
        list_of_hypothesis = []
        results = {}
        with torch.no_grad():
            #batch = self.dataset.get_data(data, cols, table_description)
            desc = self.dataset.get_data_for_table(data, cols)
            #input_string = batch[-1]
            #batch = batch[:-1]
            #print(f'input_string: {input_string}')
            #print(f'batch: {batch}')
            #idx = dataset.get_idx('test')
            #references = dataset.get_reference(idx, 'test')
            #table_id = dataset.get_table_id(idx, 'test')
            #results[stat_key] = []

            #batch = tuple(Variable(t).to(device) for t in batch)
            #trg_inp, trg_out, mask, caption = batch

            fake_inputs = desc# caption
            fake_inputs = fake_inputs.to(device)

            print(desc.shape)

            samples = sample_sequence(self.model, 30, fake_inputs, [], top_p=0.9)
            samples = samples[:, desc.shape[1]:]
            samples = samples.cpu().data.numpy()
            print(f'samples len: {len(samples)}')
            for s in samples:
                text = self.tokenizer.decode(s, clean_up_tokenization_spaces=True)
                text = text[: text.find(self.tokenizer.eos_token)]

                hypothesis = text.lower().split(' ')
                
                list_of_hypothesis.append(hypothesis)
            
            return list_of_hypothesis
                