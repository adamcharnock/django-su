# -*- coding: utf-8 -*-

from django.db.models import Q
from django.utils.encoding import force_text
from django.utils.html import escape

from ajax_select import register, LookupChannel

from django_su import get_user_model


@register('django_su')
class UsersLookup(LookupChannel):

    model = get_user_model()

    def get_query(self, q, request):
          return self.model.objects.filter(
              Q(username__icontains=q) | Q(pk__icontains=q)).order_by('pk')

    def format_match(self, obj):
        return escape(force_text("%s [pk: %s]" % (
            obj.get_full_name() or obj.username, obj.pk)))

    def format_item_display(self, obj):
        return escape(force_text("%s [pk: %s]" % (
            obj.get_full_name() or obj.username, obj.pk)))
