from instapaper import Instapaper as ipaper
from instapaper import Bookmark

INSTAPAPER_KEY = ''
INSTAPAPER_SECRET = ''
email_adress = ''
password = ''
i = ipaper(INSTAPAPER_KEY, INSTAPAPER_SECRET)
i.login(email_adress, password)

b = Bookmark(i,{'url':'https://habrahabr.ru/post/318906/'})
b.save()

b = Bookmark(i,{'text':'просто текст для проверки как это работает'})
b.save()

marks = i.bookmarks()
print (len(marks))
for i in marks:
    print (i)
