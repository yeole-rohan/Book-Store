from django import template
import datetime
register = template.Library()

def date_format(value):
    d1 = datetime.datetime.strptime("2013-07-12T07:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    new_format = "%Y-%m-%d"
    d1.strftime(new_format)
    return d1

register.filter("date_format", date_format)