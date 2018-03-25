from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=256, unique=True, null=True)
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

    def __str__(self):
        return self.title

# Article Model
# is_deleted(default value = 1), descr: 1 for active, 3 for deleted
class Article(models.Model):
    articleId = models.IntegerField(primary_key=True)
    url = models.URLField()
    title = models.CharField(max_length=256)
    description = models.TextField()
    body = models.TextField()
    author = models.CharField(max_length=128)
    date = models.DateField(auto_now=False)

    def __str__(self):
        return self.title

class Rank(models.Model):
    userId = models.ForeignKey(User, null=True)
    articleId = models.ForeignKey(Article, null=True)
    is_deleted = models.IntegerField(default=1)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.rate

class ArticleRss(models.Model):
    rssId = models.ForeignKey(RSS, null=True)
    articleId = models.ForeignKey(Article, null=True)
    is_deleted = models.IntegerField(default=1)

    def __str__(self):
        return self.rssId

class UserRSS(models.Model):
    userId = models.ForeignKey(User, null=True)
    rssId = models.ForeignKey(RSS, null=True)
    is_deleted = models.IntegerField(default=1)

    def __str__(self):
        return self.rssId
