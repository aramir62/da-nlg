import sys
sys.path.append('../../../..')

import pandas as pd
from sacrebleu.metrics import BLEU
from sacrebleu import sentence_bleu,corpus_bleu

print ('Loading file...')
df = pd.read_csv('../data/video_game/test.csv')
# df = pd.read_csv('../data/video_game/sampled_var7.csv')
df = df.dropna(subset = ['text'])
df.head()

selected, df_criteria = [], []
next_criteria = {'SACC':'PSEUDO BLEU','PSEUDO BLEU':'PPL'}
sort_criteria = {'SACC':'max','PSEUDO BLEU':'max','PPL':'min'}

# if da correct > 1
#   sort highest sacc 
#       highest pseudo-bleu
#           lowest ppl
                # random

#if da correct = 0
    # select other
        # same process


def shortlist(group,criteria,column):
    '''
    group: pandas dataframe 
    criteria: string used for tracking the selection criteria
    column: column in group which will be used for ranking at current stage (SACC, BLEU, PPL)
    '''

    criteria += "_"+column

    type = sort_criteria[column]
    # print ('GRP',column,group,group['text'])
    
    #for single words ppl is not defined
    if column=='PPL' and len(group.dropna(subset=['PPL']))==0:
        group['PPL'] = 0.0

    if type=='max':
        group = group[group[column]==group[column].max()]
    else:
        group = group[group[column]==group[column].min()]

    if len(group)>1:
        if column =='PPL':
            group = group.sample(1)
        else:
            group, criteria = shortlist(group,criteria,next_criteria[column]) #recursive function to next criteria
    # print ('!!!!',column,criteria,group)
    return group, criteria


for i, grp in df.groupby('Id'):

    criteria = 'match'
    _grp = grp[grp['MR_DA']==grp['DA']] # 1: if MR_da matches predicted DA
    
    if len(_grp)==0:
        _grp = grp[grp['DA']=='other'] # 1: if MR_DA does not match, selected others
        criteria='other'
        
        if len(_grp)==0: # 1: if there is no other, then select all rows
            _grp = grp
            criteria = 'all'

    if len(_grp)>1:
        _grp, criteria = shortlist(_grp,criteria=criteria,column='SACC') # 2: Select using SACC
    try:
        selected.append(_grp.index[0])
    except:
        print (_grp,grp,criteria)
        raise
    df_criteria.append(criteria)

# assert len(df_criteria)==360
print (len(df_criteria))

df = df.loc[selected]
df['criteria'] = df_criteria
print (df)

from collections import  Counter
print (Counter(df_criteria).most_common())

df['bleurt_max'] = df[['bleurt_ref1','bleurt_ref2','bleurt_ref3']].max(axis=1)
df['bert_max'] = df[['bertsc_ref1','bertsc_ref2','bertsc_ref3']].max(axis=1)

df.to_csv('../data/video_game/ranked.csv',index=True)
df = pd.read_csv('../data/video_game/ranked.csv')
# df = df.astype('str')

mean_ps = round(df['PSEUDO BLEU'].mean(),4)
print (f'Pseudo bleu average:{mean_ps}')

refs = df[['ref1','ref2','ref3']].values.tolist()
pred  = df['text'].tolist()
print (f'Corpus_bleu: {corpus_bleu(pred, refs)}')

mean_bl = round(df['bleurt_max'].mean(),4)
print (f'BLEURT average of max:{mean_bl}')

mean_be = round(df['bert_max'].mean(),4)
print (f'BERT Score average of max:{mean_be}')

mean_sacc = round(df['SACC'].mean(),4)
print (f'SACC Score average:{mean_sacc}')

perf_sacc = sum(df['SACC Perfect'])
print ('perfect SACC percent: ',perf_sacc/len(df))

perf_da = sum(df['DA Perfect'])
print ('perfect DA percent: ',perf_da/len(df))

perf_dasacc = sum((df['DA Perfect']==1)&(df['SACC Perfect']==1))
print ('perfect SACC+DA percent: ',perf_dasacc)
