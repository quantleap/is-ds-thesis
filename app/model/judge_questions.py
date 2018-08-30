# -*- coding: utf-8 -*
import pandas as pd

from model import session
from model.common import get_active_bankrupt_insolvents_by_judge
from model.judge_models import RegisterJudge
from thesis import con


def number_of_active_cases_per_judge():
    sql = """select rj.id, full_name as judge_name, count(*) as no_active_cases from active_company_bankrupt_insolvents_view i 
             join register_judges rj on i.register_judge_id = rj.id
             group by 1, 2
             order by 3 desc, 2;"""
    df = pd.read_sql(sql, con)
    print(df)


def duration_active_cases_by_judge(judge_id):
    judge = session.query(RegisterJudge).get(judge.id)
    get_active_bankrupt_insolvents_by_judge(judge)
    pass


if __name__ == "__main__":
    duration_active_cases_by_judge(2507)
