from django.db import models


class User(models.Model):
    ...

    class Meta:
        db_table = 'user'


class Todo_list(models.Model):
    ...


    class Meta:
        db_table = 'todo_list'