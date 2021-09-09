from typing import Mapping, Optional, TypeVar

from django import template

register = template.Library()


_KT = TypeVar('_KT')
_VT_co = TypeVar('_VT_co', covariant=True)


@register.filter
def getitem(value: Mapping[_KT, _VT_co], arg: _KT) -> Optional[_VT_co]:
    """
    Retrieve `value[arg]` from a mapping `value`, where `arg` can be a variable.

    This will return `None` if `arg` is not found. It may be useful to chain the `default_if_none`
    filter after this one.

    Sample usage::
        {% load girder_utils %}
        {% for key in some_keys %}
            {{ my_dict|getitem:key }}
        {% endfor %}
    """
    return value.get(arg, None)
