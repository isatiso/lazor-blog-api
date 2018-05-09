# coding:utf-8
"""Module of Table Category Query Function."""

import time
from hashlib import md5
from uuid import uuid1 as uuid
from sqlalchemy import desc

from models.lazor_models import Category
from workers.manager import exc_handler


@exc_handler
def query_category_by_user_id(user_id, **kwargs):
    """Query Category Info."""
    sess = kwargs.get('sess')

    category_list = sess.query(Category).filter(
        Category.user_id == user_id).all()

    category_list = [
        category.to_dict(('category_id', 'category_name', 'create_time',
                          'category_type')) for category in category_list
    ]

    return dict(category_list=category_list)


@exc_handler
def insert_category(category_name, user_id, category_type, **kwargs):
    """Insert Category."""
    sess = kwargs.get('sess')

    category_id = uuid().hex

    new_category = Category(
        category_id=category_id,
        user_id=user_id,
        category_name=category_name,
        category_type=category_type,
        category_order=0,
        create_time=int(time.time()))

    sess.add(new_category)
    sess.commit()

    return dict(category_id=category_id)


@exc_handler
def update_category_name(category_id, category_name, **kwargs):
    """Update title or content of an article."""
    sess = kwargs.get('sess')

    effect_rows = sess.query(Category).filter(
        Category.category_id == category_id).update(
            dict(category_name=category_name))

    sess.commit()

    return dict(effect_rows=effect_rows)


@exc_handler
def delete_category(category_id, user_id, **kwargs):
    """Delete a category."""
    sess = kwargs.get('sess')

    effect_rows = sess.query(Category).filter(
        Category.category_id == category_id).filter(
            Category.user_id == user_id).filter(
                Category.category_type == 1).delete()

    sess.commit()

    return dict(effect_rows=effect_rows)


TASK_DICT = dict(
    query_category_by_user_id=query_category_by_user_id,
    insert_category=insert_category,
    update_category_name=update_category_name,
    delete_category=delete_category,
)
