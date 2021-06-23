from django.db import models

class User(models.Model): 
    identity     = models.CharField(max_length=45, unique=True, null=True)
    kakao_id     = models.CharField(max_length=45, unique=True, null=True)
    password     = models.CharField(max_length=45)
    korean_name  = models.CharField(max_length=45)
    english_name = models.CharField(max_length=45)
    birth        = models.CharField(max_length=45)
    phone        = models.CharField(max_length=45, unique=True)
    email        = models.EmailField(max_length=100, unique=True)
    gender       = models.CharField(max_length=45)

    class Meta: 
        db_table = 'users'