from django.db import models
from account.models import User

# Create your models here.
class Query(models.Model):
    subject = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=500, blank=False)
    file = models.ImageField(upload_to='files/create', blank=False)
    status = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject + '-' + self.status


class ResponseToQuery(models.Model):
    query = models.ForeignKey(Query, blank=False, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=500, blank=False)
    response_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.query
    