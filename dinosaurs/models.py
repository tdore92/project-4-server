from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Dinosaur(models.Model):
    name = models.CharField(max_length=50)

    class Type(models.TextChoices):
        CARNIVORE = 'Carnivore', _('Carnivore')
        HERBIVORE = 'Herbivore', _('Herbivore')
        PISCIVORE = 'Piscivore', _('Piscivore')

    type = models.CharField (
        max_length= 10,
        choices=Type.choices,
        default=Type.CARNIVORE
    )

    def is_upperclass(self):
        return self.type in {
        self.Type.CARNIVORE,
        self.Type.HERBIVORE,
    }

    danger_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

  
    class Size(models.TextChoices):
        LARGE = 'Large', _('Large')
        MEDIUM = 'Medium', _('Medium')
        SMALL = 'Small', _('Small')

    size = models.CharField (
        max_length= 10,
        choices=Size.choices,
        default=Size.MEDIUM
    )

    def is_upperclass(self):
        return self.size in {
        self.Size.MEDIUM,
        self.Size.LARGE,
        }

    description = models.CharField(max_length=500)
    image = models.CharField(max_length=250)
    price = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(10000000)])


    def __str__(self):
        return f'{self.name}'

class Comment(models.Model):
    content = models.TextField(max_length=250)
    dinosaur = models.ForeignKey(Dinosaur, 
    related_name='comments', 
    on_delete=models.CASCADE
    )

    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='dinoComments',
        on_delete=models.CASCADE
        
    )

    def __str__(self):
        return f'Comment {self.id} on {self.dinosaur}'

