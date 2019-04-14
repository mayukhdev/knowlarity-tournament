from django.db import models


# Create your models here.
class Sport(models.Model):
    SPORT_CHOICE = (
        ('TT', 'Table Tennis'),
        ('FB', 'Foos Ball'),
    )
    name = models.CharField(max_length=2, choices=SPORT_CHOICE, default='TT')

    def __str__(self):
        return "{}".format(self.name)


class Team(models.Model):
    name = models.CharField(max_length=64, blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="sports")
    score = models.IntegerField(default=0)

    def __str__(self):
        return "{} {} : {} Score: {}".format(self.pk, self.sport, self.name, self.score)


class Employee(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    email_id = models.EmailField(max_length=70, unique=True)
    team = models.ManyToManyField(Team, blank=True, related_name="team")

    def __str__(self):
        return "{} {} ({})".format(self.first, self.last, self.email_id)
