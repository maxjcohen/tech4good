import json
import datetime

import numpy as np
import pandas as pd

def filter_data(n_days=0):
    df = pd.read_csv('src/data.csv', sep='\t')

    if n_days==0:
        return filter_from_df(df)
        
    format_date = '%m/%d/%Y'
    date_list = list(map(lambda x: datetime.datetime.strptime(x, format_date), df.iloc[:, 4]))

    time_days = datetime.timedelta(days=n_days)
    threshold = datetime.datetime.now() - time_days
    filtered_df = df.iloc[np.where(np.array(date_list)>threshold)]
    return filter_from_df(filtered_df)

def filter_from_df(df):
    df_filled = df.fillna(0, inplace=True)
    df_local = df.groupby(['Votre délégation départementale']).sum()
    data = {'actions': {'visites': {}, 'permanences': {}, 'formation': {}, 'prevention': {}, 'participants': {}}}
    for index, row in df_local.iterrows():
        data['actions']['visites'][index] = {'total': row[0], 'femmes': row[1], 'hommes': row[2], 'trans': row[3]}        
        data['actions']['permanences'][index] = {'total': row[5], 'femmes': row[6], 'hommes': row[7], 'trans': row[8]}
        data['actions']['formation'][index] = {'total': row[9]}
        data['actions']['participants'][index] = {'total': row[11]} 
        data['actions']['prevention'][index] = {'total': row[10]}
    data['benevoles'] = df['test'].nunique() 
    return data

