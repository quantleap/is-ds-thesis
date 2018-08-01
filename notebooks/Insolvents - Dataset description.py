
# coding: utf-8

# #### Setup

# In[5]:


#import pdb; pdb.set_trace()

get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import json
import psycopg2
from sqlalchemy.engine.url import URL

# connection to the database
# connection string for use in pandas:
con = str(URL(drivername='postgresql', 
              username=os.environ['DB_QIR_USERNAME'], 
              password=os.environ['DB_QIR_PASSWORD'], 
              host='www.quantleap.nl', 
              #host='localhost', 
              database='qir'))

# cursor for use with psycopg2
conn = psycopg2.connect(con)
cur = conn.cursor()  
print('CONNECTION ESTABLISHED')


# # Insolvency types
# insolvencies can be of different types:
# - schuldsanering (R)
# - surseance (S)
# - Fallissement (F)
# 
# and can involve a (person_legal_personality)
# - rechtspersoon 
# - natuurlijk persoon

# In[6]:


sql = """select insolvency_type, person_legal_personality from insolvents;"""
df = pd.read_sql(sql, con)

pd.pivot_table(df, values='insolvency_type', index=['insolvency_type'],
                    columns=['person_legal_personality'], aggfunc=lambda x: len(x))


# We are interested in companies in bankrupcty, the F/rechtspersoon combination.
# 

# In[16]:


# use views that filter F/rechtspersoon
sql = """select count(*) from company_bankrupt_insolvents_view;"""
pd.read_sql(sql, con)


# In[14]:


# .. of which currently active
sql = """select count(*) from active_company_bankrupt_insolvents_view;"""
pd.read_sql(sql, con)


# # Process Mining of Insolvency Processes
# Using process mining we like to get information on the flow of insolvency cases through the court system. 
# There are two sources where the state of the insolvency case is logged:
# 
# 1. structured: in the court publication description and type code
# 2. unstructuctured: a variety of information in the progress reports
# 
# 
# # set start date insolvency using publication.type_code
# This field is derived from the publication type code. Certain type codes indicate the start of the insolvency, other the end.
# 
# 
# ## start date insolvency completeness

# In[10]:


sql = """select * from active_company_bankrupt_insolvents_view;"""
df_available_insolvents = pd.read_sql(sql, con)


# In[12]:


s = df_available_insolvents.start_date_insolvency.notnull()
has_start_date = s.groupby(s).size()
pd.DataFrame({'count': has_start_date, 'pct': has_start_date/has_start_date.sum()})


# results start data insolvency from court publication on active insolvents:
#                         count	pct
# start_date_insolvency		
# False	                973	    0.055676
# True	                16503	0.944324

# ### Result discussion
# It appears that a small portion of unknown start dates is caused by the left censoring of data: the initial publication relating to the start of the default was not included in the dataset, CIR began slowly in 2010 and only fully around 2014.
# 
# But the analysis shown below suggests otherwise, most cases without start date are from the years 2014-2015. Needs further analysis, many cases are transferred to another court.
# 
# Other sources for the start date are:
# 1. start date administrator
# 2. start date address insolvent

# ### how do cases start out

# In[ ]:


sql = """
create temp table publication_types (type_code varchar, description  varchar);
insert into publication_types (type_code, description) values
  ('1100', 'uitspraak faillissement in hoger beroep'),
  ('1200', 'uitspraak faillissement in cassatie'),
  ('1300', 'uitspraak faillissement'),
  ('1301', 'uitspraak faillissement door tussentijdse beëindiging schuldsanering'),
  ('1302', 'uitspraak faillissement tijdens schuldsanering'),
  ('1303', 'uitspraak faillissement door ontbinding akkoord in schuldsanering '),
  ('1304', 'heropening faillissement door ontbinding akkoord in faillissement'),
  ('1305', 'uitspraak faillissement door ontbinding akkoord in surseance'),
  ('1306', 'uitspraak faillissement na beëindiging surseance '),
  ('3313', 'Beëindiging door omzetting in faillissement');
with available_insolvents as 
    (select * from insolvents where person_legal_personality = 'rechtspersoon' and type = 'F'
     --and is_removed is False and (end_findability > current_date or end_findability is null)
     ),
with_start_date_ins as (select * from insolvents where start_date_insolvency is not NULL)
  select pub.type_code, pt.description, count(*)
    from with_start_date_ins ins
      join publications pub on ins.id = pub.insolvent_id
      join publication_types pt on pt.type_code = pub.type_code
    where pub.type_code in ('1100', '1200', '1300', '1301', '1302', '1303', '1304', '1305', '1306', '3313')
  group by 1, 2
order by count desc;
"""
df = pd.read_sql(sql, con)
df.style


# #### Results
# We can determine how cases start out. This can be sliced to a period, court, etc.<br>
# Using a stacked area graph it can be shown how cases endings change over time.

# ### how do cases end

# In[ ]:


sql = """
create temp table publication_types (type_code varchar, description  varchar);
insert into publication_types (type_code, description) values
('1102', 'vernietiging faillissement in hoger beroep'),
('1202', 'vernietiging faillissement in cassatie'),
('1316', 'opheffing faillissement wegens gebrek aan baten'),
('1317', 'einde faillissement door verbindende uitdelingslijst'),
('1318', 'einde faillissement door goedkeuring akkoord'),
('1319', 'einde faillissement door verbindende uitdelingslijst na verzet'),
('1320', 'vernietiging faillissement na verzet'),
('1324', 'einde faillissement door voldoen van alle schulden'),
('1333', 'Faillissement omgezet in schuldsanering');

with available_insolvents as 
    (select * from insolvents where person_legal_personality = 'rechtspersoon' and type='F'
     --and is_removed is False and (end_findability > current_date or end_findability is null)
     ),
with_end_date_ins as (select * from insolvents where end_date_insolvency is not NULL)
  select pub.type_code, pt.description, count(*)
    from with_end_date_ins ins
      join publications pub on ins.id = pub.insolvent_id
      join publication_types pt on pt.type_code = pub.type_code
    where pub.type_code in ('1102', '1202', '1316', '1317', '1318', '1319', '1320', '1324', '1333')
  group by 1, 2
order by count desc;
"""
df = pd.read_sql(sql, con)
df.style.set_properties()


# ## Intermediate states
# Apart from beginning and end state many intermediate states can be identified from the data. One example is the moment of setting the verification meeting for which a timing constraint is set by the law.
# 
# ### when are verification meetings set
# Verfification meetings are supposed to be schedules (not held) within 14 days after the publication of bankruptcy. This demand is seen as a dead letter to be changed with the new law from 2019-1-1 onwards. From the distribution is can be seen that this deadline is almost never met, on the contrary, it appears breached up to a point that it needs further inspection.

# In[ ]:


sql = """
with available_insolvents as
  (select * from insolvents where person_legal_personality = 'rechtspersoon' and type='F'
                             and start_date_insolvency is not null
                             and is_removed is False
                             and (end_findability > current_date or end_findability is null)
                             --limit 1000
  ),
  min_pub_dates as (select case_number, (select min(p.date) from publications p
                                             join available_insolvents i2 on p.insolvent_id = i2.id
                                             where i2.id = i1.id
                                               and p.type_code in ('1309', '1310', '1325', '1326',
                              '2310', '2311', '2312', '2313', '2314', '2315', '2316', '2317', '2318',
                              '2338', '2339', '2340', '2341', '2342', '2343', '2344', '2345', '2346', '2347')
                                             ) as min_pub_date,
                           start_date_insolvency
                    from available_insolvents i1)
select start_date_insolvency, case_number, min_pub_date - start_date_insolvency as days_after_start
from min_pub_dates where min_pub_date is not null
order by 1 desc, 2, 3 desc;"""
df = pd.read_sql(sql, con)


# In[ ]:


df.days_after_start.plot.hist(bins=50);


# In[ ]:


# see recent breaches
df[df.start_date_insolvency > datetime.date(2016, 1, 1)].plot.hist(bins=50)

# this data is right censored, cases which not yet had a verification meeting publication are not seen.


# In[ ]:


# see recent breaches
import datetime
df[df.start_date_insolvency > datetime.date(2016, 1, 1)].sort_values(by=['days_after_start'], ascending=False).head(20)


# In[ ]:


# pull a file e.g. the second
sql = """
select case_number, date, type_code, description, start_date_insolvency
from insolvents i join publications p on i.id = p.insolvent_id
where case_number = 'F.03/16/31'
order by date;
"""
pd.read_sql(sql, con).style


# In[ ]:




