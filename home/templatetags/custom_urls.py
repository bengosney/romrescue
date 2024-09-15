from django import template
from wagtail.models import Site

register = template.Library()


@register.simple_tag(takes_context=True)
def base_url(context):
    request = context["request"]
    site = Site.find_for_request(request)
    if not site:
        return ""

    base_url = f"{request.scheme}://{site.hostname}"
    if site.port:
        base_url += f":{site.port}"

    return base_url
