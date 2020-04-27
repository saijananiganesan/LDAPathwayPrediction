import os,sys
sys.path.append('../src/pyext/')
from Model import Model
from Validation import Validation
import gensim
import pickle
import pandas as pd
import numpy as np

class test_sample():
    def __init__(self):
        self.MODEL     = gensim.models.LdaModel.load('../src/pyext/models/lda/lda_train_150topics_100passes_alldata_04262020.model')
        self.dictionary = pickle.load(open("../src/pyext/models/lda/data/dictionary.pkl", "rb"))
        self.data_name_dict = pickle.load(open("../src/pyext/models/lda/data/data_dict.pkl", "rb"))
        self.data_map_link = pickle.load(open("../src/pyext/models/lda/data/data_map_link.pkl", "rb"))
        self.data_dataframe = pickle.load(open("../src/pyext/models/lda/data/data_df_cols.pkl", "rb"))
        self.total_words=pickle.load(open("../src/pyext/models/lda/data/total_words.pkl", "rb"))

    def Check_format(self,sample):
        sample_lower=sample.lower()
        try:
            sample_list=sample_lower.split(',')
        except :
            printed_text="Input not in the right format, you might have forgotten commas"
            return 1,printed_text
        try:
            ec=[i.count('ec') for i in sample_list]
            #print (ec)
            #print (sample_list)
            if len(sample_list)!=sum(ec):
                printed_text="Input not in the right format, you might have forgotten using ec or the semicolon between ec and the numbers"
                return 1,printed_text
        except:
                printed_text= "Input not in the right format, you might have forgotten using ec or the semicolon between ec and the numbers"
                return 1,printed_text
        try:
            ec_class=set([int(i.split(':')[1].split('.')[0]) for i in sample_list])
            #print (ec_class)
            ec_class_incorrect= [i for i in list(ec_class) if i not in range(1,8)]
            #print (ec_class_incorrect)
            if len(list(ec_class))>=7: 
                printed_text= "Input not in the right format, you are not using EC classe 1-7"
                return 1,printed_text
            if len(ec_class_incorrect)>0: 
                printed_text= "Input not in the right format, you are not using EC classe 1-7"
                return 1,printed_text                
        except:
                printed_text= "Input not in the right format, you might have forgotten using ec or the semicolon between ec and the numbers"
                return 1,printed_text
        try:
            ec_nums=set([len(i.split(':')[1].split('.')) for i in sample_list])
            #print (ec_nums)
            if len(list(ec_nums))>1:
                printed_text= "Input not in the right format, check your ec numbers"
                return 1,printed_text
            elif 4 not in ec_nums:
                printed_text= "Input not in the right format, check your ec numbers"
                return 1,printed_text                
        except:
                printed_text= "Input not in the right format, check your ec numbers"
                return 1,printed_text

        return 0,"Input in the right format"

    def Check_In_DB(self,sample):
        num,statement=self.Check_format(sample)
        if num==0:
            sample_lower=sample.lower()
            sample_list=sample_lower.split(',')
            common_elements=list(set(sample_list).intersection(set(self.total_words)))
            if len(common_elements)<len(sample_list):
                return "Please try FastText, one or more enzymes not in training set"
            elif len(common_elements)==len(sample_list):
                return "All enzymes in training set, can use LDA or FastText"
            else:
                return "Error in input, please check input"
        else:
            return "Error in input, please check input format"


    def LDA_results(self,sample):
        num,statement=self.Check_format(sample)
        if num==0:
            sample_lower=sample.lower()
            sample_list=sample_lower.split(',')            
            test={}
            test['Map']='UNK'
            test['Name']='UNK pathway'
            test['EC']=[sample_list]
            df_validate=pd.DataFrame(test)
            df_result=Validation().compare_test_train_docs(df_validate,self.data_dataframe,self.MODEL,self.dictionary)
            return df_result
        else:
            return "None"


if __name__=='__main__':
    test_sample()
    sample='ec:2.4.1.3,ec:4.4.1.36,ec:4.44.444.1'
    a,b=test_sample().Check_format(sample='ec:2.4.1.3,ec:4.4.1.36,ec:4.44.444.1')
    print (a,b)
    c=test_sample().Check_In_DB(sample)
    print (c)
    d=test_sample().LDA_results(sample)
    print(d)
'''
sample='ec:1.2.3.4,ec:2.3.4.44,ec:3.1.23.1'

valid=['ec:4.2.1.166','ec:2.8.3.8','ec:3.1.2.1','ec:4.2.1.55','ec:1.1.1.157','ec:2.3.1.9'];valid_dist={}
valid_dist['Map']='PF06050'
valid_dist['Name']='UNK pathway'
valid_dist['EC']=[valid]
df_validate=pd.DataFrame(valid_dist)
df_validate
df_result=Validation().compare_test_train_docs(df_validate,data_df_cols,model,dictionary)
Validation().print_heat_map_for_one(df_result,df_validate)
'''
