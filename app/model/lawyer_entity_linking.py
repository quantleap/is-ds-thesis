# -*- coding: utf-8 -*
import pandas as pd
from app.model import session, con


def entity_linking():
    no_distinct_active_administrators_active_cases = session.execute("""
        select count(distinct(ar.person_family_name, 
            ar.person_middle_part,
            ar.person_initials,
            ar.person_title)) 
        from active_company_bankrupt_insolvents_view i
        join administrators_receivers ar on ar.insolvent_id = i.id
        where ar.type = 'C'
            and ar.date_end is null;""").scalar()
    print('active administrators on active cases, no. of distinct names in CIR: %d' %
          no_distinct_active_administrators_active_cases)

    no_distinct_administrators = session.execute("""
        select count(distinct(ar.person_family_name, 
            ar.person_middle_part,
            ar.person_initials,
            ar.person_title)) 
        from company_bankrupt_insolvents_view i
        join administrators_receivers ar on ar.insolvent_id = i.id
        where ar.type = 'C';""").scalar()
    print('all administrators, no. of distinct names in CIR: %d' % no_distinct_administrators)

    no_mapped = session.execute("""select count(*) from administrator_associations aa; """).scalar()
    print('no. of mapped administrators: %d' % (no_mapped - 1))  # minus onbekend

    no_mapped_to_nova = session.execute("""select count(*) from administrator_associations aa 
                                           join nova_lawyers n on aa.nova_lawyer_id = n.id
                                           where source = 'nova';""").scalar()
    print('no. of administrators mapped using NOvA: %d' % no_mapped_to_nova)

    no_mapped_to_advocatenzoeken = session.execute("""select count(*) from administrator_associations aa 
                                           join nova_lawyers n on aa.nova_lawyer_id = n.id
                                           where source = 'advocatenzoeken';""").scalar()
    print('no. of administrators mapped using advocatenzoeken: %d' % no_mapped_to_advocatenzoeken)

    no_mapped_to_unknown = session.execute("""select count(*) from administrator_associations aa 
                                           join nova_lawyers n on aa.nova_lawyer_id = n.id
                                           where full_name = 'ONBEKEND';""").scalar()
    print('no. of administrators mapped to UNKNOWN: %d' % no_mapped_to_unknown)

    active_administrators_by_distinct_names_not_mapped = session.execute("""
        select count(distinct(ar.person_title, ar.person_initials, ar.person_middle_part, ar.person_family_name))
        from active_company_bankrupt_insolvents_view i
          join administrators_receivers ar on ar.insolvent_id = i.id
        where ar.type = 'C' and ar.date_end is null
          and ar.nova_lawyer_id is null;
    """).scalar()

    print('no. of (distinct names of) active administrators on active cases unmapped: %d' %
          active_administrators_by_distinct_names_not_mapped)

    active_administrators_by_distinct_names_mapped_unknown = session.execute("""
        select count(distinct(ar.person_title, ar.person_initials, ar.person_middle_part, ar.person_family_name))
        from active_company_bankrupt_insolvents_view i
          join administrators_receivers ar on ar.insolvent_id = i.id
        where ar.type = 'C' and ar.date_end is null
          and ar.nova_lawyer_id = 421;
    """).scalar()

    print('no. of (distinct names of) active administrators on active cases mapped to UNKNOWN: %d' %
          active_administrators_by_distinct_names_mapped_unknown)


def review_associations():
    df = pd.read_sql("""select source,count(*) from administrator_associations aa
                        join nova_lawyers n on aa.nova_lawyer_id = n.id
                        group by 1
                        order by count(*) desc;""", con)
    print(df)

    df = pd.read_sql("""select aa.id, source, cir_initials, cir_full_family_name, bar_code, full_name, 
                        has_same_normalized_name, is_verified from administrator_associations aa 
                        join nova_lawyers n on aa.nova_lawyer_id = n.id
                        order by source, cir_full_family_name, cir_initials;""", con)
    df.to_excel("administrator_associations.xlsx")


if __name__ == "__main__":
    review_associations()
    pass
