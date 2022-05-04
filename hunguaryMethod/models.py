from django.db import models


# Create your models here.


class AuctionTask(models.Model):
    task_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auction_task'


class GitCommits(models.Model):
    start_work = models.TextField(blank=True, null=True)
    commit_and_push_time = models.TextField(blank=True, null=True)
    commit_message = models.TextField(blank=True, null=True)
    full_time = models.IntegerField(blank=True, null=True)
    task_id = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)
    sha = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'git_commits'


class LoadProgrammers(models.Model):
    programmer_id = models.IntegerField(blank=True, null=True)
    load_minutes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'load_programmers'


class Programmers(models.Model):
    github_email = models.CharField(max_length=45, blank=True, null=True)
    firstname = models.CharField(max_length=45, blank=True, null=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    surname = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programmers'


class Projects(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    fullname = models.TextField(blank=True, null=True)
    github = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class RefTaskType(models.Model):
    name = models.CharField(max_length=220, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ref_task_type'


class TaskDistribution(models.Model):
    task_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    time_dist = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_distribution'


class Tasks(models.Model):
    task_name = models.TextField(blank=True, null=True)
    created_ts = models.IntegerField(blank=True, null=True)
    difficult = models.IntegerField(blank=True, null=True)
    term = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    closed = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'



class Tasked(models.Model):
    task_name = models.TextField(blank=True, null=True)
    task_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tasked'


class Executors(models.Model):
    username = models.TextField(blank=True, null=True)
    plain_execute_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'executors'