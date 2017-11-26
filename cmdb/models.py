from django.db import models

# Create your models here.
class Resources(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    title = models.CharField(max_length=250)
    img_url = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def time_diff(self):
        from django.utils import timezone
        current = timezone.now()
        delta = current - self.updated_at

        return "{} 秒".format(delta.seconds)


class User(models.Model):
    email = models.CharField(max_length=45, blank=True, null=True)
    nickname = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=45, blank=True, null=True)
    prefix = models.IntegerField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    updated_at = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.nickname

class UserComment(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    resources = models.ForeignKey(Resources, models.DO_NOTHING)
    content = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)



class UserLikes(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    resources = models.ForeignKey(Resources, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)