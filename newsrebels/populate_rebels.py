import os
os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'newsrebels.settings')

import django
django.setup()
from rebels.models import Article, RSS, Rank

def populate():
    
