import sys
import csv 

from sqlalchemy import engine_from_config

from my_closet import app
from my_closet.models import DBSession
from my_closet.models import Base
from my_closet.models import User
from my_closet.models import Item
from my_closet.models import Outfit

def genereate_default_data():
    load_users()
    load_items()
    DBSession.commit()

def load_users():
    # users.txt and other seed files are in seed_data directory, must be ascii/UTF-8 compliant as decoding isn't handled here
    with open('../../seed_data/users.txt') as f:
        reader = csv.reader(f, delimiter = "|")

        # data format - ['1', 'Chris', 'Meono', 'meonocr@ucla.edu', 'pass', '90291']
        for row in reader:
            print row
            first = row[0]
            last = row[1]
            email = row[2]
            password = row[3]
            location = row[4]

            # Use kwargs to create dictionary with row item - ({'last': 'Meono', 'id': '1', 'location': '90291', 'password': 'pass', 'email': 'meonocr@ucla.edu', 'first': 'Chris'}). Note this creates a list of dictionaries, zips __init__ kwargs with row values 
            c = User(first=first, last=last, email=email, password = password, location=location)
            DBSession.add(c)
        DBSession.flush()


def load_items():
    user = DBSession.query(User).first()
    with open('../../seed_data/items.txt') as f:
        reader = csv.reader(f, delimiter = "|")

        for row in reader:
            print row
            name = row[0]
            type = row[1]
            style = row[2]
            image_url = row[3]
            color = row[4]
            item_rating = row[5]
            rain = row[6]
            heat = row[7]
            snow = row[8]
            low_temp = row[9]
            high_temp = row[10]

            c = Item(user=user, name=name, type=type, style=style, image_url=image_url, color=color, item_rating=item_rating, rain=rain, heat=heat, snow=snow, low_temp=low_temp, high_temp=high_temp)
            DBSession.add(c)
        DBSession.flush()

def load_outfits(session):
    pass    


def main(argv=sys.argv):
    if len(sys.argv) == 2:
        path = sys.argv[1]

        if not os.path.isabs(path):
            here = os.path.dirname(__file__)
            path = os.path.abspath(os.path.join(here, path))
    else:
        path = 'settings.py'

    app.config.from_pyfile(path)

    engine = engine_from_config(app.config['SQLALCHEMY'], prefix='')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    generate_default_data()

if __name__ == '__main__':
    main()

