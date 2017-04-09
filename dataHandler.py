#coding:utf-8
import sys
import os
import json
import re

def parseRawData():
    rst = []
    def sentenceParse(para):
        # para = "-181-村橋路不端，數里就迴湍。積壤連涇脉，高林上笋竿。早嘗甘蔗淡，生摘琵琶酸。（「琵琶」，嚴壽澄校《張祜詩集》云：疑「枇杷」之誤。）好是去塵俗，煙花長一欄。"
        result, number = re.subn("（.*）", "", para)
        result, number = re.subn("{.*}", "", result)
        result, number = re.subn("[\]\[]", "", result)
        return result.strip("[0123456789-]")

    def handleJson(file):
        # print file
        rst = []
        data = json.loads(open(file).read())
        for poetry in data:
            pdata = ""
            for sentence in poetry.get("paragraphs"):
                pdata += sentence
            pdata = sentenceParse(pdata)
            if pdata!="":
                rst.append(pdata)
        return rst
    # print sentenceParse("")
    data = []
    src = './chinese-poetry/json/'
    for filename in os.listdir(src):
        if filename.startswith("poet.tang"):
            data.extend(handleJson(src+filename))
    return data

if __name__=='__main__':
    data = parseRawData()
    for s in data:
        print s
