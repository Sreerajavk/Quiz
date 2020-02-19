from django.contrib.auth.models import User
from django.db import models

# Create your models here.




class Questions ( models.Model ):

    question = models.TextField( max_length= 500)
    choice1 = models.TextField( max_length= 100)
    choice2 = models.TextField(max_length=100)
    choice3 = models.TextField(max_length=100)
    choice4 = models.TextField(max_length=100)
    correct_answer = models.TextField( max_length= 100)


class ScoreCard ( models.Model ):

    username = models.ForeignKey( User  , on_delete=models.CASCADE )
    # email = models.EmailField()
    # phone = models.TextField(max_length=100)
    # College_name = models.TextField( max_length=100)
    score = models.IntegerField()


class TimeStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    status  = models.BooleanField(default=False)


