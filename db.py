import sqlite3

#conn = sqlite3.connect('user_information.sqlite')
#db_session = conn.cursor()
    

def is_user_login(userid):
    conn = sqlite3.connect('user_information.sqlite')
    db_session = conn.cursor()
    user_status = db_session.execute("SELECT * FROM users_settings_db WHERE id = ?",(userid,))
    user_status.fetchone()
    if user_status:
        return True
    else:
        return False

def add_user(userid):
    #проверять есть ли такой пользователь уже или нет
    db_session.execute("INSERT INTO users_settings_db (id) VALUES (?)",(userid))
    db_session.commit()


def get_record(userid):
    user_rec = db_session.execute("SELECT token, token_pass FROM users_settings_db WHERE id = ?",(userid,))
    user_rec.fetchone()
    return user_rec


def delete(userid):
    db_session.execute("DELETE FROM users_settings_db WHERE id = ?",(userid,))
    db_session.commit()


'''

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
        self.id = id
        self.token = token
        self.token_pass = passwd

    def merge(self):
        db_session.merge(self)
        db_session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def add_user(userid):
        #проверять есть ли такой пользователь уже или нет

        db_session.execute(
            "INSERT INTO users_settings_db (id) VALUES ({})".format(userid)
            
        )
        db_session.commit()


    def get_record(userid):
        user_rec = db_session.query(User).get(userid)
        return user_rec

    def delete(userid):
        db_session.execute(
            "DELETE FROM users_settings_db WHERE id=:userid",
            {"userid": userid}
        )
        db_session.commit()



Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    a = User(51447112, 'q', 'e')
    b = db_session.merge(a)
    db_session.commit()
    a = User()

    # filter(or_(User.name == 'ed', User.name == 'wendy'))
    print(User.get_record(51447112).token)
'''