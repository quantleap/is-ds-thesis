# -*- coding: utf-8 -*
from datetime import date

from app.model import session


def print_cir_entity_size_and_delta():
    calculation_date = date.today()

    no_active_bankrupt_insolvents = session.execute('select count(*) from active_company_bankrupt_insolvents_view')\
        .scalar()

    no_active_reports = session.execute("""select count(*) from active_company_bankrupt_insolvents_view i 
                                           join reports r on r.insolvent_id = i.id""").scalar()

    _of_which_progress = session.execute("""select count(*) from active_company_bankrupt_insolvents_view i 
                                           join reports r on r.insolvent_id = i.id
                                           where is_attachment is false""").scalar()

    _of_which_financial = session.execute("""select count(*) from active_company_bankrupt_insolvents_view i 
                                           join reports r on r.insolvent_id = i.id
                                           where is_attachment is true""").scalar()

    no_active_publications = session.execute('select count(*) from active_company_bankrupt_insolvents_view i '
                                             'join publications p on p.insolvent_id = i.id').scalar()

    no_distinct_administrators = session.execute("""select count(distinct(ar.person_family_name, 
                                                                         ar.person_middle_part,
                                                                         ar.person_initials,
                                                                         ar.person_title)) 
                                                     from company_bankrupt_insolvents_view i
                                                     join administrators_receivers ar on ar.insolvent_id = i.id
                                                   where ar.type = 'C'                                                          
                                                """).scalar()

    no_distinct_active_judges = session.execute("""select count(distinct(supervisory_judge)) 
                                                     from active_company_bankrupt_insolvents_view i
                                                """).scalar()

    # delta
    no_insolvents_per_month = session.execute("""
        with insolvents_year as ( 
          select id from insolvents 
            where person_legal_personality = 'rechtspersoon' and insolvency_type = 'F' 
              and start_date_insolvency between '01-06-2017' and '01-06-2018')
          select count(*) / 12 from insolvents_year ;                     
        """).scalar()

    no_insolvents_last_month = session.execute("""
        with insolvents_year as ( 
          select id from insolvents 
            where person_legal_personality = 'rechtspersoon' and insolvency_type = 'F' 
              and current_date - start_date_insolvency < 31)
          select count(*) / 12 from insolvents_year ;                     
        """).scalar()

    no_reports_per_month = session.execute("""
        with insolvents_year as ( 
          select id from insolvents 
            where person_legal_personality = 'rechtspersoon' and insolvency_type = 'F')
          select count(*) / 12 
              from insolvents_year as i join reports r on r.insolvent_id = i.id
              where publication_date::date between '01-06-2017' and '01-06-2018';                     
        """).scalar()

    no_reports_last_month = session.execute("""
          select count(*) from reports              
              where current_date - publication_date::date < 31                     
        """).scalar()

    no_publications_per_month = session.execute("""
        with insolvents_year as ( 
          select id from insolvents 
            where person_legal_personality = 'rechtspersoon' and insolvency_type = 'F')
          select count(*) / 12 
            from insolvents_year as i join qir.public.publications p on p.insolvent_id = i.id
                where p.date between '01-06-2017' and '01-06-2018';                     
        """).scalar()

    no_publications_last_month = session.execute("""
        with insolvents_year as ( 
          select id from insolvents 
            where person_legal_personality = 'rechtspersoon' and insolvency_type = 'F')
          select count(*) / 12 
            from insolvents_year as i join qir.public.publications p on p.insolvent_id = i.id
                where current_date - p.date < 31;                     
        """).scalar()

    print('calculation date: %s' % calculation_date)

    print('aantal actieve insolventies: %d' % no_active_bankrupt_insolvents)
    print('aantal insolventen per maand: %d' % no_insolvents_per_month)
    print('aantal insolventen laatste maand: %d' % no_insolvents_last_month)

    print('aantal actieve rapporten: %d' % no_active_reports)
    print('...waarvan voortgangs: %d' % _of_which_progress)
    print('...waarvan financiele bijlage: %d' % _of_which_financial)
    print('aantal publicaties per maand: %d' % no_publications_per_month)

    print('aantal actieve publicaties: %d' % no_active_publications)
    print('aantal publicaties per maand: %d' % no_publications_per_month)
    print('aantal publicaties laatste maand: %d' % no_publications_last_month)

    print('aantal verschillende curator namen: %d' % no_distinct_administrators)
    print('aantal verschillende rechter namen: %d' % no_distinct_active_judges)


if __name__ == "__main__":
    print_cir_entity_size_and_delta()
    pass
