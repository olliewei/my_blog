import bcrypt
from sqlalchemy import String, Integer
from routes import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    fullname: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str] = mapped_column(String,nullable=True)

    def check_password_correction(self, attempted_password):
        password_hashed = self.password.encode('utf-8')
        return bcrypt.checkpw(attempted_password.encode('utf-8'), password_hashed)