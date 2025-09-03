from django import template
import base64

register = template.Library()

@register.filter
def base64encode(image):
    if image:
        return base64.b64encode(image).decode('utf-8')
    else:
        return ''
