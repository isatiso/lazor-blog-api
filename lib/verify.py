# coding:utf-8
"""Some Verify Function."""
import re

email_pattern = re.compile(r'^([\w\-.]+)@([\w-]+)(\.([\w-]+))+$')
password_pattern = re.compile(
    r'^[0-9A-Za-z`~!@#$%^&*()_+\-=\{\}\[\]:;"\'<>,.\\|?/]{6,24}$')


def verify_email(email):
    """Verify Email Pattern."""
    return re.match(email_pattern, email)


def verify_password(password):
    """Verify Password Pattern."""
    return re.match(password_pattern, password)
