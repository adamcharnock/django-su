"""
This file exists to contain all Django and Python compatibility issues.

In order to avoid circular references, nothing should be imported from
django_su.
"""

import sys
import django

if django.VERSION[:2] < (1, 5):
    # If the user is using Django < 1.5, then load up the url tag
    # from future. Otherwise use the normal one. The purpose of this
    # is to get the url template tag that supports context variables
    # for the first argument, yet won't raise a deprecation warning
    # about importing it from future.
    from django.templatetags.future import url  # NOQA
else:
    from django.template.defaulttags import url  # NOQA

if django.VERSION[:2] < (1, 6):
    from django.utils import six
    from django.utils.importlib import import_module
    from django.core.exceptions import ImproperlyConfigured

    def import_by_path(dotted_path, error_prefix=''):
        """
        Import a dotted module path and return the attribute/class designated by the
        last name in the path. Raise ImproperlyConfigured if something goes wrong.
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
                error_prefix, dotted_path))
        try:
            module = import_module(module_path)
        except ImportError as e:
            msg = '%sError importing module %s: "%s"' % (
                error_prefix, module_path, e)
            six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                        sys.exc_info()[2])
        try:
            attr = getattr(module, class_name)
        except AttributeError:
            raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
                error_prefix, module_path, class_name))
        return attr

elif django.VERSION[:2] < (1, 8):
    from django.utils.module_loading import import_by_path

else:
    from django.utils.module_loading import import_string as import_by_path
