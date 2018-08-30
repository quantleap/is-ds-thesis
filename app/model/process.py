# -*- coding: utf-8 -*
import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sqlalchemy import func
from app.model.common import query_insolvents
from cir.models import Insolvent
from datetime import date

logger = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
def insolvency_start_date_completeness(only_active=True, cutoff_date=date(2014, 1, 1)):
    """ Returns a dict with insolvency start date completeness information. """
    result = query_insolvents((Insolvent.start_date_insolvency.isnot(None).label('with_start_date'), func.count('*')),
                              only_active)\
        .filter(Insolvent.start_date_insolvency >= cutoff_date) \
        .group_by('with_start_date').all()

    # create result dict
    assert result[0][0] is True  # with start date exists
    no_with = result[0][1]
    no_without = result[1][1] if len(result) == 2 else 0
    result_dict = {'with_start_date': no_with,
                   'without_start_date': no_without,
                   'completeness': no_with / (no_with+no_without)}
    return result_dict


# noinspection PyUnresolvedReferences
def insolvency_start_date_count(cutoff_date=date(2014, 1, 1)):
    """ Returns a series of count of new insolvencies per day. """
    result = query_insolvents((Insolvent.start_date_insolvency,), only_active=False) \
        .filter(Insolvent.start_date_insolvency >= cutoff_date) \
        .filter(Insolvent.start_date_insolvency.isnot(None)).all()

    # convert dates to pandas datetime64
    dates = [pd.to_datetime(r[0]) for r in result]

    # results contain duplicate dates, group by date and count results
    s = pd.Series(data=1, index=dates).groupby(level=0).count()
    return s


def plot_insolvency_start_date_count(s):
    """ Returns a plot figure using data series. """
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(1, 1)
    s.plot(kind="bar", ax=ax, figsize=(10, 6), title='new bankruptcies per month', color='blue')
    tick_labels = [item.strftime('%m') for item in s.index]
    tick_labels[::12] = [item.strftime('%Y-%m') for item in s.index[::12]]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(tick_labels))
    return fig


def _save_figure(fig, fname):
    """ Saves a figure in static folder. """
    fig.savefig(os.path.join(os.path.dirname(__file__), '../static/', fname))


def refresh_insolvency_start_date_count_figure():
    """ Refreshes the saved plot for insolvency start date histo. """
    s = insolvency_start_date_count().resample('M').sum()
    fig = plot_insolvency_start_date_count(s)
    _save_figure(fig, 'insolvency_start_date_count.png')


if __name__ == "__main__":
    refresh_insolvency_start_date_count_figure()
