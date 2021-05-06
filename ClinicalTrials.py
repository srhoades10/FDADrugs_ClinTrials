""" ClinicalTrials.gov analysis. Approval drugs are analyzed separately in 
    FDADrugs.py. The following filters were applied for the purpose of surveying
    what is currently in trials (or ready to go into trials):

    Since export limit is 10k, then all public study records must be downloaded 
        at https://clinicaltrials.gov/AllPublicXML.zip (1.3GB)

    - Status: Not yet recruiting; recruiting; enrolling by invitation; active, not recruiting
    - Age Group: Adult; Older Adult 
    - Study type: Interventional (Clinical Trial)
    - Interventions must only contain Drug: [], and a rough check will be made as
        to whether multiple drugs are present, and if so, check if "combination"
        appears anywhere on the description (crude assessment for active monotherapy
        vs. combination therapy trials)
    
    Author: Seth Rhoades
"""
import os, re, json, sys 
sys.path.append('./src')
import setup_trials as util

def main():
    results = util.buildQueryDict(baseDir = 'AllPublicXML')
    
    with open('ref/ClinicalTrialQuery.json', 'w') as fout:
        json.dump(results, fout, indent = 4)
        fout.write('\n')

if __name__ == '__main__':
    main()
