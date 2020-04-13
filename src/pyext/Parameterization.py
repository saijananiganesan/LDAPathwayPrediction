import os,pickle,random 
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from gensim import corpora, models
from gensim.models.phrases import Phrases, Phraser
import gensim
from sklearn.metrics import fbeta_score
from sklearn.metrics import f1_score
from gensim.models import CoherenceModel
from scipy.stats import entropy
import logging
import Model

class Parameterization(Model.Model):
    def __init__(self):
        super().__init__()
        self.df=Model.Model().df_pkl
        self.EC_train,self.EC_test=Model.Model().get_train_and_test(Model.Model().df_pkl)
        self.dictionary,self.corpus=Model.Model().get_dict_corpus(self.EC_train)
        self.test_corpus=Model.Model().get_test_corpus(self.dictionary,self.EC_test)
        self.path='../images/'

    def MyLDA_param(self,corpus,dictionary,num_topics,alpha,eta,random_state=200,passes=100):
        ldamodel=gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics,
                                      alpha=alpha,
                                      eta=eta,
                                      random_state=random_state,
                                      id2word = dictionary, passes=passes)
        return ldamodel

    def gridsearch(self,alpha,eta,topics):
        if alpha is None:
            alpha=np.arange(0,0.5,0.1)
        if eta is None:
            eta=np.arange(0,0.5,0.1)
        if topics is None:
            topics=np.arange(50,150,25)
        cols = ['Topics', 'alpha', 'eta','Coherence','log_perplexity']
        lst = []
        for topic in topics:
            for a in alpha:
                for e in eta:
                    model=self.MyLDA_param(self.corpus,self.dictionary,topic,a,e)
                    coherence=Model.Model().model_coherence(model,self.EC_train,dictionary)
                    perplexity=Model.Model().model_perplexity(model,self.test_corpus)
                    lst.append([topic, alpha,beta,coherence,perplexity])
        df = pd.DataFrame(lst, columns=cols)
        df.sort_values(by=['Coherence'])
        pickle.dump(df, open( "model/gridsearch.pkl", "wb" ) )


if __name__=='__main__':
    #Parameterization()
    #print (Parameterization().df.head())
