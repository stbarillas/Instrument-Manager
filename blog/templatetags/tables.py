from django import template
from django.db.models import Q
from django.utils import timezone
import datetime


register = template.Library()

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




# @register.filter(name='exists')
# def exists(document, user):
#     if TrainingRecord.objects.filter(user = user, document_name = document):
#         result = True
#     else:
#         result = False
#     return result
#
# @register.filter(name='team_member_records')
# def team_member_records(team_member):
#     records = TrainingRecord.objects.order_by('document_name', '-created_date').distinct('document_name').filter(user = team_member)
#     return records
#
# @register.filter(name='test')
# def test(document, member):
#     if TrainingRecord.objects.all():
#         result = True
#     else:
#         result = False
#     print(result)
#     return result
#
# @register.filter(name='required_documents')
# def required_documents(member):
#     job_title = member.job_title
#     req_document = job_title.required_training.all()
#     return req_document
#
#
# @register.filter(name='not_required_documents')
# def not_required_documents(member):
#     job_title = member.job_title
#     req_document = job_title.required_training.all()
#     my_filter_qs = Q()
#     for doc in req_document:
#         my_filter_qs = my_filter_qs | Q(document_name=doc)
#     not_req_document = TrainingDocument.objects.exclude(my_filter_qs)
#     return not_req_document
#
# @register.filter(name='not_required_documents')
# def not_required_documents(member):
#     job_title = member.job_title
#     req_document = job_title.required_training.all()
#     my_filter_qs = Q()
#     for doc in req_document:
#         my_filter_qs = my_filter_qs | Q(document_name=doc)
#     not_req_document = TrainingDocument.objects.exclude(my_filter_qs)
#     return not_req_document