from flask import g

from crystalcv.models.models import User, UserModel


def decode_token(*args, **kwargs):
    pass


def get_user_basic(username, password, **kwargs):
    user = UserModel.get_user_by_username_and_password(username=username, password=password)
    g.user = user


def get_current_user():
    return getattr(g, "user")
