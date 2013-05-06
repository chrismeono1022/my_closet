import sys
import csv 

from sqlalchemy import engine_from_config

from my_closet import app
from my_closet.models import DBSession
from my_closet.models import Base
from my_closet.models import User
from my_closet.models import Item
from my_closet.models import Outfit

def generate_default_data():
    # load_users()
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
            print "this is %s" % c
            DBSession.add(c)
            print "added to session"
        # DBSession.flush()
        # print "added users"
        DBSession.commit()
        print "added to users"


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
            print "this is %s" % c
            DBSession.add(c)
            print "added to session"
        DBSession.flush()
        print "added items"
        # DBSession.commit()
        # print "added items"

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
        print "we are using settings.py"

    app.config.from_pyfile(path)
    print "we configured path"

    engine = engine_from_config(app.config['SQLALCHEMY'], prefix='')
    print "engine configured successfully"
    DBSession.configure(bind=engine)
    print "bound to engine"
    # Base.metadata.drop_all(engine)
    # print "dropping tables"
    Base.metadata.create_all(engine)
    print "we have deleted and made all tables again"

    generate_default_data()
    print "we are calling function to populate data"

if __name__ == '__main__':
    print "we are in seed.py"
    main()

