
# coding: utf-8

# # Setup

# In[ ]:


#import pdb; pdb.set_trace()

get_ipython().magic('matplotlib inline')
import pandas as pd
import os
import re
import json


# In[ ]:


# connection to the database
import os
from sqlalchemy import create_engine

# set username/password here:
db = {'username': os.environ['USERNAME_11323671'],
      'password': os.environ['PASSWORD_11323671'],
      'host': 'quantleap.nl:5432',
      'catalog': 'qir'}

con = 'postgresql://{username}:{password}@{host}/{catalog}'.format(**db)
engine = create_engine(con, echo=True)
print('CONNECTION ESTABLISHED')


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
         where supervisory_judge notnull
         order by 1"""

non_normalized_name = pd.read_sql(sql, con)

def normalize_judge_name(name):
    return name.replace(r"\(.*\)","")
    

non_normalized_name['supervisory_judge'].apply(normalize_judge_name)[0:10]


# In[ ]:


# rechters_df = pd.read_html('http://ors.openstate.eu/relations')[0]
rechters_df = pd.read_json('http://ors.openstate.eu/relations/json')


# In[ ]:


rechters_df


# In[ ]:


rechters_df[rechters_df['set'] == 'Rechtbank Amsterdam']


# # Verslagen

# ## Split voortgangs vs financiele rapportages

# In[ ]:


sql = """select 
           count(*), 
           count(*)::decimal/(select count(*) from reports)*100 as pct, 
           right(identification, 1) = 'B' as is_financial_report
         from reports
         group by 3;"""
pd.read_sql(sql, con)


# ## Split PDF was scanned vs converted

# In[ ]:


sql = """select 
           count(*), 
           count(*)::decimal/(select count(*) from reports)*100 as pct, 
           is_ocr as was_scanned
         from reports
         group by 3;"""
pd.read_sql(sql, con)


# todo: run new classifier over all pdfs on S3 for unknowns

# ## praktijk van het rapporteren voortgangsverslagen met/zonder financiele bijlage

# In[ ]:


sql = """select * from progess_financial_report_cooccurence;"""
df = pd.read_sql(sql, con)
df = df.transpose()
df.columns = ['count']
df['pct'] = df['count']/df['count'].sum()*100
df


# ## rapportages over tijd

# In[ ]:


sql = """
with
financial as (
      select to_char(publication_date, 'YYYY-MM') as month,
             count(*) as financial_count
      from reports
      where right(identification, 1) = 'B'
      group by 1),
progress as (
      select to_char(publication_date, 'YYYY-MM') as month,
             count(*) as progres_count
      from reports
      where right(identification, 1) != 'B'
      group by 1)
select prog.month as maand, progres_count as voortgangsverslag, coalesce(financial_count, 0) as financieelverslag
  from financial fin
    full outer join progress prog on fin.month = prog.month
  order by prog.month;
"""
df = pd.read_sql(sql, con, index_col="maand")
df.plot.bar(stacked=True, figsize=(20, 5), title='publicaties per maand')


# ## steekproef van niet OCR eindverslagen

# In[ ]:


sql = '''SELECT identification, publication_date, is_end_report, content, start_date_insolvency
         FROM reports rep
             JOIN company_insolvents ins ON rep.insolvent_id = ins.id
         WHERE rep.is_end_report = TRUE
             AND is_ocr is FALSE
         ORDER BY publication_date DESC
         LIMIT 1000;'''

df_reports = pd.read_sql(sql, con, index_col='identification')
df_reports.head()


# ## Data field wish list from the PDF report

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

# ### Bevindingen / Issues
# - Bij insolventen van verslagen 13_ams_15_478_F_V_06 en 10_rot_12_90_F_V_16 zijn geen enkele financiele verslagen ook curator salaris wordt niet genoemd. Vraag: wie levert geen financieel verslag en waarom?
# - Bij eindverslag 10_rot_14_1054_F_V_10 staat curator salaris alleen in de financiele bijlage. Er lijkt ook sprake van een schikking - regeling bestuurder: 22.000 - wegens rechtmatigheidsissue. 
# - bij 11_rot_12_41_F_V_15 staan bedragen doorgestreept, textconversie pakt dat niet
# - De eindverslagen zijn niet echt eindverslagen: 'Naar verwachting zal het faillissement in de komende
# verslagperiode eindigen.' (11_rot_12_41_F_V_15)
# - uurtarief bij 11_rot_12_41_F_V_15 komt op 280,-
# - 10_rot_14_1054_F_V_10, 01_obr_13_293_F_V_09 omzetting pdf>txt verliest letters/gegevens/structuur met PDFMiner. Welke converter pakt dit goed aan ?
# - strikethrough in PDF komt niet terug in de tekstconversie

# ## Extracting structured text from PDF reports

# ### Kandidaat sectie headers

# In[ ]:


# Step 1: extract sections from progress reports
# Sub step: extract candidate sections from model report
model_content = open('model-verslag-faillissement-rechtspersoon.txt', 'r').read()

def match_headings(content, level=2):
    """ returns level 2 (e.g. 1.1) heading matches as tuple (heading number, heading title)"""
    flags = re.MULTILINE
    if level == 2:
        pattern = r"^\s*(\d{1,2}\.\d{1,2})\s*(.*)$"
    elif level == 1:
        pattern = r"^\s*(\d{1,2}\.\d{0,2})\s*(.*)$"
    else:
        raise NotImplementedError
    match = re.findall(pattern, content, flags)
    return match

model_headings = match_headings(model_content, level=1)
model_heading_numbers = list(zip(*model_headings))[0]
model_headings


# In[ ]:


report_content = df_reports['content']['01_obr_13_1204_F_V_04']
print(report_content)


# In[ ]:


report_headings = match_headings(report_content, level=1)
report_heading_numbers = list(zip(*report_headings))[0]



# In[172]:


# BREADTH FIRST SEARCH: eerst van zoveel mogelijk rapporten een zo weid mogelijk net uitgooien, dan inzoomen
# 0. eigenlijk eerst full text search op gehele content
# 1. search op sections
# 2. search op parameter values

# SECTIONS
# check hoeveel er exact matchen(ignore case)
# check hoeveel er op heading nummers matchen
# for stop anchor point we need to level 1 headings too

# ZOU MATCH OP HEADING NUMMER AL GENOEG KUNNEN ZIJN ? :
# check of heading nummers oplopen
# check of heading nummers in kandidatenlijst voorkomen

# level 1 pattern with .? yields many false positives (in first examined case)

def is_strictly_increasing_heading_numbers(heading_numbers):
    """ checks if all level 2 headings 1.1, 1.2, 3.1 etc in list are strictly increasing. """
    if heading_numbers is not None:
        return all([float(a) < float(b) for (a, b) in zip(heading_numbers, heading_numbers[1:])])
    else:
        return False
    
def only_model_headings(report_heading_numbers):
    if report_heading_numbers is not None:
        report_headings_not_in_model = set(report_heading_numbers).difference(set(model_heading_numbers))
        return len(report_headings_not_in_model) == 0
    else:
        return False


def get_heading_numbers(content):
    headings = match_headings(content)
    if headings:
        heading_numbers, _ = list(zip(*headings))
        return heading_numbers
    else:
        return None
  


print('is strictly increasing: {}'.format(is_strictly_increasing_heading_numbers(report_heading_numbers)))
print('all headings report in model: {}'.format(all_report_headings_in_model(report_heading_numbers, model_heading_numbers)))


# In[ ]:


# store matched headers as json strings
df_reports['headings'] = df_reports['content'].apply(lambda x: json.dumps(match_headings(x)))
df_reports['headings']


# In[ ]:


df_reports['heading_numbers'] = df_reports['content'].apply(lambda x: json.dumps(get_heading_numbers(x)))
df_reports['heading_numbers']


# In[ ]:


df_reports['strictly_increasing'] = df_reports['heading_numbers'].apply(
    lambda x: is_strictly_increasing_heading_numbers(json.loads(x)))
df_reports['strictly_increasing']


# In[115]:


# report percentage strictly increasing
df_reports['strictly_increasing'][df_reports['strictly_increasing'] == True].count() / df_reports['strictly_increasing'].count() * 100


# In[ ]:


df_reports['only_model_headings'] = df_reports['heading_numbers'].apply(
    lambda x: is_strictly_increasing_heading_numbers(json.loads(x)))
df_reports['strictly_increasing']


# In[ ]:


df_reports['only_model_headings'] = df_reports['heading_numbers'].apply(
    lambda x: only_model_headings(json.loads(x)))
df_reports['only_model_headings']


# In[114]:


# report percentage only model headings
df_reports['only_model_headings'][df_reports['only_model_headings'] == True].count() / df_reports['only_model_headings'].count() * 100


# In[174]:


# inspect not strictly increasing
df_not_increasing = df_reports[df_reports.only_model_headings & (~df_reports.strictly_increasing)]
index = 20
print(df_not_increasing.index[index])
heading_numbers = list(zip(*json.loads(df_not_increasing.headings[index])))[0]
is_strictly_increasing_heading_numbers(heading_numbers)
for a, b in zip(heading_numbers, heading_numbers[1:]):
    print(float(a), float(b), float(a)<float(b))
    
# finding: in many reports 3.10 became 3.1 even though the PDF shows 3.10, PDFMiner issue ?


# In[ ]:




