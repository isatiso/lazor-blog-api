# coding:utf-8
"""Base Module."""
import types
import enum
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


def to_dict(self, options=None):
    res = dict()
    for key in self.__dict__:
        if not options or key in options:
            if not key.startswith('_'):
                if isinstance(self.__dict__[key], enum.Enum):
                    res[key] = self.__dict__[key].name
                else:
                    res[key] = self.__dict__[key]

    return res


BASE.to_dict = to_dict
# BASE.__repr__ = lambda
# self: self.__tablename__ + ' => ' + str(self.to_dict())
