from django.db.models import Model, DateTimeField, ForeignKey
from django.utils.timezone import now

class Kick (Model):
    kicker = ForeignKey('auth.User')
    at = DateTimeField(default=now)
