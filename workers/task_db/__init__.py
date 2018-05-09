# coding:utf-8
"""Query Task of Database lazor_blog."""

from workers.manager import APP as app, Tasks
from workers.task_db.lazor_account import TASK_DICT as account_dict
from workers.task_db.lazor_category import TASK_DICT as category_dict
from workers.task_db.lazor_article import TASK_DICT as article_dict

TASK_DICT = dict()
TASK_DICT.update(account_dict)
TASK_DICT.update(category_dict)
TASK_DICT.update(article_dict)

TASKS = Tasks(TASK_DICT)
