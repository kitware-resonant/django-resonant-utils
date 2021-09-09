from typing import Mapping, Optional, TypeVar

from django import template

register = template.Library()


_KT = TypeVar('_KT')
_VT_co = TypeVar('_VT_co', covariant=True)


@register.filter
def getitem(value: Mapping[_KT, _VT_co], arg: _KT) -> Optional[_VT_co]:
    """
    Retrieve value[arg] from a template, where arg can be a variable.
    """
    return value.get(arg, None)
