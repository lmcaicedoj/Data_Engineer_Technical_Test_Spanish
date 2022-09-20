# ETL

import pandas as pd
from pandas import json_normalize
import requests
import datetime
import requests
import json
import config

# (1) Extract:
API_KEY = config.api_key

date_list = []
for i in range(1,32):
     x = datetime.datetime(2020, 12, i)
     date_list.append(x.strftime('%Y-%m-%d'))


url = 'http://api.tvmaze.com/schedule'
web = 'web?date='

API_ = []
List_url = []
for t in date_list:
    API_ = '{}/{}{}'.format(url, web, t)
    List_url.append(API_)

API_2 = []
List_txt = []
List_json = []
list_dfs = []

for j in List_url:
   API_2 = requests.get(j)
   List_txt.append(API_2.text)
   json_file = json.loads(API_2.text)
   List_json.append(json_file)
   df_all = json_normalize(json_file)
   list_dfs.append(df_all)
   
# (2) Transform:
list_all_data = []
for i in list_dfs:
    list_all_data.append(i[['id','url','name','season','type','airdate','_embedded.show.genres',
                             '_embedded.show.status','_embedded.show.premiered','_embedded.show.webChannel.country.name',
                             '_embedded.show.webChannel.country.code','_embedded.show.averageRuntime','rating.average']])
   
df_all_data = pd.concat(list_all_data, ignore_index=True)

# (2.1) Format: 
df_all_data['_embedded.show.webChannel.country.name'] = df_all_data['_embedded.show.webChannel.country.name'].astype(str)
df_all_data['_embedded.show.webChannel.country.code'] = df_all_data['_embedded.show.webChannel.country.code'].astype(str)

df_all_data['type'] = df_all_data['type'].astype('category')
df_all_data['type'] = df_all_data['type'].cat.codes

df_all_data['airdate'] = df_all_data['airdate'].astype('datetime64[ns]')

# (2.2) Creating a new column:
df_all_data.insert(13,'name_complete','',True)
for i in range(0,len(df_all_data['url'])):
        trail = df_all_data['url'].loc[i].split("/")[-1:]
        df_all_data['name_complete'].loc[i] = trail[0]

# Load:

df_all_data.to_csv('c:/Users/luisc/Downloads/2022-09-16_Prueba_Tecnica_2/tv_series_db.csv', index=False)
#print(df_all_data)