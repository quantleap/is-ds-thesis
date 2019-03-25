# -*- coding: utf-8 -*
import re
import psycopg2

# create session
from sqlalchemy.engine.url import URL


con = str(URL(drivername='postgresql',
              username='dbusr',  # os.environ['DB_QIR_USERNAME'],
              password='dbpw',  # os.environ['DB_QIR_PASSWORD'],
              host='www.quantleap.nl',
              database='qir'))
conn = psycopg2.connect(con)
cur = conn.cursor()

class ProgressReportSectionExtractor:
    """ Class to extract sections from a progress report.
        Supplied patterns are applied in given order, specify from strict to broad.
        Only the first match is returned. """
    def __init__(self, report_content=None):
        self.report_content = report_content
        self.sections = {'0.0': {'id': 'introduction',
                                 'heading': 'Introduction',
                                 'patterns': [r'(.*?)(?=\n1\.1)']},
                         '1.1': {'id': 'directie_en_organisatie',
                                 'heading': 'Directie en organisatie',
                                 'patterns': [r'(?<=\n1\.1)(.*?)(?=\n1\.2)',
                                              r'(?:inventarisatie.*\n1)(.*?)(?:\n2)']},  # heading level 2 missing
                         '1.7': {'id': 'oorzaak_faillissement',
                                 'heading': 'Oorzaak faillissement',
                                 'patterns': [r'(?<=\n1\.7)(.*?)(?=\n2)']},
                         '2.1': {'id': 'aantal_ten_tijde_van_faillissement',
                                 'heading': 'Aantal ten tijde van faillissement',
                                 'patterns': [r'(?<=\n2\.1)(.*?)(?=\n2\.2)']},
                         '7.1': {'id': 'boekhoudplicht',
                                 'heading': 'Boekhoudplicht',
                                 'patterns': [r'(?<=\n7\.1)(.*?)(?=\n7\.2)']},
                         '7.5': {'id': 'onbehoorlijk_bestuur',
                                 'heading': 'Onbehoorlijk bestuur',
                                 'patterns': [r'(?<=\n7\.5)(.*?)(?=\n7\.6)']},
                         '7.6': {'id': 'paulianeus_handelen',
                                 'heading': 'Paulianeus handelen',
                                 'patterns': [r'(?<=\n7\.6)(.*?)(?=\n7\.7)',
                                              r'(?<=\n7\.6)(.*?)(?=\n8)',  # next sub heading (7.7) often omitted
                                              r'(?:rechtmatigheid.*?)(paulianeus.*?)(?:\n8)',  # own sub heading omitted
                                              r'(?:rechtmatigheid.*?)(paulianeus.*?)(?:crediteuren)',  # heading info not reliable
                                              r'(paulianeus.*?\n{2,})']},
                         '8.1': {'id': 'boedelvorderingen',
                                 'heading': 'Boedelvorderingen',
                                 'patterns': [r'(?<=\n8\.1)(.*?)(?=\n8\.2)']},
                         '8.2': {'id': 'pref_vord_van_de_fiscus',
                                 'heading': 'Pref. vord. van de fiscus',
                                 'patterns': [r'(?<=\n8\.2)(.*?)(?=\n8\.3)']},
                         '8.3': {'id': 'pred_vord_van_het_uwv',
                                 'heading': 'Pref. vord. van het UWV',
                                 'patterns': [r'(?<=\n8\.3)(.*?)(?=\n8\.4)']},
                         '8.4': {'id': 'andere_pred_crediteuren',
                                 'heading': 'Andere pref. crediteuren',
                                 'patterns': [r'(?<=\n8\.4)(.*?)(?=\n8\.5)']},
                         '8.5': {'id': 'aantal_concurrente_crediteuren',
                                 'heading': 'Aantal concurrente crediteuren',
                                 'patterns': [r'(?<=\n8\.5)(.*?)(?=\n8\.6)']},
                         '8.6': {'id': 'bedrag_concurrente_crediteuren',
                                 'heading': 'Bedrag concurrente crediteuren',
                                 'patterns': [r'(?<=\n8\.6)(.*?)(?=\n8\.7)']},
                         }

    def extract_section(self, section):
        """ Return given section (by heading number) from the reports. """
        if section not in self.sections.keys():
            raise NotImplementedError

        section_content = None
        for pattern in self.sections[section]['patterns']:
            match = re.search(pattern, self.report_content, re.DOTALL | re.IGNORECASE)
            if match:
                section_content = match.group(1)
                break
        return section_content

    def section_id(self, section):
        return self.sections[section]['id']

    def section_heading(self, section):
        return self.sections[section]['heading']


# helper function
def extract_section(content, section):
    extractor = ProgressReportSectionExtractor(report_content=content)
    return extractor.extract_section(section)


def get_content(report_id):
    cur.execute("select content from reports where identification = '{}';".format(report_id))
    result = cur.fetchone()
    return result[0]


def test():
    content = get_content('05_gel_12_600_F_V_04')
    print(extract_section(content, '7.6'))


if __name__ == '__main__':
    # put noting here as this is also run by the jupyter notebook %run command
    test()
    pass
