from django import template

from django_su.utils import can_su_login
register = template.Library()


@register.inclusion_tag('su/login_link.html', takes_context=True)
def login_su_link(context, user):
    return {'can_su_login': can_su_login(user)}
