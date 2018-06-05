
# coding: utf-8

# # Setup

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
db = {'username': 'dbusr',  #os.environ['USERNAME_11323671'],
      'password': 'dbpw',  #os.environ['PASSWORD_11323671'],
      'host': 'localhost',  # 'quantleap.nl:5432',
      'catalog': 'qir'}

con = 'postgresql://{username}:{password}@{host}/{catalog}'.format(**db)
engine = create_engine(con, echo=True)
print('CONNECTION ESTABLISHED')


# # Judges

# ## Example of non normalized judge names:
#  
#  - "mr. W.J.  Geurts - de Veld"
#  - "mr. W.J. Geurts - de Veld"
#  - "mr. W.J. Geurts-deVeld"
#  - "mr. W.J. Geurts-de Veld"
#  - "mr. W.J.Geurts-de Veld"
#  - "mr.W.J. Geurts-de Veld"
#  - "mr. W.J. Geurts-de Veld (Rotterdam)"
#  - "mr W.J.Geurts-de Veld"
#  - "W.J.Geurts-de Veld"
#  
#  correct: "mr. W.J. Geurts-de Veld"
#  normalized: "wj geurts-de veld"
#  
#  normalization steps:
#  1. make lowercase
#  2. remove leading mr[.]
#  3. remove spaces around dash
#  4. remove dots
#  5. replace double spaces by single space
#  6. remove parentheses and text within
#  7. strip leading and trailing spaces 

# ## normalisering van de namen

# ## golden standard - nevenfunctieregister, already scraped by openstate (up to date?)

# ## API voor nevenfuncties
# Open Rechtspraak bevat nu tevens ook een heuse API (application programming interface) voor nevenfuncties. Dit is een RESTFULL api welke twee apicalls ondersteunt:
# 
# 1. http://ors.openstate.eu/index.php/relations/json geeft een overzicht van alle nevenfuncties met URL's naar de JSON pagina
# 
# 2. http://ors.openstate.eu/relations/instantie/RECHTBANK/NAAM/json Naam en Rechtbank dienen in URL ENCODE gecodeerd te zijn, cf. de lijst van punt 1.
# 
# Voorbeeld: http://ors.openstate.eu/relations/instantie/Rechtbank+Amsterdam/mw.+mr.+J.F.+Aalders+/json

# In[ ]:


# rechters_df = pd.read_html('http://ors.openstate.eu/relations')[0]
rechters_df = pd.read_json('http://ors.openstate.eu/relations/json')
rechters_df.head()A


# In[ ]:


rechters_df[rechters_df['set'] == 'Rechtbank Amsterdam']


# In[2]:




