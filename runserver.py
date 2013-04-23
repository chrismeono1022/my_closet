from sqlalchemy import engine_from_config
from my_closet.models import DBSession
from my_closet import app
import sys
import os


if __name__ == "__main__":
     
    path = 'my_closet/settings.py'

    if len(sys.argv) == 2:
        path = sys.argv[1]

    if not os.path.isabs(path):
        here = os.path.dirname(__file__)
        path = os.path.abspath(os.path.join(here, path))
       

    app.config.from_pyfile(path)

    engine = engine_from_config(app.config['SQLALCHEMY'], prefix='')
    DBSession.configure(bind=engine)

    app.run()
