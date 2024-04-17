from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class DbClient(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    cat_cli = relationship('DbCatCli', back_populates='client')
    account = relationship('DbAccount', back_populates='client', cascade='all, delete')

class DbAccount(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'))

    client = relationship('DbClient', back_populates='account')

class DbCategory(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    cat_cli = relationship('DbCatCli', back_populates='category')

class DbCatCli(Base):
    __tablename__ = 'category_client'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship('DbCategory', back_populates='cat_cli')
    client = relationship('DbClient', back_populates='cat_cli')