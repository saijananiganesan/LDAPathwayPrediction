import os,pickle,random 
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split

class Model(object):
    def __init__(self):
        self.path='../data/files/'
        self.df_pkl=pickle.load(open(self.path+'df_final.pkl','rb'))
    
    def get_EC_list(self,df):
        EC_list_init=df['EC'].values.tolist()
        EC_list=[list(set(i)) for i in EC_list_init]
        return EC_list

    def get_train_and_test(self,df):
        for i in range(0,10000):
            train,test=train_test_split(df,test_size=0.075)
            test_crop=test[['Map','Name','EC_all_cleaned']]
            test_crop.rename(columns={'EC_all_cleaned':'EC'}, inplace=True)
            train_crop=train[['Map','Name','EC_all_cleaned']]
            train_crop.rename(columns={'EC_all_cleaned':'EC'}, inplace=True)
            EC_unique_train=set([j for i in train_crop['EC'].to_list() for j in i])
            EC_unique_test=set([j for i in test_crop['EC'].to_list() for j in i])
            if EC_unique_test.issubset(EC_unique_train):
                print ("True")
            break
        EC_list_train=self.get_EC_list(train_crop)
        EC_list_test=self.get_EC_list(test_crop)
        return EC_list_train,EC_list_test

if __name__=='__main__':
    EC_list_train,EC_list_test=Model().get_train_and_test(Model().df_pkl)
    print (EC_list_test)

