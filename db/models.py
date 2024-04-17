from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

 # CLIENT
class DbClient(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    cat_cli = relationship('DbCatCli', back_populates='client')
    account = relationship('DbAccount', back_populates='client', cascade='all, delete')


# ACCOUNT
class DbAccount(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'))

    client = relationship('DbClient', back_populates='account')
    movement = relationship('DbMovement', back_populates='account')

# CATEGORY
class DbCategory(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    cat_cli = relationship('DbCatCli', back_populates='category')


# CATEGORY CLIENT
class DbCatCli(Base):
    __tablename__ = 'category_client'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship('DbCategory', back_populates='cat_cli')
    client = relationship('DbClient', back_populates='cat_cli')

# MOVEMENT
class DbMovement(Base):
    __tablename__ = 'movement'
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    transaction_type = Column(String)
    amount = Column(Float)
    date = Column(Date)

    account = relationship('DbAccount', back_populates='movement')