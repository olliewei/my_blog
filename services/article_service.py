from re import search

from sqlalchemy import Select, func, select

from models.article import Article
from routes import db



class ArticleService:
    def get_article(self, id):
        return db.session.get(Article, id)

    def get_articles(self, page=1, per_page=8, author: str = None, search: str = None):
        query = select(Article)
        if author:
            query = query.where(Article.author == author)
        if search:
            query = query.where(Article.title.ilike(f"%{search}%"))
        query = query.order_by(Article.create_time.desc())
        # 返回分页对象
        return db.paginate(query, page=page, per_page=per_page, error_out=False)



    #往数据库添加文章
    def create_article(self,article:Article):
        #to-do添加通标题文章是否存在的检测，如有则抛出异常
        query = Select(Article).where(Article.title == article.title)
        existing_article = db.session.scalars(query).first()
        if existing_article:
            return article,'Article title already exists'
        db.session.add(article)#添加
        db.session.commit()#提交

        return article, None

    def update_article(self,article:Article):
        existing_article = db.session.get(Article, article.id)
        if not existing_article:
            return article, 'Article not found'

        query = Select(Article).where(Article.title == article.title, Article.id != article.id)
        same_title_article = db.session.scalars(query).all()
        if same_title_article:
            return article, 'Article title already exists'
        existing_article.title = article.title
        existing_article.content = article.content
        existing_article.updated_at = func.now()

        db.session.commit()#提交

        return article, None

    def delete_article(self, article_id):
        article = db.session.get(Article, article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
            return True, None
        else:
            return False, 'Article not found'