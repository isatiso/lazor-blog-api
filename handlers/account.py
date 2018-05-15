# coding:utf-8
"""Handlers."""
import time
from tornado import web, gen

from base_handler import BaseHandler
from workers.task_db import TASKS as tasks
from lib import generate, verify
from config import CFG as O_O


class Auth(BaseHandler):
    """Handler account stuff."""

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        """Log in."""
        args = self.parse_json_arguments('name', 'password')

        user_info = tasks.query_user(username=args.name)

        if not user_info['data']:
            user_info = tasks.query_user(email=args.name)

        if not user_info['data']:
            self.fail(3011)

        user_info = user_info['data']
        if user_info['pswd'] != generate.encode_passwd(args.password):
            self.fail(3001)

        if not user_info['active_status']:
            self.fail(3002)

        user_params = dict(
            supervisor=user_info['supervisor'],
            user_name=user_info['username'],
            email=user_info['email'],
            user_id=user_info['user_id'])

        self.set_current_user(user_info['user_id'])
        self.set_parameters(user_params)

        self.success(user_params)

    @web.asynchronous
    @gen.coroutine
    def put(self, *_args, **_kwargs):
        args = self.parse_json_arguments('username', 'email', 'password')

        if not verify.verify_email(args.email):
            self.fail(3032)
        if not verify.verify_password(args.password):
            self.fail(3031)

        result = tasks.query_user_exists(
            username=args.username, email=args.email)
        if result['data']['exist']:
            self.fail(3004)

        result = tasks.insert_user(
            username=args.username,
            email=args.email,
            pswd=generate.encode_passwd(args.password))
        user_id = result['data']['user_id']

        tasks.insert_category(
            category_name='默认分类', category_type=0, user_id=user_id)

        self.success(dict(user_id=user_id))

    @web.asynchronous
    @gen.coroutine
    def delete(self, *_args, **_kwargs):
        self.set_current_user('')
        self.set_parameters(dict())
        self.success()


class User(BaseHandler):
    pass


class UserProfile(BaseHandler):
    """Handler account info stuff."""

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        params = yield self.check_auth()

        args = self.parse_json_arguments('name')

        result = tasks.query_user_exists(username=args.name)

        if result['data']['exist']:
            self.fail(3004)

        tasks.update_user_name(user_id=params.user_id, username=args.name)

        params['user_name'] = args.name
        self.set_parameters(params)

        self.success()


class UserPassword(BaseHandler):
    """Handle password of account."""

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        params = yield self.check_auth()

        args = self.parse_json_arguments('old_pass', 'new_pass')

        user_info = tasks.query_user(user_id=params.user_id)

        if not user_info['data']:
            self.fail(4004)

        old_md5 = generate.encode_passwd(args.old_pass)

        if old_md5 != user_info['data']['pswd']:
            self.fail(3001)

        new_md5 = generate.encode_passwd(args.new_pass)
        tasks.update_user_pass(user_id=params.user_id, pswd=new_md5)

        self.success()


class UserList(BaseHandler):
    """Handle normal users."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        _params = yield self.check_auth(supervisor=1)

        user_list = tasks.query_normal_user_list()

        self.success(user_list['data']['users'])
