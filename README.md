# FDA drug approvals and combination therapy clinical trials

## Introduction

The most effective strategies to curb the rise of cardiometabolic diseases in the late 20th century focused on single risk factors. Population-level blood pressure and cholesterol, for instance, decreased in large part from pharmaceuticals [1,2]. The returns on these innovations now appear to be diminishing: obesity rates continue to rise [3], and gains in healthy life expectancy trail that of total life expectancy [4]. If these patterns reflect a broader depiction of the modern human condition, then we should question if such complex challenges can be addressed through such focused countermeasures. The primary question of interest here is how many approved therapies consist of multiple active chemicals or biologics.

### Protocol

_FDADrugs.py_: Drugs@FDA is downloaded from https://www.fda.gov/Drugs/InformationOnDrugs/ucm079750.htm, and a filter is created on drugs which are original Submissions, Prescription or Over the Counter Status, and an ANDA, NDA or BLA Application type.

_ClinicalTrials.py_: Clinical trial metadata is downloaded from https://clinicaltrials.gov/AllPublicXML.zip, and a filter is created where trials are Not Yet Recruiting, Recruiting, Enrolling, Active, or Not Recruiting, and where Age Group is greater than 18, and an Interventional Study Type. A keyword search for 'combination' is performed in the study description. 

### Results and Conclusions

An overwhelming majority of FDA-approved drugs consist of one active compound, and clinical trials continue to rely on single drug interventions (Figure 1). Two primary forces likely drive this effect. The first is rooted in the overtly reductionist framework in biomedical research. Therapeutic-oriented research is primarily concerned with a one-at-a-time functional assessment, such as the role of a single protein in a signaling pathway, or single nucleotide polymorphism genotype-phenotype relationships. The second force is both the complexity and challenge in both designing and gaining approval for combination therapies. Combination therapy trials require more human subjects and cost, and must demonstrate greater efficacy over single therapies to win approval. Despite these challenges, there does appear to be a trend towards greater therapeutic complexity in recent years. This effect may highlight encouraging shifts in systems-level thinking in translational research and an innovative drive towards more effective therapies against hard-to-treat chronic conditions.


### References 

1. Zhou, B., Bentham, J., Di Cesare, M., Bixby, H., Danaei, G., Cowan, M. J., … Zuñiga Cisneros, J. (2017). Worldwide trends in blood pressure from 1975 to 2015: a pooled analysis of 1479 population-based measurement studies with 19·1 million participants. The Lancet, 389(10064), 37–55. https://doi.org/10.1016/S0140-6736(16)31919-5
2. Farzadfar, F., Finucane, M. M., Danaei, G., Pelizzari, P. M., Cowan, M. J., Paciorek, C. J., … Ezzati, M. (2011). National, regional, and global trends in serum total cholesterol since 1980: systematic analysis of health examination surveys and epidemiological studies with 321 country-years and 3·0 million participants. The Lancet, 377(9765), 578-586. https://doi.org/10.1016/S0140-6736(10)62038-7 
3. The GBD 2015 Obesity Collaborators. (2017). Health Effects of Overweight and Obesity in 195 Countries over 25 Years. New England Journal of Medicine, 377(1), 13–27. https://doi.org/10.1056/NEJMoa1614362 
4. Kyu, H. H., Abate, D., Abate, K. H., Abay, S. M., Abbafati, C., Abbasi, N., … Murray, C. J. L. (2018). Global, regional, and national disability-adjusted life-years (DALYs) for 359 diseases and injuries and healthy life expectancy (HALE) for 195 countries and territories, 1990–2017: a systematic analysis for the Global Burden of Disease Study 2017. The Lancet, 392(10159), 1859–1922. https://doi.org/10.1016/S0140-6736(18)32335-3 

