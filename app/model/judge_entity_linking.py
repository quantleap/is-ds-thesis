# -*- coding: utf-8 -*
import pandas as pd

from app.model import con


def report_busy_judges():
    """ report number of active cases per judge. """
    sql = """select full_name, count(*) from active_company_bankrupt_insolvents_view i 
             join register_judges rj on i.register_judge_id = rj.id
             group by 1
             order by 2 desc;"""
    df = pd.read_sql(sql, con)
    print(df)


if __name__ == "__main__":
    report_busy_judges()
