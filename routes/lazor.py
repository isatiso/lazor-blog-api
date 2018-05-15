# coding:utf-8

from handlers import account
from handlers import category
from handlers import article
from handlers import guard
from handlers import file

LAZOR_ROUTES = [
    (r'/middle/auth', account.Auth),
    (r'/middle/user/profile', account.UserProfile),
    (r'/middle/user/password', account.UserPassword),
    (r'/middle/user_list', account.UserList),
    (r'/middle/category', category.Category),
    (r'/middle/category/order', category.CategoryOrder),
    (r'/middle/article', article.Article),
    (r'/middle/article/list', article.ArticleList),
    (r'/middle/article/order', article.ArticleOrder),
    (r'/middle/guard/auth', guard.AuthGuard),
    (r'/middle/guard/owner', guard.ArticleOwnerGuard),
    (r'/middle/guard/supervisor', guard.SupervisorGuard),
    (r'/middle/file', file.File),
    (r'/middle/image', file.Image),
    (r'/middle/image/record/.*', file.ImageRecord),
]
