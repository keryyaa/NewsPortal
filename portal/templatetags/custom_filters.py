from django import template

register = template.Library()


@register.filter()
def censor(value: str):
    forbidden = ['фыавфывцйуйуцйыфвывфывфцуй']
    for _ in value.split():
        if _.isalpha() and _.lower() in forbidden:
            value = value.replace(_, f'{_[0]}{"*" * (len(_) - 1)}')
    return value
