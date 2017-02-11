import instapaper  # should be installed as pip install git+https://github.com/rsgalloway/instapaper
import config  # временно загружаю логин-пароль для instapaper
import db
import urllib.parse


class Ipaper(object):

    def __init__(self):
        self.instapaper = None

    def login(self, userid, args):
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
                    user.commit()

                    # getting user data
                    self.username = self.instapaper.user().get('username')
                    # user_data['username'] = user
                    msg = 'Logged in as %s!' % self.username
                except KeyError:
                    msg = 'Incorrect credentials!'

        except Exception as e:
            msg = 'There was an error: %s' % str(e)

        return msg

    def login_with_token(self, userid):
        self.instapaper = instapaper.Instapaper(config.oauth_token, config.oauth_secret)
        user_rec = db.User.get_record(userid)
        self.instapaper.login_with_token(user_rec.token, user_rec.token_pass)

    def bookmark(self, params):
        b = instapaper.Bookmark(self.instapaper, params)
        b.save()
