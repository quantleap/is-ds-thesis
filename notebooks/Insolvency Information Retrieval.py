
# coding: utf-8

# #### Setup

# In[1]:


#import pdb; pdb.set_trace()

get_ipython().magic('matplotlib inline')
import pandas as pd
import os
import re
import json

# connection to the database
import os
from sqlalchemy import create_engine

# set username/password here:
db = {'username': os.environ['DB_QIR_USERNAME'],
      'password': os.environ['DB_QIR_PASSWORD'],
      'host': 'www.quantleap.nl',  # localhost
      'catalog': 'qir'}


con = 'postgresql://{username}:{password}@{host}/{catalog}'.format(**db)
engine = create_engine(con, echo=True)
print('CONNECTION ESTABLISHED')


# # Insolvents

# In[2]:


sql = """select count(distinct case_number) 
         from company_insolvents"""

no_insolvents = pd.read_sql(sql, con).iloc[0][0]
print('the total number of insolvents cases in the database is {}'.format(no_insolvents))


# In[3]:


sql = """select start_date_insolvency is not null as known, count(*)
         from company_insolvents
         group by start_date_insolvency is not null"""

df_known_start_date = pd.read_sql(sql, con)
print('fraction of known start date')
df_known_start_date


# In[4]:


df_known_start_date.plot.pie(y='count', labels=df_known_start_date['known'])


# In[5]:


# rechters_df = pd.read_html('http://ors.openstate.eu/relations')[0]
rechters_df = pd.read_json('http://ors.openstate.eu/relations/json')


# In[183]:


rechters_df


# In[184]:


rechters_df[rechters_df['set'] == 'Rechtbank Amsterdam']


# ## steekproef van niet OCR eindverslagen

# ### Wenselijke datavelden in het voortgangsverslag
# Het voortgangsverslag hoort gestructureerd te zijn volgens de RECOFA richtlijnenm zie **model-verslag-faillissement-rechtspersoon.pdf**. In eerste instantie zijn we geinteresseerd in de data uit de **eindverslagen**.
# 
# Algemeen
# - Personeel gemiddeld aantal: aantal
# - Bestede uren totaal: aantal
# - Saldo boedelrekening: bedrag
# 
# 
# 4 Debiteuren
# 
# 4.2 Opbrengst: bedrag
# 
# 
# 7 Rechtmatigheid
# 
# 7.2 Depot jaarrekeningen: wel/niet 
# 
# 7.5 Onbehoorlijk bestuur: wel/niet
# 
# 
# 8 Crediteuren
# 
# 8.1 Boedelvorderingen: bedrag (salaris curator / UWV / ..)
# 
# 8.2 Preferente vorderingen van de fiscus: bedrag
# 
# 8.3 Preferente vorderingen van het UWV: bedrag
# 
# 8.4 Andere preferente vorderingen: bedrag
# 
# 8.5 Aantal concurrente crediteuren: bedrag
# 
# 8.6 Bedrag concurrente crediteuren: bedrag
# 
# 

# ### Enige bevindingen / Issues
# - Bij insolventen van verslagen 13_ams_15_478_F_V_06 en 10_rot_12_90_F_V_16 zijn geen enkele financiele verslagen ook curator salaris wordt niet genoemd. Vraag: wie levert geen financieel verslag en waarom?
# - Bij eindverslag 10_rot_14_1054_F_V_10 staat curator salaris alleen in de financiele bijlage. Er lijkt ook sprake van een schikking - regeling bestuurder: 22.000 - wegens rechtmatigheidsissue. 
# - bij 11_rot_12_41_F_V_15 staan bedragen doorgestreept, textconversie pakt dat niet
# - De eindverslagen zijn niet echt eindverslagen: 'Naar verwachting zal het faillissement in de komende
# verslagperiode eindigen.' (11_rot_12_41_F_V_15)
# - uurtarief bij 11_rot_12_41_F_V_15 komt op 280,-
# - 10_rot_14_1054_F_V_10, 01_obr_13_293_F_V_09 omzetting pdf>txt verliest letters/gegevens/structuur met PDFMiner. Welke converter pakt dit goed aan ?
# - strikethrough in PDF komt niet terug in de tekstconversie
# - PDFMiner wisselt soms woordvolgorde en mangled soms letters ook al staat dit duidelijk in het PDF

# In[276]:


# store matched headers as json strings
df_reports['headings'] = df_reports['content'].apply(lambda x: json.dumps(match_headings(x)))
df_reports['headings'].head(n=20)


# In[277]:


df_reports['heading_numbers'] = df_reports['content'].apply(lambda x: json.dumps(get_heading_numbers(x)))
df_reports['heading_numbers'].head(n=20)


# In[278]:


# 
df_reports['strictly_increasing'] = df_reports['heading_numbers'].apply(
    lambda x: is_strictly_increasing_heading_numbers(json.loads(x)))
df_reports['strictly_increasing'].head(n=20)


# In[279]:


# report percentage strictly increasing
df_reports['strictly_increasing'][df_reports['strictly_increasing'] == True].count() / df_reports['strictly_increasing'].count() * 100


# In[280]:


df_reports['only_model_headings'] = df_reports['heading_numbers'].apply(
    lambda x: is_strictly_increasing_heading_numbers(json.loads(x)))
df_reports['strictly_increasing'].head(n=20)


# In[281]:


df_reports['only_model_headings'] = df_reports['heading_numbers'].apply(lambda x: has_only_model_heading_numbers(json.loads(x)))
df_reports['only_model_headings'].head(n=20)


# In[282]:


# report percentage only model headings
df_reports['only_model_headings'][df_reports['only_model_headings'] == True].count() / df_reports['only_model_headings'].count() * 100


# In[283]:


# inspect cases only model heading numbers but not strictly increasing
df_not_increasing = df_reports[df_reports.only_model_headings & (~df_reports.strictly_increasing)]
index = 20
print(df_not_increasing.index[index])
heading_numbers = list(zip(*json.loads(df_not_increasing.headings[index])))[0]
is_strictly_increasing_heading_numbers(heading_numbers)
for a, b in zip(heading_numbers, heading_numbers[1:]):
    print(float(a), float(b), float(a)<float(b))
    
# finding: in many reports 3.10 became 3.1 even though the PDF shows 3.10, PDFMiner issue ?


# In[284]:


# count heading number in model collection
df_reports['no_headings'] = df_reports['heading_numbers'].apply(
    lambda x: json.loads(x))
df_reports['only_model_headings'].head(n=20)

