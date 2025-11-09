from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__,
            template_folder='../templates',
            static_folder='../assets',
            static_url_path='/assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/my_blog_db'
app.config['SECRET_KEY'] = 'dev-key'
db = SQLAlchemy(app)
# ✅ 创建并注册 login_manager
login_manager = LoginManager()
login_manager.init_app(app)

# ✅ 先导入 User，再定义 user_loader
from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

# ✅ 最后导入路由，防止循环引用
from routes import user_routes
from routes import admin_routes



