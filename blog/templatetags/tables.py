from django import template
from django.utils import timezone


register = template.Library()

#Creates displayed waitlist by comparing instrument primary keys
@register.filter(name='waitlist')
def waitlist(checklists, instrument):
    list = []
    for checklist in checklists:
        if checklist.instrument_pk == instrument.pk:
            list.append(checklist)
    return list[:7]

@register.filter(name='elapsed_time_calculator')
def elapsed_time_calculator(ownership_time):
    elapsed_time = timezone.now() - ownership_time

    #calculate all times for formating time delta (this can be made into a reusable function)
    seconds = elapsed_time.total_seconds()
    days = round(seconds // 86400)
    hours = round((seconds % 86400) // 3600)
    minutes = round((seconds % 3600) // 60)
    seconds = round(seconds % 60)

    #set conditions so the format you want is displayed depending on the elapsed time
    if days==0 and hours==0 and minutes==0:
        return '{} sec'.format(seconds)
    elif days==0 and hours==0:
        return '{} min, {} sec'.format(minutes, seconds)
    elif days==0:
        return '{} hr, {} min'.format(hours, minutes)
    else:
        return '{} day, {} hr'.format(days, hours)
