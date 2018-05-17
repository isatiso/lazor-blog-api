# coding:utf-8
"""Module of Table Article Query Function."""
import time
from uuid import uuid1 as uuid

from sqlalchemy import desc

from models.lazor_models import Article, User, Category
from workers.manager import exc_handler


@exc_handler
def query_article(article_id, **kwargs):
    """Query Article Info."""
    sess = kwargs.get('sess')

    article, category, user = sess.query(Article, Category, User).outerjoin(
        Category, Category.category_id == Article.category_id).outerjoin(
            User, User.user_id == Article.user_id).filter(
                Article.article_id == article_id).first()

    result = dict()
    if article:
        result.update(
            article.to_dict([
                'article_id', 'title', 'update_time', 'create_time',
                'publish_status'
            ]))

    if category:
        result.update(category.to_dict(['category_id', 'category_name']))

    if user:
        result.update(user.to_dict(['user_id', 'user_name', 'email']))

    return dict(article=result)


@exc_handler
def query_article_latest(**kwargs):
    """Query Article Info."""
    sess = kwargs.get('sess')

    result = sess.query(Article, Category, User).outerjoin(
        Category, Category.category_id == Article.category_id).outerjoin(
            User, User.user_id == Article.user_id)

    result = result.order_by(desc(Article.create_time))

    result = result.limit(20)

    article_list = list()
    for article, category, user in result:
        item = dict()
        if article:
            item.update(
                article.to_dict([
                    'article_id', 'title', 'update_time', 'create_time',
                    'publish_status'
                ]))
        if category:
            item.update(category.to_dict(['category_id', 'category_name']))
        if user:
            item.update(user.to_dict(['user_id', 'username']))
        article_list.append(item)

    return dict(article_list=article_list)


@exc_handler
def query_article_info_list(**kwargs):
    """Query Article Info."""
    sess = kwargs.get('sess')

    result = sess.query(Article, Category, User).outerjoin(
        Category, Category.category_id == Article.category_id).outerjoin(
            User, User.user_id == Article.user_id)

    if kwargs.get('category_id'):
        result = result.filter(Article.category_id == kwargs['category_id'])

    if kwargs.get('publish_status'):
        result = result.filter(
            Article.publish_status == kwargs['publish_status'])

    result = result.order_by(desc(Article.create_time))

    if kwargs.get('limit'):
        result = result.limit(kwargs['limit'])
    else:
        result = result.all()

    article_list = list()
    for article, category, user in result:
        item = dict()
        if article:
            item.update(
                article.to_dict([
                    'article_id', 'title', 'update_time', 'create_time',
                    'publish_status'
                ]))
        if category:
            item.update(category.to_dict(['category_id', 'category_name']))
        if user:
            item.update(user.to_dict(['user_id', 'username']))
        article_list.append(item)

    return dict(article_list=article_list)


@exc_handler
def insert_article(title, user_id, category_id, **kwargs):
    """Insert Article."""
    sess = kwargs.get('sess')

    article_id = uuid().hex
    new_article = Article(
        article_id=article_id,
        category_id=category_id,
        user_id=user_id,
        title=title,
        content='',
        publish_status=0,
        update_time=int(time.time()),
        create_time=int(time.time()),
    )

    sess.add(new_article)
    sess.commit()

    return dict(article_id=article_id)


@exc_handler
def update_article(article_id, **kwargs):
    """Update title or content of an article."""
    sess = kwargs.get('sess')

    key_list = ['title', 'content', 'category_id']
    update_dict = dict()

    for key in key_list:
        if kwargs.get(key):
            update_dict[key] = kwargs.get(key)

    if update_dict:
        update_dict['update_time'] = int(time.time())

        effect_rows = sess.query(Article).filter(
            Article.article_id == article_id).update(update_dict)

        sess.commit()
        return dict(effect_rows=effect_rows)
    else:
        return dict()


@exc_handler
def update_article_publish_state(article_id, publish_status, **kwargs):
    """Update publish state of an article."""
    sess = kwargs.get('sess')

    effect_rows = sess.query(Article).filter(
        Article.article_id == article_id).update(
            dict(publish_status=publish_status))

    sess.commit()

    return dict(effect_rows=effect_rows)


@exc_handler
def delete_article(article_id, user_id, **kwargs):
    """Delete article."""
    sess = kwargs.get('sess')

    effect_rows = sess.query(Article).filter(
        Article.article_id == article_id).filter(
            Article.user_id == user_id).delete()

    sess.commit()

    return dict(effect_rows=effect_rows)


@exc_handler
def delete_article_by_category_id(category_id, **kwargs):
    """Delete article."""
    sess = kwargs.get('sess')

    effect_rows = sess.query(Article).filter(
        Article.category_id == category_id).delete()

    sess.commit()

    return dict(effect_rows=effect_rows)


TASK_DICT = dict(
    query_article=query_article,
    query_article_info_list=query_article_info_list,
    query_article_latest=query_article_latest,
    insert_article=insert_article,
    update_article=update_article,
    delete_article=delete_article,
    delete_article_by_category_id=delete_article_by_category_id,
)
