import instapaper  # should be installed as pip install git+https://github.com/rsgalloway/instapaper
#для python3 обязательно в исходной библиотеке задокументировать строки 
#112-115 иначе он будет пытаться перевести всё в формат UTF8
import config  # временно загружаю логин-пароль для instapaper
import db
import urllib.parse


class Ipaper(object):

    def __init__(self):
        self.instapaper = None

    def login(self, userid, args):
        loggedin = 0
        try:
            if self.instapaper:
                msg = 'Already logged in!'

            elif len(args) != 2:
                msg = 'Please enter credentials as "/login username password". We don\'t save them'
            else:
                self.instapaper = instapaper.Instapaper(config.oauth_token, config.oauth_secret)
                try:
                    # logging in
                    self.instapaper.login(args[0], args[1])
                    token = dict(urllib.parse.parse_qsl(str(self.instapaper.token)))

                    # insert new
                    user = db.User(userid, token['oauth_token'], token['oauth_token_secret'])

                    # getting user data
                    self.username = self.instapaper.user().get('username')
                    # user_data['username'] = user
                    msg = 'Logged in as {}!'.format(self.username)
                    loggedin = 1
                except KeyError:
                    msg = 'Incorrect credentials!'

        except Exception as e:
            msg = 'There was an error: {}'.format(str(e))

        return (loggedin, msg)

    def login_with_token(self, user_id):
        self.instapaper = instapaper.Instapaper(config.oauth_token, config.oauth_secret)
        token, token_pass = db.User.get_record(user_id)
        self.instapaper.login_with_token(token, token_pass)

    def bookmark(self, params):
        b = instapaper.Bookmark(self.instapaper, params)
        b.save()

    

