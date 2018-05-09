# coding:utf-8

from handlers import account
from handlers import category
from handlers import article
from handlers import guard

LAZOR_ROUTES = [
    (r'/middle/user', account.User),
    (r'/middle/user/profile', account.UserProfile),
    (r'/middle/user/password', account.UserPassword),
    (r'/middle/category', category.Category),
    (r'/middle/category/order', category.CategoryOrder),
    (r'/middle/article', article.Article),
    (r'/middle/article/list', article.ArticleList),
    (r'/middle/article/order', article.ArticleOrder),
    (r'/middle/guard/auth', guard.AuthGuard),
    (r'/middle/guard/owner', guard.ArticleOwnerGuard),
]
