from django.db import models
from django.contrib.auth.models import User

SEX_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

# Create your models here.

class Wallet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    money = models.IntegerField()
    tickets = models.IntegerField()

    def __str__(self):
        return self.owner.username + "'s wallet"

class Kennel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Litter(models.Model):
    breeder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return " Litter #" + str(self.id) + " - " + self.breeder.username

class Dog(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sire = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="dogs_sire")
    dam = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="dogs_dam")
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='M')
    color = models.CharField(max_length=200)
    litter = models.ForeignKey(Litter, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self): 
        return self.name

class ColorGenetics(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE);
    kAlele = models.CharField(max_length=20, null=True, blank=True);
    aAlele = models.CharField(max_length=20, null=True, blank=True);
    eAlele = models.CharField(max_length=20, null=True, blank=True);
    bAlele = models.CharField(max_length=20, null=True, blank=True);
    dAlele = models.CharField(max_length=20, null=True, blank=True);
    sAlele = models.CharField(max_length=20, null=True, blank=True);
    mAlele = models.CharField(max_length=20, null=True, blank=True);

    def __str__(self): 
        return self.dog.name + "'s Genetics"


