import os,pickle,random 
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split

class CleanData(object):
    def __init__(self):
        self.path='../../data/files/'

    def get_file_handle(self,fname):
        File_Handle=open(os.path.join(self.path+fname),'r+')
        return File_Handle

    def get_pathway_dict(self,fname):
        pathway_name_dict={item.strip().split(':')[0]:item.strip().split(':')[1].replace('__',' ').replace('_',' ') for num,item in enumerate(self.get_file_handle(fname).readlines())}
        return pathway_name_dict
    
    def get_dataframe(self,fname):
        maps=[];Rx=[];EC=[];ECI=[];ECA=[]
        for i,j in enumerate(open(self.path+fname)):
            line=j.strip().split(':')
            if len(line[2:])>1:
                EC_crop_space=[X.strip() for X in line[2:]]
                EC_crop=':'.join(EC_crop_space)
                EC_each=EC_crop.split('_')
                ECA.append(list((EC_each)))
                maps.append(line[0])
                Rx.append(line[1])
        df=pd.DataFrame(list(zip(maps,ECA)), columns=['Map','EC_all'])
        return df

    def get_list_of_EC(self,df,dictionary):
        df_doc_group= df.groupby(['Map'])['EC_all'].apply(list).reset_index(['Map'])
        df_doc_group['Name']=[dictionary[i] for i in df_doc_group['Map']]
        return df_doc_group

    def clean_dataframe(self,df):
        EC_all_dict={new_list: [] for new_list in range(df.shape[0])} 
        for i,j in enumerate(df['EC_all']):
            for k in j:
                for l in k:
                    EC_all_dict[i].append(l)         
        df['EC_all_cleaned']=pd.Series(EC_all_dict)
        indexNames = df[df['EC_all_cleaned'].map(len)<=3].index
        df.drop(indexNames , inplace=True)
        df_final=df.copy()
        pickle.dump(df_final, open(self.path+"df_final.pkl", "wb" ) )
        return df_final
    

if __name__=='__main__':
    pathway_name_dict=CleanData().get_pathway_dict(fname='pathway_ID.csv')
    df=CleanData().get_dataframe(fname='ec_gram.csv')
    df_grouped=CleanData().get_list_of_EC(df,pathway_name_dict)
    df_final=CleanData().clean_dataframe(df_grouped)
    EC_list_train,EC_list_test=CleanData().get_train_and_test(df_final)

