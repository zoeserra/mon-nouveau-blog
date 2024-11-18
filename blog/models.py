from django.db import models
 
class Equipement(models.Model):
    id_equip = models.CharField(max_length=100, primary_key=True)
    disponibilite = models.CharField(max_length=20)
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.id_equip
 

class Character(models.Model):
    id_character = models.CharField(max_length=100, primary_key=True)
    etat = models.CharField(max_length=20)
    origine = models.CharField(max_length=20)
    sport = models.CharField(max_length=20)
    lieu = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='characters_photos/', null=True, blank=True)  

    def __str__(self):
        return self.id_character