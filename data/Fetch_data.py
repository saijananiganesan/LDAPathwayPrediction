import requests
import os 
import pandas as pd
from collections import Counter

class KEGG_data(object):
    def __init__(self):
        self.url='http://rest.kegg.jp'
        self.path='../data/'

    def get_response_from_url(self,url):
        response=requests.get(url)
        if response.status_code!=200:
            print ("Error in fetching data, check if url is {}".format(url))
        return response.text

    def get_all_pathways(self):
        url_new=self.url+'/list/pathway';pathway_id={}
        pathway_file=open(os.path.join(self.path+"list_of_pathways.csv"),'w+')
        pathway_file.write(self.get_response_from_url(url_new))
        for k,j in enumerate(response.text.splitlines()):
            pathway_id[j.strip('\t').split(':')[1].strip().split()[0]]='_'.join(j.strip('\t').split(':')[1].strip().split()[1:])  
        pathway_map=open(os.path.join(self.path+"pathway_ID.csv"),'w+')
        for m,n in pathway_id.items():
            pathway_map.write("%s:%s\n" %(m,n))
        pathway_file.close()
        return pathway_id,pathway_id.keys()
 
    def get_all_organisms(self):
        url_new=self.url+'/list/organism'
        organism_file=open(os.path.join(self.path+"list_of_organisms.csv"),'r+')
        organism_file.write(self.get_response_from_url(url_new))
        organism_file.close()

    def get_prokaryotes(self):
        org_list=[]
        file=open(os.path.join(self.path+"list_of_organisms.csv"),'r+')
        for i,j in enumerate(file.readlines()):
            if ('Prokaryotes' in j.strip()): 
                org_list.append(j.strip().split()[1])
        prokaryotes_file=open(os.path.join(self.path+"prokaryotes.csv"),'w+')
        for item in org_list:
            prokaryotes_file.write("%s\n" %item) 
        prokaryotes_file.close()
        return org_list

    def get_prok_path(self):
        prok_path=[];prok_path_dict={}
        org_list=self.get_prokaryotes()
        prok_file=open(os.path.join(self.path+"prok_pathways.csv"),'w+')
        prok_file_stats=open(os.path.join(self.path+"prok_path_stats.csv"),'w+')
        for i in org_list:
            url_new=self.url+'/list/pathway/'+i
            for k,j in enumerate(self.get_response_from_url(url_new).splitlines()):
                path=j.strip('\t').split(':')[1].strip().split()[0]
                path_id=path.replace(i,'')
                prok_path.append('map'+path_id)
        prok_path_dict=Counter(prok_path)
        
        for i,j in prok_path_dict.items():
            prok_file_stats.write("map%s:%s\n" %(i,j))
        prok_file_stats.close()

        prok_path_final=list(set(prok_path))
        for item in prok_path_final:
            prok_file.write("%s\n" %item)
        prok_file.close()
        return prok_path_final,prok_path_dict

    def get_rxn_list_for_pathways(self):
        pathway_file=open(os.path.join(self.path+"prok_pathways.csv"),'r+')
        rxn_file=open(os.path.join(self.path+"rxn_pathways.csv"), 'w+')
        for i,item in enumerate(pathway_file.readlines()):
            url_new=self.url+'/link/rn/'+item.strip()
            rxn_file.write(self.get_response_from_url(url_new))
        rxn_file.close()
    
    def get_ec_for_rxn(self):
        rxn_file=open(os.path.join(self.path+"rxn_pathways.csv"),'r+')
        ec_file=open(os.path.join(self.path+"ec_gram.csv"),'w+')
        for i,item in enumerate(rxn_file.readlines()):
            if len(item.strip().split())>0:
                print (i, item.strip().split()[1].split(':')[1])
                rxn=item.strip().split()[1].split(':')[1]
                mapid=item.strip().split()[0].split(':')[1]
                url_new=self.url+'/link/ec/'+rxn
                ec_file.write(mapid+':'+rxn+':')
                ec_text=self.get_response_from_url(url_new);ec=[]
                for i,j in enumerate(ec_text.splitlines()):
                    if(len(j.strip().split())>0):
                        ec.append(j.strip().split('\t')[1])
                ec='_'.join(ec)
                ec_file.write(ec+'\n')
        ec_file.close()

    def get_ko_for_rxn(self):
        rxn_file=open(os.path.join(self.path+"rxn_pathways.csv"),'r+')
        ko_file=open(os.path.join(self.path+"ko_gram.csv"),'w+')
        for i,item in enumerate(rxn_file.readlines()):
            if len(item.strip().split())>0:
                print (i, item.strip().split()[1].split(':')[1])
                rxn=item.strip().split()[1].split(':')[1]
                mapid=item.strip().split()[0].split(':')[1]
                url_new=self.url+'/link/ko/'+rxn
                ko_file.write(mapid+':'+rxn+':')
                ko_text=self.get_response_from_url(url_new);ko=[]
                for i,j in enumerate(ko_text.splitlines()):
                    if(len(j.strip().split())>0):
                        ko.append(j.strip().split('\t')[1])
                ko='_'.join(ko)
                ko_file.write(ko+'\n')
        ko_file.close()

    def get_ec_for_rxn_table(self):
        rxn_file=open(os.path.join(self.path+"rxn_pathways.csv"),'r+')
        ec_file=open(os.path.join(self.path+"ec_table.csv"),'w+')
        for i,item in enumerate(rxn_file.readlines()):
            if len(item.strip().split())>0:
                print (i, item.strip().split()[1].split(':')[1])
                rxn=item.strip().split()[1].split(':')[1]
                mapid=item.strip().split()[0].split(':')[1]
                url_new=self.url+'/link/ec/'+rxn
                ec_text=self.get_response_from_url(url_new);ec=[]
                for i,j in enumerate(ec_text.splitlines()):
                   if(len(j.strip().split())>0):
                        ec_file.write(mapid+','+rxn+','+j.strip().split('\t')[1]+'\n')        
        ec_file.close()

    def get_ec_for_map_table(self):
        prok=open(os.path.join(self.path+"prok_pathways.csv"),'r+')
        ec_file=open(os.path.join(self.path+"ec_map_table.csv"),'w+')
        for i,item in enumerate(prok.readlines()):
            if len(item.strip().split())>0:
                print (i, item.strip().split()[0])
                mapid=item.strip().split()[0]
                url_new=self.url+'/link/ec/'+mapid
                ec_text=self.get_response_from_url(url_new);ec=[]
                for i,j in enumerate(ec_text.splitlines()):
                   if(len(j.strip().split())>0):
                        ec_file.write(mapid+','+j.strip().split('\t')[1]+'\n')
        ec_file.close()

    def get_ko_for_rxn_table(self):
        rxn_file=open(os.path.join(self.path+"rxn_pathways.csv"),'r+')
        ko_file=open(os.path.join(self.path+"ko_table.csv"),'w+')
        for i,item in enumerate(rxn_file.readlines()):
            if len(item.strip().split())>0:
                print (i, item.strip().split()[1].split(':')[1])
                rxn=item.strip().split()[1].split(':')[1]
                mapid=item.strip().split()[0].split(':')[1]
                url_new=self.url+'/link/ko/'+rxn
                ko_text=self.get_response_from_url(url_new);ko=[]
                for i,j in enumerate(ko_text.splitlines()):
                   if(len(j.strip().split())>0):
                        ko_file.write(mapid+','+rxn+','+j.strip().split('\t')[1]+'\n')
        ko_file.close()


if __name__=='__main__':
    KEGG_data().get_all_pathways()
    KEGG_data().get_all_organisms()
    KEGG_data().get_prokaryotes()
    KEGG_data().get_prok_path()
    KEGG_data().get_rxn_list_for_pathways()
    KEGG_data().get_ec_for_map_table()
