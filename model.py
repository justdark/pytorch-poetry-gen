import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F

class PoetryModel(nn.Module):
    def __init__(self, vocab_size,hidden_dim):
        super(PoetryModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(vocab_size, self.hidden_dim)
        self.linear1 = nn.Linear(self.hidden_dim,vocab_size)
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax()

    def forward(self, input, hidden):
        length = input.size()[0]

        output, hidden = self.lstm(input.view(length, 1, -1), hidden)
        # print output.size()

        output = F.relu(self.linear1(output.view(length,-1)))
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self,length = 1):
        return (Variable(torch.zeros(length, 1, self.hidden_dim).cuda()),
                Variable(torch.zeros(length, 1, self.hidden_dim)).cuda())