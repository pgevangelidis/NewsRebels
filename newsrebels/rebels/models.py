from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first = models.CharField(max_length=128, null=True)
    last = models.CharField(max_length=128, null=True)
    def __str__(self):
        return self.user.username

class RSS(models.Model):
    rssId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    link = models.URLField()
    description = models.CharField(max_length=256, null=True)
    date_rss = models.DateField(auto_now=True)
    is_deleted = models.IntegerField(default=1)
    #selectedRSS = models.ManyToManyField(User,through='UserRSS', through_fields=('selected','userId'))
    UserRss = models.ManyToManyField(User)
    #suggestedRSS = models.ManyToManyField(User,through='SuggestedRSS', through_fields=('suggested','userId'))

    def __str__(self):
        return self.title

# Article Model
# is_deleted(default value = 1), descr: 1 for active, 3 for deleted
class Article(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=256)
    description = models.TextField()
    body = models.TextField()
    author = models.CharField(max_length=128)
    date = models.DateField(auto_now=False)
    is_deleted = models.IntegerField(default=1)
    provider = models.ManyToManyField(RSS)
    rates = models.ManyToManyField(User,through='Rank', through_fields=('articleId','userId'))
    def __str__(self):
        return self.title

class Rank(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    articleId = models.ForeignKey(Article, on_delete=models.CASCADE,null=True)
    rate = models.IntegerField(default=0)
    #is_deleted = models.IntegerField(default=1)

    def __str__(self):
        return self.rate

#class SuggestedRSS(models.Model):
#    userId = models.ForeignKey(User,on_delete=models.CASCADE, related_name='foreign_user_selected')
#    suggested = models.ForeignKey(RSS,on_delete=models.CASCADE)
#    title = models.CharField(max_length=128)
#
#    def __str__(self):
#        return self.suggested

#class UserRSS(models.Model):
#    userId = models.ForeignKey(User,on_delete=models.CASCADE)
#    selected = models.ForeignKey(RSS,on_delete=models.CASCADE)
#    title = models.CharField(max_length=128, null=True)
#
#    def __str__(self):
#        return self.selected
