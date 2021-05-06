""" Analyze Drugs@FDA. Downloaded from 
    https://www.fda.gov/Drugs/InformationOnDrugs/ucm079750.htm. Note .csv will be
    exported for plots in R

    Procedures:
        - Only ORIG, approved, (AP), from Submissions
        - Only 1 or 2 MarkingStatus (Rx or OTC)
        - Only NDA or BLA from Applications
        - Extract Form from Products (after the semicolon)
        - Extract DrugName:ActiveIngredient pairs in Products (disregard strength)
    
    Author: Seth Rhoades
"""

import csv, yaml, re
import pandas as pd 

fileDir = 'params/FDAFiles.yaml'
with open(fileDir) as fin:
    files = yaml.safe_load(fin)

def main(files):

    submission = pd.read_csv(files['Submissions'], sep = '\t', dtype = 'str', 
            usecols = [0, 1, 2, 3, 4, 5])
    submission['Year'] = [re.sub(r'\-.*', '', str(x)) for x in submission['SubmissionStatusDate']]
    marketingStatus = pd.read_csv(files['MarketingStatus'], sep = '\t', dtype = 'str')
    applications = pd.read_csv(files['Applications'], sep = '\t', dtype = 'str')
    products = pd.read_csv(files['Products'], sep = '\t', dtype = 'str', 
        usecols = [0, 2, 5, 6])

    origsSubmission = set(submission['ApplNo'][(submission['SubmissionType'] == 'ORIG') & 
        (submission['SubmissionStatus'] == 'AP') & 
        (submission['SubmissionClassCodeID'].notnull())].values)
    origSubset = submission[(submission['SubmissionType'] == 'ORIG') & 
        (submission['SubmissionStatus'] == 'AP') & 
        (submission['SubmissionClassCodeID'].notnull())]
    applYearDict = dict(zip(origSubset.ApplNo, origSubset.Year))

    marketedItems = list(set(marketingStatus['ApplNo'][(marketingStatus['MarketingStatusID'] == '1') |
    (marketingStatus['MarketingStatusID'] == '2')].values))

    NDAsBLAs = list(set(applications['ApplNo'][(applications['ApplType'] == 'NDA') |
    (applications['ApplType'] == 'BLA') | (applications['ApplType'] == 'ANDA')].values))
    entitySubset = applications[(applications['ApplType'] == 'NDA') |
    (applications['ApplType'] == 'BLA') | (applications['ApplType'] == 'ANDA')]
    entityDict = dict(zip(entitySubset.ApplNo, entitySubset.ApplType))

    finalAppls = origsSubmission.intersection(NDAsBLAs).intersection(marketedItems)
    finalProducts = products[products['ApplNo'].isin(finalAppls)].drop_duplicates() 

    finalProducts['Route'] = [re.sub(r'^.*\;', '', x) for x in finalProducts.Form]
    finalProducts['Route'] = [re.sub(r'^ | $|\-\d+', '', x) for x in finalProducts.Route]
    finalProducts['Route'] = finalProducts['Route'].str.lower()
    finalProducts['Year'] = [applYearDict[x] for x in finalProducts['ApplNo']]
    finalProducts['Entity'] = [entityDict[x] for x in finalProducts['ApplNo']]

    finalProducts.to_csv('ref/ApprovedFDADrugs.csv')

if __name__ == '__main__':

    main(files)