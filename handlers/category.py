# coding:utf-8
"""Handlers."""
import time
from tornado import web, gen

from base_handler import BaseHandler
from workers.task_db import TASKS as tasks
from lib import generate, verify
from config import CFG as O_O


class Category(BaseHandler):
    """Handler category stuff."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        """Get Category List of Current User."""

        args = self.parse_form_arguments('user_id')

        result = tasks.query_category_by_user_id(user_id=args.user_id)
        category_list = result['data']['category_list']

        order_list = self.category_order.find_one({'user_id': args.user_id})

        if order_list:
            order_list = order_list.get('category_order')

        self.success(
            data=dict(category_list=category_list, order_list=order_list))

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        """Add a Category to Current User."""
        params = yield self.check_auth()

        args = self.parse_json_arguments('category_name')

        result = tasks.insert_category(
            category_name=args.category_name,
            category_type=1,
            user_id=params.user_id)
        category_id = result['data']['category_id']

        self.success(dict(category_id=category_id))

    @web.asynchronous
    @gen.coroutine
    def put(self, *_args, **_kwargs):
        """Update Category Name."""
        yield self.check_auth()

        args = self.parse_json_arguments('category_id', 'category_name')

        tasks.update_category_name(
            category_id=args.category_id, category_name=args.category_name)

        self.success()

    @web.asynchronous
    @gen.coroutine
    def delete(self, *_args, **_kwargs):
        params = yield self.check_auth()

        args = self.parse_form_arguments('category_id')

        result = tasks.delete_category(
            category_id=args.category_id, user_id=params.user_id)

        if not result['data'] or not result['data']['effect_rows']:
            self.fail(4004)

        tasks.delete_article_by_category_id(category_id=args.category_id)

        self.success()


class CategoryOrder(BaseHandler):
    """Handler category order stuff."""

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        params = yield self.check_auth()

        args = self.parse_json_arguments('order_list')
        if not isinstance(args.order_list, list):
            self.fail(4005)

        self.category_order.update(
            {
                'user_id': params.user_id
            }, {'$set': {
                'category_order': args.order_list
            }},
            upsert=True)

        self.success()
