# coding:utf-8
"""Lazor Database Module."""

import enum

from sqlalchemy import (CHAR, BigInteger, Column, Enum, Integer, SmallInteger,
                        Text, String)
from models.base import BASE


class User(BASE):
    """User Model."""
    __tablename__ = 'user'

    user_id = Column(CHAR(36), primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    pswd = Column(CHAR(32), nullable=False)
    active_status = Column(SmallInteger, nullable=True, default=0)
    supervisor = Column(SmallInteger, nullable=True, default=0)
    create_time = Column(Integer, nullable=False, index=True)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class Article(BASE):
    """Article Model."""
    __tablename__ = 'article'

    article_id = Column(CHAR(36), primary_key=True)
    category_id = Column(CHAR(36), default='default', index=True)
    user_id = Column(CHAR(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    publish_status = Column(SmallInteger, nullable=False)
    update_time = Column(Integer, nullable=False, index=True)
    create_time = Column(Integer, nullable=False, index=True)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class Category(BASE):
    """Category Model."""
    __tablename__ = 'category'

    category_id = Column(CHAR(36), primary_key=True)
    user_id = Column(CHAR(36), nullable=False, index=True)
    category_name = Column(String(255), nullable=False)
    category_type = Column(SmallInteger, nullable=False)
    category_order = Column(SmallInteger, nullable=False)
    create_time = Column(Integer, nullable=False, index=True)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )


class Image(BASE):
    """Category Model."""
    __tablename__ = 'image'

    image_id = Column(CHAR(36), primary_key=True)
    user_id = Column(CHAR(36), nullable=False, index=True)
    md5_code = Column(CHAR(32), nullable=False, index=True)
    sha1_code = Column(CHAR(40), nullable=False)
    create_time = Column(Integer, nullable=False, index=True)

    __table_args__ = ({'mysql_engine': 'InnoDB'}, )
