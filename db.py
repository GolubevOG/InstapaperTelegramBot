from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///user_information.sqlite')

db_session = scoped_session(sessionmaker(bind = engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users_settings_db'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique = True)
    user_nikname = Column(String(50))
    user_first_name = Column(String(50))
    user_last_name = Column(String(50))
    email = Column(String(120))
    passwd = Column(String(120))
    #login_activation_flag = Column(Boolean, default=False)
    #date_of_activation = Column(String(50))


    def __init__(self, user_id = None, user_nikname = None, 
                    user_first_name=None, user_last_name=None, 
                    passwd = None, email=None):
        self.user_id = user_id
        self.user_nikname = user_nikname
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.email = email
        self.passwd = passwd

    
    def add_login_passwd(self, passwd = None, email=None):
        self.email = email
        self.passwd = passwd
        db_session.add(self)
        db_session.commit()


    def __repr__(self):
        return '<User {} {} {}>'.format(self.user_id, self.user_first_name, self.user_last_name)

if __name__ == '__main__':
    Base.metadata.create_all(bind = engine)
