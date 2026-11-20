from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from django import template
from django.utils.html import format_html

if TYPE_CHECKING:
    from collections.abc import Mapping
    from datetime import datetime

register = template.Library()


@register.filter
def get_item[Key, Value](value: Mapping[Key, Value], arg: Key) -> Value | None:
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


@register.simple_tag
def local_datetime_script() -> str:
    """
    Load the `<relative-time>` custom element, which is required by the `local_datetime` tag.

    This should be included once, typically within the page `<head>`, on any page that uses
    the `local_datetime` tag.

    Sample usage::
    {% load resonant_utils %}
    <head>
      {% local_datetime_script %}
    </head>
    """
    return format_html(
        '<script type="module" src="{}"></script>',
        "https://cdn.jsdelivr.net/npm/@github/relative-time-element@5.3.1/+esm",
    )


@register.inclusion_tag("resonant_utils/local_datetime.html")
def local_datetime(value: datetime) -> dict[str, datetime]:
    """
    Render a datetime in the viewer's local timezone.

    This is rendered client-side by the `<relative-time>` custom element
    (https://github.com/github/relative-time-element), so the `local_datetime_script` tag must
    also be included on the page. Without it, the datetime is rendered server-side in the current
    Django timezone.

    Sample usage::
    {% load resonant_utils %}
    <p>Created {% local_datetime object.created %}</p>
    """
    return {
        "dt": value,
    }
