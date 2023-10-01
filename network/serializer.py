from rest_framework import serializers
from . models import *

class PostSerializer(serializers.ModelSerializer):
    model=Post
    fields=('content',
            'owner',
            'liked_by'
    )