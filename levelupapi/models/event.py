from django.db import models


class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.CharField(max_length=90)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    
    #on delete - if the organizer gets deleted, this event will also get deleted
    #if this game gets deleted, then this event will be deleted too