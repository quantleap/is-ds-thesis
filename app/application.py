# -*- coding: utf-8 -*
import logging

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from app.filters import set_jinja_filters
from app.model import session
from app.model.process import refresh_insolvency_start_date_count_figure
from cir.models import TimeStamp

from judges_register.associate_judge import get_unknown_judge

application = Flask(__name__)
Bootstrap(application)
set_jinja_filters(application)

logger = logging.getLogger(__name__)


@application.route('/')
def home():
    return render_template('home.html')


@application.route('/entities/')
def entities():
    """ Displays general information over the loaded and linked entities. """

    last_case_update = session.query(TimeStamp.last_cir_case_extraction).one()[0]
    last_report_update = session.query(TimeStamp.last_cir_report_extraction).one()[0]
    no_insolvents = session.execute('select count(1) from active_company_bankrupt_insolvents_view;').scalar()
    no_reports = session.execute("""select count(1) from active_company_bankrupt_insolvents_view i 
                                    join reports r on r.insolvent_id = i.id;""").scalar()
    no_publications = session.execute("""select count(1)-1 from active_company_bankrupt_insolvents_view i 
                                         join publications p on p.insolvent_id = i.id;""").scalar()
    unknown_judge_id = get_unknown_judge().id
    no_judges = session.execute("""select count(*) from judge_associations where register_judge_id !={}"""
                                .format(unknown_judge_id)).scalar()
    no_administrators = session.execute("""select count(distinct nova_lawyer_id)-1 from administrator_associations;""")\
        .scalar()
    no_courts = session.execute("""select count(distinct district) from courts;""").scalar()

    data = {'last_case_update': last_case_update,
            'last_report_update': last_report_update,
            'no_insolvents': no_insolvents,
            'no_reports': no_reports,
            'no_publications': no_publications,
            'no_judges': no_judges,
            'no_administrators': no_administrators,
            'no_courts': no_courts
            }

    return render_template('entities.html', data=data)


@application.route('/process/', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        logger.info('refreshing insolvency start date histogram')
        refresh_insolvency_start_date_count_figure()
    return render_template('process.html')


if __name__ == "__main__":
    application.debug = True
    application.run()
