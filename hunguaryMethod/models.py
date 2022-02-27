from django.db import models


# Create your models here.


class Executors(models.Model):
    username = models.TextField(blank=True, null=True)
    plain_execute_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'executors'


class Tasks(models.Model):
    task_name = models.TextField(blank=True, null=True)
    task_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'