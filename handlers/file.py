# coding:utf-8
"""Handlers."""
import time
import os
import re
from hashlib import md5, sha1
from uuid import uuid1 as uuid

from tornado import web, gen

from base_handler import BaseHandler
from workers.task_db import TASKS as tasks
from lib import generate, verify
from lib.qcos.bucket import Bucket
from config import CFG as O_O

qcos_bucket = Bucket(
    bucket=O_O.cos.bucket,
    access_id=O_O.cos.access_id,
    access_key=O_O.cos.access_key,
    region=O_O.cos.region,
    appid=O_O.cos.appid)


class File(BaseHandler):
    """Handler file stuff."""

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        params = yield self.check_auth()

        file_meta = self.request.files
        file_list = []
        for fp in file_meta['file']:
            filename, ext = os.path.splitext(fp['filename'])

            ext = ext.lower()
            image_id = uuid().hex
            md5_code = md5(fp['body']).hexdigest()
            sha1_code = sha1(fp['body']).hexdigest()

            exist = self.image.find_one({
                'md5_code': md5_code,
                'sha1_code': sha1_code
            })
            if exist:
                file_list.append(
                    dict(
                        image_id=exist.get('image_id'),
                        path=exist.get('path'),
                        name=filename + ext))
                continue

            self.image.insert(
                dict(
                    image_id=image_id,
                    user_id=params.user_id,
                    md5_code=md5_code,
                    sha1_code=sha1_code,
                    name=filename + ext,
                    path='/image/' + image_id + ext,
                    update_time=int(time.time())))

            qcos_bucket.put_object(
                path='/image/' + image_id + ext.lower(), body=fp['body'])

            file_list.append(
                dict(
                    image_id=image_id,
                    path='/image/' + image_id + ext,
                    name=filename + ext))

        self.success(dict(file_list=file_list))


class Image(BaseHandler):
    """Handler image stuff."""

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        _params = yield self.check_auth()

        image_list = self.image.find(
            dict(user_id=_params.user_id),
            projection={
                '_id': 0,
                'md5_code': 0,
                'sha1_code': 0,
                'user_id': 0
            })

        res = list(image for image in image_list)
        self.success(data=res)

    @web.asynchronous
    @gen.coroutine
    def post(self, *_args, **_kwargs):
        _params = yield self.check_auth()

        file_meta = self.request.files
        file_list = []
        for fp in file_meta['file']:
            filename, ext = os.path.splitext(fp['filename'])

            ext = ext.lower()
            image_id = str(uuid())
            md5_code = md5(fp['body']).hexdigest()
            sha1_code = sha1(fp['body']).hexdigest()

            exist = self.image.find_one({
                'md5_code': md5_code,
                'sha1_code': sha1_code
            })
            if exist:
                if 'user_id' not in exist:
                    self.image.update_one({
                        'md5_code': md5_code,
                        'sha1_code': sha1_code
                    }, {
                        '$set': {
                            'user_id': _params.user_id,
                            'update_time': int(time.time()),
                            'name': filename + ext
                        }
                    })
                file_list.append(
                    dict(
                        image_id=exist.get('image_id'),
                        path=exist.get('path'),
                        name=filename + ext))
                continue

            qcos_bucket.put_object(
                path=f'/image/' + image_id + ext.lower(), body=fp['body'])

            self.image.insert(
                dict(
                    image_id=image_id,
                    md5_code=md5_code,
                    sha1_code=sha1_code,
                    name=filename + ext,
                    path=f'/middle/image/record/' + image_id + ext,
                    update_time=int(time.time())))

            file_list.append(
                dict(
                    image_id=image_id,
                    path=f'/middle/image/record/' + image_id + ext,
                    name=filename + ext))

        self.success(data=dict(file_list=file_list))

    @web.asynchronous
    @gen.coroutine
    def delete(self, *_args, **_kwargs):
        _params = yield self.check_auth()

        args = self.parse_form_arguments('image_id')

        image_info = self.image.find_one_and_delete(
            dict(image_id=args.image_id))

        qcos_bucket.delete_object(path=image_info['path'])

        self.success()


class ImageRecord(BaseHandler):
    """Handler image stuff."""

    id_checker = re.compile(
        r'^([0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12})$')
    referer_checker = re.compile(r'\/\/lazor\.cn\/')

    @web.asynchronous
    @gen.coroutine
    def get(self, *_args, **_kwargs):
        source = self.request.uri.split('/')[-1]
        referer = self.request.headers.get('Referer')

        if not referer or not re.search(self.referer_checker, referer):
            self.set_status(404)
            return self.fail(4004)

        image_id, _ = os.path.splitext(source)

        if re.match(self.id_checker, image_id):
            self.image.find_one_and_update({
                'image_id': image_id
            }, {'$set': {
                'update_time': int(time.time())
            }})

        self.redirect('/image/' + source)
