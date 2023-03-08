from django.db import models

# Create your models here.

class Quiz(models.Model):

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.content
    
class LeaderBoard(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    score = models.IntegerField()
    time = models.CharField(max_length=50) #models.DurationField()
    date = models.DateField(auto_now_add=True)