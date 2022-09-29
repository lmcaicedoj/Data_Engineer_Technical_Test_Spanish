# ETL

import pandas as pd
import numpy as np
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

df_all_data.insert(12,'Tipo_#','',True)
for i in range(0, len(df_all_data['type'])):
     df_all_data['Tipo_#'].loc[i] = df_all_data['type'].loc[i]


df_all_data['Tipo_#'] = df_all_data['Tipo_#'].astype('category')
df_all_data['Tipo_#'] = df_all_data['Tipo_#'].cat.codes

df_all_data['airdate'] = df_all_data['airdate'].astype('datetime64[ns]')

# (2.2) Creating new columns:
# Complete name of the serie:
df_all_data.insert(13,'name_complete','',True)
for i in range(0,len(df_all_data['url'])):
        trail = df_all_data['url'].loc[i].split("/")[-1:]
        df_all_data['name_complete'].loc[i] = trail[0]

# Extract all the diffent Genres:
trail = []
df_all_data.insert(14,'Genero_1','',True)
df_all_data.insert(15,'Genero_2','',True)
df_all_data.insert(16,'Genero_3','',True)
df_all_data.insert(17,'Genero_4','',True)
for i in range(0, len(df_all_data['_embedded.show.genres'])):
     trail = df_all_data['_embedded.show.genres'].loc[i]
     if trail == []:
        df_all_data['Genero_1'].loc[i] = ''
        df_all_data['Genero_2'].loc[i] = ''
        df_all_data['Genero_3'].loc[i] = ''
        df_all_data['Genero_4'].loc[i] = ''
     else:
        len_trail = len(trail)
        if len_trail == 1:
           df_all_data['Genero_1'].loc[i] = trail[0]
           df_all_data['Genero_2'].loc[i] = ''
           df_all_data['Genero_3'].loc[i] = ''
           df_all_data['Genero_4'].loc[i] = ''
        elif len_trail == 2:
            df_all_data['Genero_1'].loc[i] = trail[0]
            df_all_data['Genero_2'].loc[i] = trail[1]
            df_all_data['Genero_3'].loc[i] = ''
            df_all_data['Genero_4'].loc[i] = ''
        elif len_trail == 3:           
            df_all_data['Genero_1'].loc[i] = trail[0]
            df_all_data['Genero_2'].loc[i] = trail[1]
            df_all_data['Genero_3'].loc[i] = trail[2]
            df_all_data['Genero_4'].loc[i] = ''
        elif len_trail == 4:      
            df_all_data['Genero_1'].loc[i] = trail[0]
            df_all_data['Genero_2'].loc[i] = trail[1]
            df_all_data['Genero_3'].loc[i] = trail[2]
            df_all_data['Genero_4'].loc[i] = trail[3]
        else:
            print('Careful there are list of genre larger than 4')    

# Renaming the columns in Spanish:
df_all_data.rename(columns = {'id':'id_unico','url':'pag_web', 'name':'Episodio', 'season':'Temporada','type':'Tipo',
                              'airdate':'Fecha_alaire', '_embedded.show.genres': 'Genero',
                             '_embedded.show.status': 'Estado_Film','_embedded.show.premiered': 'Premier','_embedded.show.webChannel.country.name': 'Pais',
                             '_embedded.show.webChannel.country.code':'Cod_Pais','_embedded.show.averageRuntime':'Avg_Runtime','rating.average':'Avg_rating',
                               'name_complete':'Nombre_Completo'}, inplace = True)

# Giving a code number to Status and Genre:
df_all_data.insert(18,'Estado_Film_#','',True)
df_all_data.insert(19,'Genero_1_#','',True)

trail = []
for i in range(0, len(df_all_data['Genero'])):
     df_all_data['Estado_Film_#'].loc[i] = df_all_data['Estado_Film'].loc[i]
     df_all_data['Genero_1_#'].loc[i] = df_all_data['Genero_1'].loc[i]

df_all_data['Estado_Film_#'] = df_all_data['Estado_Film_#'].astype('category')
df_all_data['Estado_Film_#'] = df_all_data['Estado_Film_#'].cat.codes

df_all_data['Genero_1_#'] = df_all_data['Genero_1_#'].astype('category')
df_all_data['Genero_1_#'] = df_all_data['Genero_1_#'].cat.codes

# Extracting the name of the Series:
df_all_data.insert(20,'Serie','',True)
for i in range(0,len(df_all_data['Nombre_Completo'])):
        trail = df_all_data['Nombre_Completo'].loc[i]
        c ='x'
        count = trail.count(c)
        if count == 0 :
             count_2 = trail.count('2020')  
             if count_2 >= 1:
                df_all_data['Serie'].loc[i] = trail[0:6:1] 
             else:      
                df_all_data['Serie'].loc[i] = trail[0:18:1] 
        elif count == 1:
             find_val = trail.find(c)
             if find_val <= 1:
                df_all_data['Serie'].loc[i] = trail[0:15:1] 
             else:
                df_all_data['Serie'].loc[i] = trail[0:(find_val-1):1]
        else:  
             index_h = trail.rindex('x')
             index_l = trail.index('x')
             if index_l <=1:
                df_all_data['Serie'].loc[i] = trail[0:index_h:1] 
             elif index_h > 15:
                df_all_data['Serie'].loc[i] = trail[0:index_l:1]
             else:
                df_all_data['Serie'].loc[i] = trail[0:index_h:1]

# Replaing nan with Null (or Blank):
df_all_data['Pais'].replace('nan', np.nan)
df_all_data['Cod_Pais'].replace('nan', np.nan)
df_all_data['Genero'].replace('', np.nan)

# Reorganizing the columns to the prefered order:
df_all_data_final = df_all_data.iloc[:,[0,20,3,2,13,5,8,10,9,12,4,18,7,19,14,15,16,17,11,21,1]]
#df_all_data.info()

# (3) Loading the data into csv and excel files:

df_all_data_final.to_csv('c:/Users/luisc/Downloads/2022-09-16_Prueba_Tecnica_2/tv_series_db.csv', index=False)
df_all_data_final.to_excel('c:/Users/luisc/Downloads/2022-09-16_Prueba_Tecnica_2/tv_series_db.xlsx', index=False)