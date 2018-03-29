
# coding: utf-8

# # Setup

# In[ ]:


get_ipython().magic('matplotlib inline')
import pandas as pd


# In[ ]:


# connection to the database
from sqlalchemy import create_engine

# set username/password here:
db = {'username': '[USER_NAME]',
      'password': '[PASSWORD]',
      'host': 'quantleap.nl:5432',
      'catalog': 'qir'}

con = 'postgresql://{username}:{password}@{host}/{catalog}'.format(**db)
engine = create_engine(con, echo=True)

print(con)


# # Insolvents

# In[ ]:


sql = """select count(distinct case_number) 
         from company_insolvents"""

no_insolvents = pd.read_sql(sql, con).iloc[0][0]
print('the total number of insolvents cases in the database is {}'.format(no_insolvents))


# In[ ]:


sql = """select start_date_insolvency is not null as known, count(*)
         from company_insolvents
         group by start_date_insolvency is not null"""

df_known_start_date = pd.read_sql(sql, con)
print('fraction of known start date')
df_known_start_date


# In[ ]:


df_known_start_date.plot.pie(y='count', labels=df_known_start_date['known'])


# # Judges

# In[ ]:


sql = """select count(supervisory_judge) as no_cases, supervisory_judge
         from company_insolvents
         group by 2
         order by 1 desc
         limit 10"""

print("top 10 judges by number of cases")
pd.read_sql(sql, con)


# ## Example of non normalized judge names:
# 
# - "mr. W.J.  Geurts - de Veld"
# - "mr. W.J. Geurts - de Veld"
# - "mr. W.J. Geurts-deVeld"
# - "mr. W.J. Geurts-de Veld"
# - "mr. W.J.Geurts-de Veld"
# - "mr.W.J. Geurts-de Veld"
# - "mr. W.J. Geurts-de Veld (Rotterdam)"
# - "mr W.J.Geurts-de Veld"
# - "W.J.Geurts-de Veld"
# 
# correct: "mr. W.J. Geurts-de Veld"
# normalized: "wj geurts-de veld"
# 
# normalization steps:
# 1. make lowercase
# 2. remove leading mr[.]
# 3. remove spaces around dash
# 4. remove dots
# 5. replace double spaces by single space
# 6. remove parentheses and text within
# 7. strip leading and trailing spaces
# 

# In[ ]:


sql = """select distinct supervisory_judge
         from company_insolvents
         order by 1"""

non_normalized_name = pd.read_sql(sql, con)

def normalize_judge_name(name):
    return name.replace(r"\(.*\)","")
    

non_normalized_name['supervisory_judge'].apply(normalize_judge_name)


# In[ ]:


# rechters_df = pd.read_html('http://ors.openstate.eu/relations')[0]
rechters_df = pd.read_json('http://ors.openstate.eu/relations/json')


# In[ ]:


rechters_df


# In[ ]:


rechters_df[rechters_df['set'] == 'Rechtbank Amsterdam']


# In[ ]:




