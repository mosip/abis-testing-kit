from django.db import models


class Tests(models.Model):
    run_id = models.CharField(max_length=200, unique=True)
    run_type = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    msg = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RequestMap(models.Model):
    request_id = models.CharField(max_length=200)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Logs(models.Model):
    run_id = models.CharField(max_length=200)
    log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)