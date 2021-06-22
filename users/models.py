from django.db import models

class User(models.Model): 
    identity = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    name_kor = models.CharField(max_length=45)
    name_eng = models.CharField(max_length=45)
    birth    = models.CharField(max_length=45)
    phone    = models.CharField(max_length=45, unique=True)
    email    = models.EmailField(max_length=100, unique=True)
    gender   = models.BooleanField()

    class Meta: 
        db_table = 'users'