# -*- coding: utf-8 -*

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from cir.models import TimeStamp
from model import session


application = Flask(__name__)
Bootstrap(application)


@application.route('/')
def home():
    """ displays general information and links to the individual information retrieval items. """

    last_case_update = session.query(TimeStamp.last_cir_case_extraction).one()[0]
    last_report_update = session.query(TimeStamp.last_cir_report_extraction).one()[0]
    no_insolvents = session.execute('select count(1) from active_company_bankrupt_insolvents_view;').fetchone()[0]

    data = {'last_case_update': last_case_update,
            'last_report_update': last_report_update,
            'no_insolvents': no_insolvents,
            }

    return render_template('main.html', data=data)


if __name__ == "__main__":
    application.debug = True
    application.run()
