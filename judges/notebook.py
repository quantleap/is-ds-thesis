# connection to the database
import re
import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

db = {'username': 'maarten',
      'password': 'logisch',
      'host': 'quantleap.nl:5432',
      'catalog': 'qir'}

con = 'postgresql://{username}:{password}@{host}/{catalog}'.format(**db)


def get_cir_judges_names():
    sql = """select distinct supervisory_judge
             from company_insolvents
             order by 1"""

    df_judges_names = pd.read_sql(sql, con)
    return df_judges_names['supervisory_judge']


def normalize_cir_judge_name(name):
    if name is None:
        return None

    name = name.strip().lower()
    if name in ('leeg', 'rc buiten arrondissement'):
        return None

    name = name.replace('- ', '-').replace(' -', '-').\
        replace('mr.', '').replace('mr ', '').\
        replace('drs ', '').replace('drs.', '').\
        replace('dhr.', '').\
        replace('mw.', '')

    name = re.sub(r'\(.*', '', name)  # remove single parentheses and the data after
    name = re.sub(' +', ' ', name)  # replace multiple spaces with one
    name = name.replace('.', '')  # remove dots

    return name.strip()


# note: y > ij
# in nevenfuncties: rechter, senior rechter, senior raadsheer

def normalize_nevenfunctie_judge_name(name):
    # strip gender
    name = name.replace('dhr.', '')\
        .replace('mw.', '')

    # strip titles
    name = name.replace('mr.', '').\
        replace('drs.', '').\
        replace('dr.', '').\
        replace('ir.', '').\
        replace('prof.', '').\
        replace('jonkheer', '')

    # remove dots
    name = name.replace('.', '')\

    return name.lower().strip()


# use 'register nevenfuncties' to retrieve correct judge names
def get_judges_choices():
    df = pd.read_csv('./data/judges-nevenfunctie.csv', names=['judges_choices'])
    return df['judges_choices']

cir_judges_name = get_cir_judges_names()
normalized_cir_judges_names = cir_judges_name.apply(normalize_cir_judge_name)
judges_choices = get_judges_choices()
normalized_judges_choices = judges_choices.apply(normalize_nevenfunctie_judge_name)

for idx, normalized_cir_judge_name in enumerate(normalized_cir_judges_names):
    if normalized_cir_judge_name:
        cir_judge_name = cir_judges_name[idx]
        (normalized_judge_choice, score, choice_idx) = process.extractOne(normalized_cir_judge_name, normalized_judges_choices, scorer=fuzz.QRatio)
        print(", ".join([cir_judge_name, normalized_cir_judge_name, normalized_judge_choice, str(score), str(choice_idx), judges_choices[choice_idx]]))


