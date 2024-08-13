from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, UniqueConstraint
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user_account"

    username: Mapped[str] = mapped_column(String(30), primary_key=True)
    email_address: Mapped[str]
    fullname: Mapped[Optional[str]]
    password: Mapped[str]
    bonds: Mapped[List["Bonds"]] = relationship(back_populates="user")

    def get_id(self):
        return (self.username)

    def __repr__(self) -> str:
            return f"User(username={self.username!r}," \
                   f" email_address={self.email_address!r}," \
                   f" fullname={self.fullname!r}"

class Bonds(db.Model):
    __tablename__ = "bonds"

    id: Mapped[int] = mapped_column(primary_key=True)
    cusip: Mapped[str]
    notional: Mapped[int]
    purchase_price: Mapped[float]
    user_id = mapped_column(ForeignKey("user_account.username"))
    user: Mapped[User] = relationship(back_populates="bonds")

    def __repr__(self) -> str:
            return f"Bond(id={self.id!r}, cusp={self.cusip}," \
                   f" notional={self.notional!r}," \
                   f" purchase_price={self.purchase_price!r})"


class JobBoardScraperEmails(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User: {self.email}>'
