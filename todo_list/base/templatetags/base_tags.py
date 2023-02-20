from django import template
from base.models import Task

register = template.Library()


def __get_delta_to_str(hours_minutes: dict) -> str:
    return f'{hours_minutes["hours"]}h {hours_minutes["minutes"]}m'


def __get_timedelta(obj: type[Task]) -> dict:
    td = obj.done_at - obj.created_at
    hours = (td.seconds // 3600) + (td.days * 24)
    minutes = (td.seconds // 60) % 60
    return {'hours': hours, 'minutes': minutes}


@register.filter(name='spent_to_finish')
def spent_to_finish(obj: type[Task]) -> __get_delta_to_str:
    return __get_delta_to_str(__get_timedelta(obj))


@register.filter(name='avg_time')
def get_avg_time(obj: list[type[Task]]) -> __get_delta_to_str:
    minutes = 0
    for item in obj:
        hm = __get_timedelta(item)
        minutes += (hm['hours'] * 60)
        minutes += hm['minutes']
    total_minutes = minutes // len(obj)
    avg_hours = (total_minutes // 60)
    avg_minutes = (total_minutes % 60)
    return __get_delta_to_str({'hours': avg_hours, 'minutes': avg_minutes})
