from django import template
from config.settings import MEDIA_URL
from os.path import join

register = template.Library()


@register.simple_tag
def mediapath(format_string):
    return join(MEDIA_URL, format_string.name)


@register.simple_tag(takes_context=True)
def custom_page_href(context, page_num):
    """
    Меняет номер страницы для паджинации, не удаляя при этом остальные параметры
    """
    get_data = context['request'].GET.copy()
    get_data['page'] = page_num
    return get_data.urlencode()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
