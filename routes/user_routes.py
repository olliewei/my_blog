import re

from flask_login import logout_user, current_user, login_user

from forms import delete_article_form
from forms.delete_article_form import DeleteArticleForm
from forms.login_form import LoginForm
from forms.article_form import ArticleForm
from forms.signup_form import SignUpForm
from models import article
from models.article import Article
from routes import app
from flask import render_template, abort, redirect, flash, url_for, request, jsonify
from services.article_service import ArticleService
from services.user_service import UserService
import templates


@app.route('/',methods=['GET','POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def home_page():
    page = request.args.get('page', 1, type=int)
    per_page = 8
    search = request.args.get('search', '', type=str)
    if current_user.is_authenticated:
        # 已登录，显示当前用户的文章
        pagination = ArticleService().get_articles(page=page, per_page= per_page, author=current_user.username, search=search)
        articles = pagination.items
    else:
        # 未登录，可以选择显示所有文章或空列表
        pagination = ArticleService().get_articles(page=page, per_page=per_page, search=search)
    articles = pagination.items

    if request.args.get('ajax'):
        articles_data = [
            {
                'id': a.id,
                'title': a.title,
                'author': a.author,
                'content': a.content[:150] + '...',
                'create_time': a.create_time.strftime("%Y-%m-%d %H:%M")
            }
            for a in articles
        ]
        return jsonify({
            'articles': articles_data,
            'has_next': pagination.has_next,
            'next_page': pagination.next_num if pagination.has_next else None
        })
    # return render_template('index.html', articles=articles, my_title='Home Page')
    return render_template(
        'index.html',
        articles=articles,
        pagination=pagination.has_next,
        next_page = pagination.next_num if pagination.has_next else None,
        search = search
    )

@app.route('/about.html')
def about_page():
    return render_template('about.html', my_title='About Page')


@app.route('/article/<article_id>.html')
def article_page(article_id):
    article = ArticleService().get_article(article_id)
    if not article:
        abort(404)  # 文章不存在

    # 未登录用户
    if not current_user.is_authenticated:
        flash('Please log in', 'danger')
        return redirect(url_for('login_page'))

    # 权限检查
    if current_user.username != article.author:
        flash('Not authorized to view this article', 'danger')
        return redirect(url_for('home_page'))  # 或者 abort(403)

    # 只有作者可以删除文章
    delete_article_form = DeleteArticleForm()
    if delete_article_form.validate_on_submit():
        if delete_article_form.article_id.data == article.id:
            result, error_msg = ArticleService().delete_article(article.id)
            if result:
                flash('Article successfully deleted!', 'success')
                return redirect(url_for('home_page'))
            else:
                flash(f'Delete failed: {error_msg}', 'danger')

    return render_template('article.html', article=article, delete_article_form=delete_article_form,
                           my_title='Article Page')


@app.route('/login.html', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        result = UserService().do_login(form.username.data, form.password.data)
        if result:
            flash(f'You have been logged in as {form.username.data}!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password is incorrect', 'danger')
    return render_template('login.html', form=form,my_title='Login Page')


@app.route('/logout.html')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/signup.html', methods=['GET','POST'])
def signup_page():
    form = SignUpForm()
    if form.validate_on_submit():
        if len(form.password.data) < 3:
            flash('Password must be at least 3 characters long.', 'danger')
        elif not re.search(r'[A-Za-z]', form.password.data):
            flash('Password must contain at least one letter', 'danger')
        elif not re.search(r'\d', form.password.data):
            flash('Password must contain at least one digit', 'danger')
        else:
            user, error_msg = UserService().do_signup(form.username.data, form.password.data)
            if error_msg:
                flash(f'Sign up failed !', 'danger')
                return redirect(url_for('home_page'))
            else:
                login_user(user)
                flash('Sign Up successfully', 'success')
                return redirect(url_for('home_page'))
    return render_template('signup.html', form=form,my_title='SignUp Page')
