from idlelib.run import flush_stdout
from xxlimited_35 import error

from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user

from forms.article_form import ArticleForm
from models.article import Article
from routes import app
from services.article_service import ArticleService


@app.route('/createarticle.html', methods=['GET', 'POST'])
@login_required
def create_article_page():
    form = ArticleForm()
    if form.validate_on_submit():
        # print('表单验证成功')
        new_article = Article()
        new_article.title = form.title.data
        new_article.author = current_user.username
        new_article.content = form.content.data

        try:
            article, error_msg = ArticleService().create_article(new_article)
            if error_msg:
                flash(f'发布文章失败：{error_msg}', category='danger')
            else:
                flash('Article created successfully!', 'success')
                return redirect(url_for('home_page'))
        except Exception as error:
            flash(f'Create Article Failed:{error}', 'danger')

    return render_template('editarticle.html', form=form, is_edit=False)


@app.route('/editarticle/<article_id>.html', methods=['GET', 'POST'])
@login_required
def edit_article_page(article_id):
    form = ArticleForm()
    if request.method == 'GET':
        try:
            article = ArticleService().get_article(article_id)
            if not article:
                flash(f'Article not found', category='danger')
                return redirect(url_for('home_page'))
            else:
                form.title.data = article.title
                form.content.data = article.content
        except Exception as error:
            flash(f'Edit Article Failed:{error}', 'danger')
            return redirect(url_for('home_page'))

    if form.validate_on_submit():
        try:
            updated_article = Article()
            updated_article.id = int(article_id)
            updated_article.title = form.title.data
            updated_article.author = current_user.username
            updated_article.content = form.content.data

            article, error_msg = ArticleService().update_article(updated_article)
            if error_msg:
                flash(f'Edit Article Failed:{error_msg}', 'danger')
            else:
                flash('Article updated successfully!', 'success')
                return redirect(url_for('article_page', article_id=article_id))
        except Exception as error:
            flash(f'Update Article Failed:{error}', 'danger')
    return render_template('editarticle.html', form=form, article=article, is_edit=True)



@app.route('/delete_article', methods=['POST'])
@login_required
def delete_article():
    article_id = request.form.get('article_id')
    result, msg = ArticleService().delete_article(article_id)
    if result:
        flash('Article deleted successfully', 'success')
    else:
        flash(msg or 'Failed to delete article', 'danger')
    return redirect(url_for('home_page'))



@app.route('/images.html', methods=['GET','POST'])
@login_required
def get_images():
    pass

def upload_images():
    pass