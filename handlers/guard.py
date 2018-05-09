# coding:utf-8
"""Handlers."""
import time
from tornado import web, gen

from base_handler import BaseHandler
from workers.task_db import TASKS as tasks
from lib import generate, verify
from config import CFG as O_O


class AuthGuard(BaseHandler):
    """Handler account stuff."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        params = yield self.check_auth()

        self.success(params)


class ArticleOwnerGuard(BaseHandler):
    """Handler if user own the article."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        params = yield self.check_auth()

        args = self.parse_form_arguments('article_id')

        result = tasks.query_article(article_id=args.article_id)

        if not result['data']:
            self.fail(4004)
        if params.user_id != result['data']['user_id']:
            self.fail(4005)

        self.success()
