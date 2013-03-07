from django.db.models import Model, DateTimeField, ForeignKey, CharField, Manager
from django.utils.timezone import now

class Kick (Model):
    kicker = ForeignKey('auth.User')
    machine = CharField(max_length=100)
    at = DateTimeField(default=now)
