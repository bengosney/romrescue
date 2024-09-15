import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


def default_serializer(obj):
    return "ERR: " + str(obj)


@register.filter()
def inspect(value):
    if settings.DEBUG:
        return mark_safe("<pre>" + json.dumps(value.__dict__, default=default_serializer, indent=4) + "</pre>")
        return mark_safe("<pre>" + json.dumps(value.__dict__) + "</pre>")
        return mark_safe("<pre>" + "\n".join(dir(value)) + "</pre>")
