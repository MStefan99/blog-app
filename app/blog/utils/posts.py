from datetime import datetime
from sqlite3 import IntegrityError

from blog.globals import DATABASE


def get_posts():
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts '
                   'order by date desc')
    return cursor.fetchall()


def get_favourites(user):
    cursor = DATABASE.cursor()
    cursor.execute('select posts.* from posts join favourites '
                   'on (favourites.post_id = posts.id '
                   'and favourites.user_id = ?) '
                   'order by favourites.date_added desc', [user['id']])
    return cursor.fetchall()


def check_favourite(user, post):
    cursor = DATABASE.cursor()
    if user and post:
        cursor.execute('select * from posts join favourites '
                       'on (favourites.post_id = posts.id '
                       'and favourites.user_id = ? '
                       'and post_id = ?)',
                       [user['id'], post['id']])
        return bool(cursor.fetchall())


def save_post(user, post):
    cursor = DATABASE.cursor()
    time = datetime.now()
    try:
        cursor.execute('insert into favourites(user_id, post_id, date_added) '
                       'values (?, ?, ?)',
                       [user['id'], post['id'], time.strftime('%Y-%m-%d %H:%M:%S')])
        DATABASE.commit()
    except IntegrityError:
        return False
    return True


def remove_post(user, post):
    cursor = DATABASE.cursor()
    cursor.execute('delete from favourites '
                   'where user_id = ? '
                   'and post_id = ?',
                   [user['id'], post['id']])
    DATABASE.commit()
    return True


def search_posts_by_text(query):
    query = '%' + query + '%'
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts '
                   'where content like ? '
                   'or title like ? '
                   'or tagline like ? '
                   'order by date desc',
                   [query, query, query])
    return cursor.fetchall()


def search_posts_by_tag(tag):
    tag = '%' + tag + '%'
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts '
                   'where tags like ? '
                   'order by date desc',
                   [tag])
    return cursor.fetchall()
