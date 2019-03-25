# -*- coding: utf-8 -*
import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create the database engine
con = "postgresql://{user}:{password}@{host}/qir".format(user=os.getenv('DB_QIR_USERNAME'),
                                                         password=os.getenv('DB_QIR_PASSWORD'),
                                                         host='www.quantleap.nl')
engine = create_engine(con)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# set logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
                    level=logging.DEBUG,
                    stream=sys.stdout)
