from flask_login import login_user
from sqlalchemy import Select
from models.user import User
from routes import db
import bcrypt


class UserService():
    def do_login(self, username, password) -> bool:
        query = Select(User).where(User.username == username)
        user = db.session.scalar(query)
        if user and user.check_password_correction(password):
            login_user(user) #找session，并放入用户信息
            return True
        return False


    def do_signup(self, username, password):
        existing = User.query.filter_by(username=username).first()
        if existing:
            return None, "username existing, try another one"
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user, None
        except Exception as e:
            db.session.rollback()
            return None, f"数据库错误：{e}"
