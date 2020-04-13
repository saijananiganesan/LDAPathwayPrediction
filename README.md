# Improving enzymatic pathway prediction using latent Dirichlet allocation (LDA)

![Metabolic pathways in prokaryotes](https://raw.githubusercontent.com/saijananiganesan/LDAPathwayPrediction/master/images/pathways.png)

## Project objective 
- `1.` Identify co-occurring enzyme clusters(topics) in prokaryotic metabolic networks(documents)
- `2.` Identify similar, existing networks, given a set of enzymes(words) from an organism

## List of files and directories:

- `data`     contains all relevant data from KEGG (document files) 

- `src`      contains all the modeling scripts  

- `EDA`      contains an explaratory data analysis script

## List of classes:

- `KEGGData`  class to fetch data from KEGG database
             
- `CleanData` class to clean files and organize all documents (metabolic networks) into 1 dataframe 

- `Model`     class to model LDA 
                  
- `Validation` class to validate output;inherits from Model class

- `Parameterization` class to parameterize LDA model;inherits from Model class 

## Running simulations 

- `Play.ipynb` demo script on loading data, model building and validation

## Information

_Author(s)_: Sai J. Ganesan


