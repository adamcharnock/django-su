# -*- coding: utf-8 -*-

from django import template

from ..utils import su_login_callback

register = template.Library()

@register.inclusion_tag('su/login_link.html', takes_context=True)
def login_su_link(context, user):
    return {'can_su_login': su_login_callback(user)}
