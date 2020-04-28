import os,sys
sys.path.append('../src/pyext/')
from Model import Model
from Validation import Validation
import gensim
import pickle
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import numpy as np
from gensim.models.fasttext import FastText as FT_gensim
from gensim.test.utils import datapath


class TestSample():
    def __init__(self):
        self.MODEL     = gensim.models.LdaModel.load('models/lda/lda_train_150topics_100passes_alldata_04262020.model')
        self.dictionary = pickle.load(open("models/lda/data/dictionary.pkl", "rb"))
        self.data_name_dict = pickle.load(open("models/lda/data/data_dict.pkl", "rb"))
        self.data_map_link = pickle.load(open("models/lda/data/data_map_link.pkl", "rb"))
        self.data_dataframe = pickle.load(open("models/lda/data/data_df_cols.pkl", "rb"))
        self.total_words=pickle.load(open("models/lda/data/total_words.pkl", "rb"))
        self.FT=FT_gensim.load("models/FT/fasttext_04252020.model")

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
            df_sorted=df_result.sort_values(by=['Similarity'])
            return df_sorted
        else:
            return "None"

    def FT_results(self,sample):
        num,statement=self.Check_format(sample)
        if num==0:
            sample_lower=sample.lower()
            sample_list=sample_lower.split(',')
            test=[sample_list]
            train_=list(self.data_name_dict.values())
            train=[i for i in train_]
            df_result=pd.DataFrame(columns=['Pathway_test','Pathway_train','Similarity','test length','train length'])
            for k,l in enumerate(train):
                sim=self.FT.n_similarity(test[0], train[k])
                if sim>0:
                    lst=[['UNK',list(self.data_name_dict.keys())[k],1-sim,len(test[0]),len(train[k])]]
                    df_result=df_result.append(pd.DataFrame(lst,
                                              columns=['Pathway_test','Pathway_train','Similarity','test length','train length']))
            
            df_sorted=df_result.sort_values(by=['Similarity'])
            return df_sorted
        else:
            return "None"

    def convert_df_to_jsdict(self,df):
        similarity={'Rank':[],
                    'Network name':[],
                    'Network ID':[],
                    'Similarity score':[]}
        Name=df['Pathway_train'].to_list()
        Similarity_df=df['Similarity'].to_list()
        map_dict = dict(zip(self.data_dataframe.Name, self.data_dataframe.Map))
        for i in range(0,10):
            similarity['Rank'].append(i+1)
            #similarity['Network name'].append(Name[i])
            similarity['Network ID'].append(map_dict[Name[i]])
            similarity['Similarity score'].append(Similarity_df[i])
            similarity['Network name'].append(self.data_map_link[Name[i]])
        return similarity

    def dict_to_JSlist(self,Dict):
        L = []
        if bool(Dict):
            if len(list(Dict.keys()))>0:
                L.append(list(Dict.keys()))
                target=list(Dict.values())
                for i in range(len(target[0])):
                    List=[]
                    for j in target:
                        List.append(str(j[i]))
                    L.append(List)
        return L


if __name__=='__main__':
    TestSample()
    sample='ec:1.2.3.4,ec:4.1.4.1'
    a=TestSample().FT_results(sample)
    print (a)
