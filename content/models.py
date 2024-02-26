from django.db import models
import uuid
import json
from django.conf import settings
# from django.contrib.postgres.fields import ArrayField

from utils.input_helper import RequestInputHelper

# Create your models here.
class Content(models.Model):
    content_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    # body = models.TextField() # NOTE: Suggestion. textfield makes more sense here
    summary = models.CharField(max_length=60)
    document = models.FileField(max_length=225, blank=False, null=False, upload_to='content/')
    categories = models.TextField()
    # categories = models.JSONField()
    # categories = ArrayField(models.CharField(max_length=64), blank=True, null=True) # Can be easily achieved in PostgreSQL 

    # Extra fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='content_author', on_delete=models.CASCADE)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='content_modified_by', on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='content_created_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def set_categories(self, arr):
        # Convert the array to a JSON string and store it in the TextField
        self.categories = json.dumps(arr)

    def get_categories(self):
        # Retrieve the JSON string from the TextField and convert it back to an array
        return json.loads(self.categories)
    
    def __str__(self):
       return self.title
    
    def save(self, *args, **kwargs):
        # input_helper = RequestInputHelper(data=self)
        # input_helper.content_categories_helper()
        super(Content, self).save(*args, **kwargs)
