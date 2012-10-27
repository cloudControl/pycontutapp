from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    exp_date = models.DateTimeField('date expired')
    created_by = models.ForeignKey(User)
    finished = models.BooleanField(default=False)

    def is_expired(self):
        return self.exp_date <= timezone.now()
    is_expired.admin_order_field = 'exp_date'
    is_expired.boolean = True
    is_expired.short_description = 'already expired?'

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.choice
