from django import template

register = template.Library()


@register.simple_tag
def mediapath(image_path):
    return f"/static/img/{image_path}"
