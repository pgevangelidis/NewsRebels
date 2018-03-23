from django.contrib import admin
from rebels.models import UserProfile
from rebels.models import RSS, Article, Rank
# Register your models here.

# Register your models here.
#Add in this class to customise the Admin Interface
admin.site.register(UserProfile)

admin.site.register(RSS)

admin.site.register(Article)

admin.site.register(Rank)
