from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, Boolean

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref


DBSession = scoped_session(sessionmaker())


Base = declarative_base()
Base.query = DBSession.query_property()


# using SQLAlchemy default __init__ which allows for use of kwargs e.g. first = "alby", last = "meono", etc.
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
    style = Column(String(200), nullable = True) # e.g. bohemian, casual, beach wear
    image_url = Column(Text, nullable = False)
    color = Column(String(200), nullable = True)
    item_rating = Column(Integer, nullable = True)
    # info about exceptional weather conditions to collect
    rain = Column(Boolean, nullable=True)
    heat = Column(Boolean, nullable=True)
    snow = Column(Boolean, nullable=True)
    low_temp = Column(Integer, nullable = True)
    high_temp = Column(Integer, nullable = True)
    
    user = relationship("User", backref=backref("items", order_by=id))


class Outfit(Base):
    __tablename__ = "outfits" # previously suggested outfits
    
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(200), nullable = True)
    top_id = Column(Integer, ForeignKey('items.id'), nullable=True)
    bottom_id = Column(Integer, ForeignKey('items.id'), nullable=True)
    dress_id = Column(Integer, ForeignKey('items.id'), nullable=True)
    outerwear_id = Column(Integer, ForeignKey('items.id'), nullable=True)
    shoes_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    jewelry_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    accessories_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    
    # reference class name then relationship table name
    user = relationship("User", backref=backref("outfits", order_by=id)) 
    
if __name__ == "__main__":
    print "we are in model.py"
    main()
