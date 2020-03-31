from django.db import models


class TestCase(models.Model):
    request_id = models.CharField(max_length=200)
    reference_id = models.CharField(max_length=200)
    test_case_id = models.CharField(max_length=200)
    data = models.TextField()