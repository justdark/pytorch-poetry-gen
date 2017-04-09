#coding:utf-8
import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import dataHandler
from model import PoetryModel
from torch.autograd import Variable
from utils import *
import cPickle as p

data = dataHandler.parseRawData()


word_to_ix = {}
for sent in data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
word_to_ix['<EOP>'] = len(word_to_ix)
word_to_ix['<START>'] = len(word_to_ix)
VOCAB_SIZE = len(word_to_ix)
print "VOCAB_SIZE:",VOCAB_SIZE
print "data_size",len(data)
def toList(sen):
    rst = []
    for s in sen:
        rst.append(s)
    return rst
for i in range(len(data)):
    if data[i][0]=="-":
        print data[i]
    data[i] = toList(data[i])

    # print data[i]
    data[i].append("<EOP>")


p.dump(word_to_ix,file('wordDic','w'))

# for s in data:
#     print i
#     i += 1
#     transferData.append(make_one_hot_data(s,word_to_ix))

model = PoetryModel(len(word_to_ix),128);
model.cuda()
optimizer = optim.RMSprop(model.parameters(), lr=0.01)

criterion = nn.NLLLoss()
one_hot_var = {}
one_hot_var_target = {}
for w in word_to_ix:
    one_hot_var.setdefault(w,make_one_hot_vec(w,word_to_ix))
for w in word_to_ix:
    one_hot_var_target.setdefault(w, make_one_hot_vec_target(w,word_to_ix))
wordList = open('wordList','w')
for w in word_to_ix:
    wordList.write(w.encode('utf-8'))
wordList.close()

epochNum = 10;
TRAINSIZE = len(data)
batch = 100
trainingIn = []
trainingOut = []
def makeForOneCase(s):
    tmpIn = []
    tmpOut = []
    for i in range(len(s) - 1):
        w = s[i]
        w_b = s[i - 1] if s > 0 else "<START>"
        tmpIn.append(one_hot_var[w_b])
        tmpOut.append(one_hot_var_target[w])
    return torch.cat(tmpIn),torch.cat(tmpOut)

# for case in range(TRAINSIZE):
#     s = data[case]
#     makeForOneCase(s)


print "start training"
for epoch in range(epochNum):

    for batchIndex in range(int(TRAINSIZE/batch)):
        model.zero_grad()
        loss = 0
        for case in range(batchIndex*batch,(batchIndex+1)*batch):

            s = data[case]


            hidden = model.initHidden()

            # for i in range(len(s)-1):
            #     w = s[i]
            #     w_b = s[i-1] if s>0 else "<START>"
            #     output, hidden = model(one_hot_var[w_b], hidden)
            #     loss += criterion(output,one_hot_var_target[w])
            t,o = makeForOneCase(s)
            output, hidden = model(t.cuda(),hidden)
            loss += criterion(output,  o.cuda())
        loss = loss/batch
        loss.backward()
        print epoch,loss.data[0]
        optimizer.step()
torch.save(model, 'poetry-gen.pt')


        #
# for s in transferData:
#     for i in range(s.size()[0]):
#         print s[i]
#     sdasdas