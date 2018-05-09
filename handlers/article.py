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

        self.success(
            data=dict(
                article=result['data']['article'],
                content=article_content['content']))

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

        self.success(dict(article=result['data'], content=args.content))

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
