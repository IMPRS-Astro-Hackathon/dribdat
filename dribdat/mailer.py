# -*- coding: utf-8 -*-
"""Helper for sending mail."""
from flask import url_for
from flask_mail import Message, Mail
from dribdat.utils import random_password  # noqa: I005


def user_activation(user):
    """Send an activation by e-mail."""
    act_hash = random_password(24)
    user.sso_id = act_hash
    user.save()
    base_url = url_for('public.home', _external=True)
    act_url = url_for('auth.activate', userhash=act_hash, _external=True)
    mail = Mail()
    msg = Message('Your new dribdat account')
    msg.recipients = [user.email]
    msg.body = "Thanks for signing up to dribdat at %s\n\n" % base_url \
               + "Tap here to activate your account:\n\n%s" % act_url
    mail.send(msg)
