import sqlite3

#conn = sqlite3.connect('user_information.sqlite')
#db_session = conn.cursor()
    
class User():
    #надо бы поменять на add_user
    def __init__(self, id=None, token=None, passwd=None):
        self.id = id
        self.token = token
        self.token_pass = passwd
        conn = sqlite3.connect('user_information.sqlite')
        db_session = conn.cursor()
        db_session.execute("INSERT INTO users_settings_db VALUES (?,?,?)",(self.id,self.token,self.token_pass))
        conn.commit()
        conn.close()

    #пока неактивная 
    #добавляет пользователей
    def add_user(user_id,token,token_pass):
        conn = sqlite3.connect('user_information.sqlite')
        db_session = conn.cursor()
        db_session.execute("INSERT INTO users_settings_db VALUES (?,?,?)",(user_id,token,token_pass))
        conn.commit()
        conn.close()

    #проверка залогинин ли пользователь или нет
    def is_user_login(user_id):
        conn = sqlite3.connect('user_information.sqlite')
        db_session = conn.cursor()
        user_status = db_session.execute("SELECT * FROM users_settings_db WHERE id = ?",(user_id,))
        user_status = user_status.fetchone()
        if user_status:
            return True
        else:
            return False

    #добавляет пользователей, при нажатии команды start тестовая
    def add_user_when_start(user_id):
        conn = sqlite3.connect('user_information.sqlite')
        db_session = conn.cursor()
        db_session.execute("INSERT INTO users_settings_db VALUES (?,?,?)",(user_id,None,None))
        conn.commit()
        conn.close()


    def get_record(user_id):
        conn = sqlite3.connect('user_information.sqlite')
        db_session = conn.cursor()
        user_rec = db_session.execute("SELECT token, token_pass FROM users_settings_db WHERE id = ?",(user_id,))
        user_rec.fetchone()
        return user_rec


    def delete(user_id):
        conn = sqlite3.connect('user_information.sqlite')
        db_session = conn.cursor()
        db_session.execute("DELETE FROM users_settings_db WHERE id = ?",(user_id,))
        conn.commit()
        conn.close()
