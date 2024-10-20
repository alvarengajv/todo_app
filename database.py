from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def init_db(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.bind = engine
    Base.metadata.create_all(engine) 

    Session = sessionmaker(bind=engine)
    return Session()
