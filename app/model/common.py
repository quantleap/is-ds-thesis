# -*- coding: utf-8 -*
from datetime import date
from operator import or_

from cir.models import Insolvent
from app.model import session


# noinspection PyUnresolvedReferences
def query_insolvents(select_entities=Insolvent, only_active=True):

    query = session.query(*select_entities)\
        .filter(Insolvent.person_legal_personality == 'rechtspersoon') \
        .filter(Insolvent.insolvency_type == 'F')

    if only_active:
        query = query.filter(Insolvent.is_removed.is_(False)) \
            .filter(or_(Insolvent.end_findability.is_(None),
                        Insolvent.end_findability > date.today()))

    return query


if __name__ == "__main__":
    pass
