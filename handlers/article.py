# coding:utf-8
"""Handlers."""
import time
from tornado import web, gen

from base_handler import BaseHandler
from workers.task_db import TASKS as tasks
from lib import generate, verify
from config import CFG as O_O


class Article(BaseHandler):
    """Handler article stuff."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        """Get Article Source via Specific ID."""
        args = self.parse_form_arguments('article_id')

        result = tasks.query_article(article_id=args.article_id)
        if not result['data']:
            self.fail(4004)

        article_content = self.article_content.find_one(
            dict(article_id=args.article_id))

        result['data']['article']['content'] = article_content['content']
        self.success(result['data']['article'])

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        params = yield self.check_auth()

        args = self.parse_json_arguments('category_id')

        result = tasks.insert_article(
            user_id=params.user_id,
            title='无标题文章',
            content='',
            category_id=args.category_id)
        if not result['data']:
            self.fail(5003)

        article_id = result['data']['article_id']
        self.article_content.update_one(
            {
                'article_id': article_id
            }, {'$set': {
                'content': ''
            }}, upsert=True)

        self.success(dict(article_id=article_id))

    @web.asynchronous
    @gen.coroutine
    def put(self, *_args, **_kwargs):
        yield self.check_auth()

        args = self.parse_json_arguments(
            'article_id', title=None, content=None, category_id=None)

        if args.title or args.category_id:
            update_dict = dict(title=args.title, category_id=args.category_id)
            tasks.update_article(article_id=args.article_id, **update_dict)

        if args.content:
            self.article_content.update_one(
                {
                    'article_id': args.article_id
                }, {'$set': {
                    'content': args.content
                }},
                upsert=True)

        result = tasks.query_article(article_id=args.article_id)
        result['data']['article']['content'] = args.content

        self.success(result['data']['article'])

    @web.asynchronous
    @gen.coroutine
    def delete(self, *_args, **_kwargs):
        params = yield self.check_auth()

        args = self.parse_form_arguments('article_id')

        result = tasks.delete_article(
            article_id=args.article_id, user_id=params.user_id)
        if result['status']:
            self.fail(4004)
        if not result['data']['effect_rows']:
            self.fail(4005)

        self.article_content.delete_one({'article_id': args.article_id})

        self.success()


class ArticlePublishState(BaseHandler):
    """Generate a id for article."""

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        yield self.check_auth()

        args = self.parse_json_arguments('article_id', 'publish_status')

        tasks.update_article_publish_state(
            article_id=args.article_id,
            publish_status=args.publish_status,
        )

        self.success()


class ArticleList(BaseHandler):
    """Query Multi articles."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):

        args = self.parse_form_arguments('category_id')

        result = tasks.query_article_info_list(category_id=args.category_id)

        article_list = result['data']['article_list']

        order_list = self.article_order.find_one({
            'category_id':
            args.category_id
        })

        if order_list:
            order_list = order_list.get('article_order')

        self.success(
            data=dict(article_list=article_list, order_list=order_list))


class ArticleLatest(BaseHandler):
    """Query Multi articles."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):

        result = tasks.query_article_latest()

        article_list = result['data']['article_list']

        self.success(data=dict(article_list=article_list))


class ArticleRelative(BaseHandler):
    """Query Multi articles."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        args = self.parse_form_arguments('article_id')

        result = tasks.query_article_relative(article_id=args.article_id)

        article = result['data']['article']
        category = result['data']['category']
        user = result['data']['user']

        self.success(dict(article=article, category=category, user=user))


class ArticleOrder(BaseHandler):
    """Handler category order stuff."""

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        """Update Article Order of a Category."""
        yield self.check_auth()

        args = self.parse_json_arguments('category_id', 'order_list')

        self.article_order.update(
            {
                'category_id': args.category_id
            }, {'$set': {
                'article_order': args.order_list
            }},
            upsert=True)

        self.success()
