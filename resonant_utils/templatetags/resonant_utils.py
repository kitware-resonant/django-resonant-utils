from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, TypeVar

from django import template

if TYPE_CHECKING:
    from collections.abc import Mapping

register = template.Library()


_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)


@register.filter
def getitem(value: Mapping[_KT, _VT_co], arg: _KT) -> _VT_co | None:
    """
    Retrieve `value[arg]` from a mapping `value`, where `arg` can be a variable.

    This will return `None` if `arg` is not found. It may be useful to chain the `default_if_none`
    filter after this one.

    Sample usage::
        {% load resonant_utils %}
        {% for key in some_keys %}
            {{ my_dict|getitem:key }}
        {% endfor %}
    """
    return value.get(arg, None)


@register.filter
def pretty_json(value: Any, indent: int | None = None) -> str:
    """
    Convert `value` to a JSON-formatted string.

    Optionally, `indent` can be specified as an positive integer number of spaces to pretty-print
    indentation with; `None` (the default) will disable pretty-printing.

    The output should typically be embedded within HTML an `<pre>` element.
    If `indent` is specified, the output will likely contain newlines, which `<pre>` will render.

    Sample usage::
    {% load resonant_utils %}
    <pre>{{ my_object|pretty_json:4 }}</pre>
    """
    return json.dumps(value, indent=indent)
