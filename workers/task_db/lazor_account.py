# coding:utf-8
"""Module of Table Account Query Function."""

import time
from hashlib import md5
from uuid import uuid1 as uuid

from models.lazor_models import User
from workers.manager import exc_handler


@exc_handler
def query_user(**kwargs):
    """Query User Info."""
    sess = kwargs.get('sess')

    user = sess.query(User)

    if kwargs.get('user_id'):
        user = user.filter(User.user_id == kwargs['user_id'])
    elif kwargs.get('email'):
        user = user.filter(User.email == kwargs['email'])
    elif kwargs.get('username'):
        user = user.filter(User.username == kwargs['username'])

    user = user.first()

    return user and user.to_dict() or None


@exc_handler
def query_user_exists(email='', username='', **kwargs):
    """Query email if exists."""
    sess = kwargs.get('sess')

    email_exists = sess.query(User).filter(User.email == email).first()
    username_exists = sess.query(User).filter(
        User.username == username).first()

    return dict(exist=bool(email_exists or username_exists))


@exc_handler
def query_normal_user_list(**kwargs):
    """Query all users except supervisor."""
    sess = kwargs.get('sess')

    users = sess.query(User).filter(User.supervisor == 0).all()

    if users:
        users = [
            user.to_dict(['user_id', 'username', 'email', 'active_status'])
            for user in users
        ]
    else:
        users = None

    return dict(users=users)


@exc_handler
def insert_user(email, pswd, username, **kwargs):
    """Insert a user."""
    sess = kwargs.get('sess')

    user_id = uuid().hex
    new_user = User(
        user_id=user_id,
        username=username,
        email=email,
        pswd=pswd,
        active_status=0,
        create_time=int(time.time()))

    sess.add(new_user)
    sess.commit()

    return dict(user_id=user_id)


@exc_handler
def update_user_name(user_id, username, **kwargs):
    """Insert a user."""
    sess = kwargs.get('sess')

    effect_rows = sess.query(User).filter(User.user_id == user_id).update(
        dict(username=username))
    sess.commit()

    return dict(effect_rows=effect_rows)


@exc_handler
def update_user_pass(user_id, pswd, **kwargs):
    """Insert a user."""
    sess = kwargs.get('sess')

    effect_rows = sess.query(User).filter(User.user_id == user_id).update(
        dict(pswd=pswd))

    sess.commit()

    return dict(effect_rows=effect_rows)


TASK_DICT = dict(
    query_user=query_user,
    query_user_exists=query_user_exists,
    query_normal_user_list=query_normal_user_list,
    insert_user=insert_user,
    update_user_name=update_user_name,
    update_user_pass=update_user_pass,
)
