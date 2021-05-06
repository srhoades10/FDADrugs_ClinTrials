
import os, re, json, sys 
import xml.etree.ElementTree as ET

def extractClinicalTrials(dumpDict, fileName, trialIDFile, studyTypes = ['Interventional'], 
    studyStatus = ['Not yet recruiting', 'Recruiting', 'Enrolling by invitation', 
    'Active, not recruiting', 'Completed'], interventionTypes = ['Drug'], minAge = 18):
    """ Extract information from clinical trial dump, much like a query on the
        website itself (except there are limits to the number of exports on the
        website). Type, status, age, intervention are all like that on 
        clinicaltrials.gov. Note that it is difficult by purely text to know if
        a trial is a combination, so a basic check is made for 'in combination'
        in any of the text fields. """

    studyType, status, interventionType = '', '', ''
    
    trialEntry = re.sub(r'\.xml', '', trialIDFile)
    tree = ET.parse(fileName)
    root = tree.getroot()
    drugs = []
    for child in root:
        if child.tag == 'study_type':
            studyType = child.text 
        if child.tag == 'overall_status':
            status = child.text
        if child.tag == 'study_first_submitted':
            year = int(re.findall(r'\d\d\d\d', child.text)[0]) 
        for grandchild in child:
            if grandchild.tag == 'intervention_type':
                interventionType = grandchild.text
            if grandchild.tag == 'intervention_name' and interventionType == 'Drug':
                drugs.append(grandchild.text)
            if grandchild.tag == 'minimum_age':
                age = grandchild.text 
                age = re.findall(r'\d+', age)
                if len(age) > 0:
                    age = int(age[0])
                else:
                    age = -1

    if 'age' not in locals(): #If its not found in the xml, don't trust it
        age = -1 
    if 'year' not in locals(): #" "
        age = -1

    if (studyType in studyTypes and status in studyStatus and 
        interventionType in interventionTypes and age >= minAge and len(drugs) > 1):
        combinationPossibility = False
        for child in root:
            for grandchild in child:
                if 'in combination' in grandchild.text.lower():
                    combinationPossibility = True
    else:
        combinationPossibility = False 
    
    if (studyType in studyTypes and status in studyStatus and 
        interventionType in interventionTypes and age >= minAge):

        dumpDict[trialEntry] = dict()
        dumpDict[trialEntry]['Type'] = studyType 
        dumpDict[trialEntry]['Status'] = status 
        dumpDict[trialEntry]['Intervention Type'] = interventionType 
        dumpDict[trialEntry]['Drug(s)'] = drugs
        dumpDict[trialEntry]['Minimum Age'] = age 
        dumpDict[trialEntry]['Combination'] = combinationPossibility
        dumpDict[trialEntry]['Year'] = year
        return dumpDict 

    else:
        return dumpDict


def buildQueryDict(baseDir = 'AllPublicXML'):
    results = dict()
    for studySet in os.listdir(baseDir):
        if 'Contents' not in studySet:
            for study in os.listdir('{0}/{1}'.format(baseDir, studySet)):
                fileName = '{0}/{1}/{2}'.format(baseDir, studySet, study)
                results = extractClinicalTrials(results, fileName, study)
    return results
