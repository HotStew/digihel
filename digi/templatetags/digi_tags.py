import re

from dateutil import parser
from django import template
from django.utils.safestring import mark_safe

from ..models import Phase

register = template.Library()


@register.filter
def first_p(value):
    if value:
        p_search = re.search(r'<p(|\s+[^>]*)>.*<\/p>', value)
        if p_search:
            value = p_search.group(0)
            if len(p_search.group(1)) > 0:
                value = value.replace(p_search.group(1), '')
            return value
    return ''


@register.filter
def convert_datetime(value):
    return parser.parse(value)


def is_active_phase(this_phase, current_phase):
    if this_phase == current_phase:
        return 'active'
    else:
        return 'inactive'

@register.simple_tag
def phases_indicator(current_phase):
    if current_phase:
        html = '<ul class="phase-process">'
        html += '<li><span class="phase-label phase-label--discovery is-{activity}">Selvitys</span></li>'\
        .format(activity=is_active_phase(Phase.DISCOVERY, current_phase))
        html += '<li><span class="phase-label phase-label--alpha is-{activity}">Alfa</span></li>'\
        .format(activity=is_active_phase(Phase.ALPHA, current_phase))
        html += '<li><span class="phase-label phase-label--beta is-{activity}">Beta</span></li>'\
        .format(activity=is_active_phase(Phase.BETA, current_phase))
        html += '<li><span class="phase-label phase-label--live is-{activity}">Tuotanto</span></li>'\
        .format(activity=is_active_phase(Phase.LIVE, current_phase))
        html += '<li><span class="phase-label phase-label--retirement is-{activity}">Poisto</span></li>'\
        .format(activity=is_active_phase(Phase.RETIREMENT, current_phase))
        html += '</ul>'
        return mark_safe(html)
    return ''
