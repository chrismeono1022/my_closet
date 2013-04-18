from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String

from sqlalchemy.orm import sessionmaker, relationship, backref

ENGINE = None
Session = None


# investigate - what this is doing? 
Base = declarative_base()

# create engine connection
# engine = create_engine('postgresql://localhost:5432/my_closet', echo=True)

# user SQLAlchemy default __init__ which allows for user of keyword args e.g. first = "alby", last = "meono", etc.
class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	first = Column(String(120), nullable = False)
	last = Column(String(120), nullable = False)
	email = Column(String(120), nullable = False)
	password = Column(String(120), nullable = False)
	location = Column(Text, nullable=False)

class Item(Base):
	__tablename__ = "items" # clothing items 

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('users.id'))
	name = Column(String(200), nullable = False) # name your item 
	type = Column(String(200), nullable = False) # e.g. bottoms, tops, dress
	tag = Column(String(200), nullable = True) # e.g. bohemian, casual
	image_url = Column(Text, nullable=False)
	item_rating = Column(Integer, nullable=True)

	user = relationship("User", backref=backref("items", order_by=id))

class Outfit(Base):
	__tablename__ = "outfits"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('users.id'))
	top_id = Column(Integer, ForeignKey('items.id'))
	bottom_id = Column(Integer, ForeignKey('items.id'))
	dress_id = Column(Integer, ForeignKey('items.id'))
	shoes_id = Column(Integer, ForeignKey('items.id'))
	accessories_id = Column(Integer, ForeignKey('items.id'))
	outfit_rating = Column(Integer, nullable=True)

	user = relationship("User", backref=backref("outfits", order_by=id)) # class name, table name
	#item = relationship("Item", backref=backref("outfits", order_by=id))


def connect():
	global ENGINE 
	global Session

	ENGINE = create_engine('postgresql://localhost:5432/my_closet', echo=True)
	Session = sessionmaker(bind=ENGINE)

	return Session() 


def main():
	"""In case we need this for something"""
	pass

if __name__ == "__main__":
	print "we are in model.py"
	main()