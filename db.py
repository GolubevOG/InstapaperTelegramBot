from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///user_information.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users_settings_db'
    # telegram ID
    id = Column(Integer, primary_key=True)
    # email = instapaer username
    # email = Column(String(120))
    # instapaper token
    token = Column(String(50))
    # instapaper token password
    token_pass = Column(String(50))
    # status = Column(Integer)
    # date_of_activation = Column(String(50))

    def __init__(self, id=None, token=None, passwd=None):
        '''self.email = email
        self.passwd = passwd'''
        self.id = id
        self.token = token
        self.token_pass = passwd

    def commit(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.id)


Base.metadata.create_all(bind=engine)
