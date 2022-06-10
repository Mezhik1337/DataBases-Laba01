from tkinter import CASCADE
from typing import Callable
from django.db import models
class City(models.Model):
    city = models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.city
class Judje(models.Model):
    full_name = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)    
    def __str__(self) -> str:
        return self.full_name  
class Team(models.Model):
    team_name = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)  
    def __str__(self) -> str:
        return self.team_name
class Trainer(models.Model):
    trainer_name = models.CharField(max_length=30)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    grade = models.IntegerField() 
    def __str__(self) -> str:
        return self.trainer_name
class Sportsman(models.Model):
    sportsman_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False,)
    sex = models.CharField(max_length=1)
    weight = models.FloatField()
    grade = models.IntegerField()
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.sportsman_name
class Competition(models.Model):
    compatition_name = models.CharField(max_length=30)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    team_organisator = models.ForeignKey(Team, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    main_judje = models.ForeignKey(Judje, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.compatition_name
