from flask import render_template, request, redirect, make_response

from blog.globals import COOKIE_NAME
from blog.utils.posts import get_posts, check_favourite, get_favourites, search_posts_by_text, search_posts_by_tag
from blog.utils.search import find_user_by_cookie, find_post_by_link
from blog.utils.users import get_user
from blog_app import app


@app.route('/sign in/')
def web_web_sign_in():
    cookie_id = request.cookies.get(COOKIE_NAME)

    if cookie_id:
        user = find_user_by_cookie(cookie_id)
        if user:
            return redirect('/account/', code=302)
        else:
            return redirect('/logout/', code=302)
    else:
        return render_template('user/select.html')


@app.route('/login/')
def web_login():
    return render_template('user/login.html')


@app.route('/register/')
def web_register():
    return render_template('user/register.html')


@app.route('/logout/')
def web_logout():
    resp = make_response(redirect('/', code=302))
    resp.set_cookie(COOKIE_NAME, 'Bye!', expires=0)

    return resp


@app.route('/account/')
def web_account():
    user = get_user()

    if user:
        return render_template('user/account.html', user=user)
    else:
        return render_template('status/error.html', code='logged_out')


@app.route('/settings/')
def web_settings():
    user = get_user()

    if user:
        return render_template('user/settings.html')
    else:
        return render_template('status/error.html', code='logged_out')


@app.route('/recover_create/')
def web_recover_create():
    return render_template('user/recover-create.html')


@app.route('/recover/')
def web_recover():
    key = request.args.get('key')
    return render_template('user/recover.html', key=key)


@app.route('/delete/')
def web_delete():
    return render_template('user/delete.html')


@app.route('/post/<string:post_link>/')
def web_post(post_link):
    user = get_user()
    post = find_post_by_link(post_link)
    is_favourite = check_favourite(user, post)

    return render_template('posts/post.html', post=post, is_favourite=is_favourite,
                           tags=post['tags'].split(','))


@app.route('/')
@app.route('/posts/')
@app.route('/favourites/')
@app.route('/search/')
@app.route('/tag/<string:tag>')
def web_posts(tag=''):
    if 'favourites' in request.path:
        user = get_user()
        if not user:
            return render_template('status/error.html', code='logged_out')
        posts = get_favourites(user)
    elif 'search' in request.path:
        query = request.args.get('q')
        posts = search_posts_by_text(query)
    elif 'tag' in request.path:
        posts = search_posts_by_tag(tag)
    else:
        posts = get_posts()

    if not posts:
        return render_template('posts/posts.html', code='no_posts')
    current_page = request.args.get('page')

    if not current_page:
        current_page = 0
    else:
        current_page = int(current_page)
    pages_number = len(posts) // 10 + 1

    if len(posts) > 10:
        posts = posts[current_page * 10:current_page * 10 + 10]

    return render_template('posts/posts.html', posts=posts, current_page=current_page, pages_number=pages_number)


@app.route('/secret/')
def web_secret():
    return render_template('status/secret.html')


if __name__ == '__main__':
    app.run()
