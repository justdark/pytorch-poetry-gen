#coding:utf-8
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import dataHandler
from model import PoetryModel
from torch.autograd import Variable
import cPickle as p
from utils import *

model = torch.load('poetry-gen.pt')
max_length = 20
rFile =file('wordDic','r')

word_to_ix = p.load(rFile)
def invert_dict(d):
    return dict((v,k) for k,v in d.iteritems())
ix_to_word = invert_dict(word_to_ix)

# Sample from a category and starting letter
def sample(startWord='<START>'):
    input = make_one_hot_vec(startWord,word_to_ix)
    hidden = model.initHidden()
    output_name = "";
    for i in range(max_length):
        output, hidden = model(input.cuda(), hidden)
        topv, topi = output.data.topk(1)
        topi = topi[0][0]
        w = ix_to_word[topi]
        if w == "<EOP>":
            break
        else:
            output_name += w
        input = make_one_hot_vec(w,word_to_ix)
        print output_name
    return output_name
sample()
# sample("床".decode('utf-8'))