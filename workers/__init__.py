# coding:utf-8
import sys

from config import _ENV as env
from workers.manager import APP as app, QUEUE_LIST as queue_list
from workers.manager import assemble_celery_cmd
from workers.manager import Tasks
